"""EP001-B2 primitives; importing/running this module never analyzes real data.

Frozen specification: commit 09404c92970a909b8263b11e334cb7b29ce7289a.
See ep001b2_implementation.md for algorithms, tolerances and execution boundaries.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

import numpy as np

GAMMAS = (0.5, 0.9, 1.0)
PRIMARY = tuple(range(76))
EXPOSED = tuple(range(76, 80))
CHECKPOINTS = (5, 20, 100, 500, 2000)
BOOTSTRAP_REPLICATES = 10_000
LD = np.longdouble


def vectors(*args):
    arrays = tuple(np.asarray(a, dtype=LD) for a in args)
    if not arrays or any(a.ndim != 1 or a.shape != arrays[0].shape
                         or not np.isfinite(a).all() for a in arrays):
        raise ValueError("expected aligned finite vectors")
    return arrays


def weights(w):
    (w,) = vectors(w)
    if not w.size or np.any(w < 0) or w.sum() <= 0:
        raise ValueError("weights must have positive total and be nonnegative")
    return w / w.sum()


def mean(x, w):
    x, w = vectors(x, w)
    return float(np.sum(x * weights(w), dtype=LD))


def hierarchical_weights(config, seed, expected_configs=None):
    config, seed = np.asarray(config), np.asarray(seed)
    if config.ndim != 1 or config.shape != seed.shape or not config.size:
        raise ValueError("empty or unaligned population")
    configs = np.unique(config)
    if expected_configs is not None and set(configs) != set(expected_configs):
        raise ValueError("missing or unexpected configuration; cannot drop a grid cell")
    out = np.zeros(config.size, dtype=LD)
    for c in configs:
        cm = config == c
        seeds = np.unique(seed[cm])
        for s in seeds:
            m = cm & (seed == s)
            out[m] = LD(1) / (len(configs) * len(seeds) * m.sum())
    return out


def conditional_mean(x, w, mask):
    x, w = vectors(x, w)
    m = np.asarray(mask, dtype=bool)
    if m.shape != x.shape:
        raise ValueError("unaligned conditioning mask")
    return mean(x[m], w[m]) if w[m].sum() > 0 else None


def quantiles(x, w, probabilities=(.25, .5, .75, .9)):
    x, w = vectors(x, w)
    if np.any(w < 0):
        raise ValueError("negative weight")
    p = np.asarray(probabilities)
    if np.any((p < 0) | (p > 1)):
        raise ValueError("quantile outside [0,1]")
    keep = w > 0
    if not keep.any():
        return [None] * len(p)
    x, w = x[keep], w[keep]
    order = np.argsort(x, kind="stable")
    cumulative = np.cumsum(w[order], dtype=LD)
    indices = np.minimum(np.searchsorted(cumulative, p * cumulative[-1]), len(x)-1)
    return [float(z) for z in x[order][indices]]


def finite_population(raw, split, block="primary"):
    if split not in (0, 1) or block not in ("primary", "exposed"):
        raise ValueError("explicit split and primary/exposed block required")
    d = np.asarray(raw["deltas"])
    if d.ndim != 2 or d.shape[1] != 11:
        raise ValueError("raw deltas must have columns 0,...,10")
    configs = PRIMARY if block == "primary" else EXPOSED
    return ((np.asarray(raw["split"]) == split)
            & np.isin(raw["config_id"], configs)
            & np.isfinite(raw["delta_now"])
            & np.isfinite(d[:, :10]).all(axis=1))


def validate_structure(raw, manifest):
    """Structure only: never derive transport, fit a scalar or inspect residuals."""
    n = 80 * 50 * 5 * 64
    required = {"config_id", "seed", "split", "checkpoint", "query_id", "delta_now", "deltas"}
    if not required.issubset(raw):
        raise ValueError("missing required raw fields")
    for key in ("config_id", "seed", "split", "checkpoint", "query_id", "delta_now"):
        if np.asarray(raw[key]).shape != (n,):
            raise ValueError(f"unexpected raw shape: {key}")
    if np.asarray(raw["deltas"]).shape != (n, 11):
        raise ValueError("unexpected deltas shape")
    c, s, sp, ck, q = [np.asarray(raw[k]) for k in
                       ("config_id", "seed", "split", "checkpoint", "query_id")]
    for a, hi in ((c, 80), (s, 50), (q, 64)):
        if not np.issubdtype(a.dtype, np.integer) or np.any((a < 0) | (a >= hi)):
            raise ValueError("invalid ID")
    if not np.array_equal(sp, (s >= 20).astype(int)) or not np.isin(ck, CHECKPOINTS).all():
        raise ValueError("unexpected split/checkpoint")
    ci = np.searchsorted(CHECKPOINTS, ck)
    key = (((c.astype(np.int64)*50+s)*5+ci)*64+q)
    if not np.all(np.bincount(key, minlength=n) == 1):
        raise ValueError("missing or duplicate configuration/seed/checkpoint/query")
    if manifest["master_seed"] != 20260913 or manifest["row_count"] != n:
        raise ValueError("wrong source manifest")
    configs = manifest["configurations"]
    if len(configs) != 80 or sorted(z["config_id"] for z in configs) != list(range(80)):
        raise ValueError("unexpected manifest grid")
    for z in configs:
        i = z["config_id"]
        di, ei, ni = i//16, (i%16)//8, (i%8)//4
        expected = dict(distribution_index=di, eta_index=ei, noise_index=ni,
                        eta=(.02,.05)[ei], target_noise_std=(0.,.1)[ni],
                        eta_teacher=(.02,.05)[(i%4)//2], teacher_variance=(.01,.05)[i%2],
                        distribution="gaussian" if di==0 else "gaussian_spike",
                        q=(None, 1/6, 1/3, .5, 1.)[di])
        if any(z[k] != v for k,v in expected.items()):
            raise ValueError(f"configuration mismatch: {i}")
    finite = np.isfinite(raw["delta_now"]) & np.isfinite(raw["deltas"][:, :10]).all(1)
    return {"finite_exclusions": [
        {"config_id": i, "seed": j, "excluded": int((~finite & (c==i) & (s==j)).sum())}
        for i,j in np.unique(np.column_stack((c[~finite],s[~finite])), axis=0)]}


def load_raw(path: Path):
    with np.load(path, allow_pickle=False) as archive:
        raw = {key: archive[key] for key in archive.files}
    manifest = json.loads(path.with_name("run_manifest.json").read_text())
    report = validate_structure(raw, manifest)
    return raw, manifest, report


def derived(delta_now, deltas, gamma):
    if gamma not in GAMMAS:
        raise ValueError("gamma outside preregistration")
    (now,) = vectors(delta_now)
    d = np.asarray(deltas, dtype=LD)
    if d.shape not in ((len(now), 10), (len(now), 11)) or not np.isfinite(d[:, :10]).all():
        raise ValueError("ten finite required Delta columns")
    with np.errstate(over="raise", invalid="raise"):
        powers = LD(gamma) ** np.arange(10)
        static = powers.sum() * d[:, 0]
        adapt = d[:, :10] @ powers
        target = now + LD(gamma)*adapt
        baseline = now + LD(gamma)*static
    if not all(np.isfinite(a).all() for a in (static, adapt, target, baseline)):
        raise FloatingPointError("derived overflow")
    return dict(B_H=float(powers.sum()), delta_static=static, delta_adapt=adapt,
                e_transport=adapt-static, c_static=baseline, c_transport=target,
                delta_c=LD(gamma)*(adapt-static))


@dataclass(frozen=True)
class ScalarFit:
    c: float
    loss: float
    regions: tuple[tuple[float, float], ...]
    method: str
    comparison_tolerance: float = 0.0


def _choose(regions, reference):
    candidates = [max(lo, min(hi, LD(reference))) for lo, hi in regions]
    return min(candidates, key=lambda c: (abs(c-reference), abs(c), c))


def lad_fit(static, target, w, constrained=False):
    """Weighted median of target/static with masses w*abs(static)."""
    x, y, w = vectors(static, target, w)
    w = weights(w)
    keep = (x != 0) & (w > 0)
    lo, hi = LD(-np.inf), LD(np.inf)
    tol = LD(0)
    if keep.any():
        ratios, mass = y[keep]/x[keep], w[keep]*abs(x[keep])
        if not np.isfinite(ratios).all():
            raise FloatingPointError("nonfinite LAD breakpoint")
        order = np.argsort(ratios, kind="stable")
        ratios, mass = ratios[order], mass[order]
        cum = np.cumsum(mass, dtype=LD)
        half = cum[-1]/2
        j = int(np.searchsorted(cum, half))
        lo = hi = ratios[j]
        # Comparison tolerance is arithmetic only, relative to total mass.
        tol = 64*np.finfo(LD).eps*len(mass)*cum[-1]
        if j > 0 and abs(cum[j-1]-half) <= tol:
            lo, hi = ratios[j-1], ratios[j]
        elif j+1 < len(mass) and abs(cum[j]-half) <= tol:
            lo, hi = ratios[j], ratios[j+1]
    if constrained:
        lo, hi = np.clip([lo, hi], 0, 1)
    c = _choose([(lo, hi)], LD(1))
    return ScalarFit(float(c), mean(abs(y-c*x), w), ((float(lo), float(hi)),),
                     "weighted_median_LAD",float(tol))


def ols_fit(static, target, w, constrained=False):
    x,y,w = vectors(static,target,w)
    w = weights(w)
    denom = np.sum(w*x*x, dtype=LD)
    c = np.sum(w*x*y, dtype=LD)/denom if denom != 0 else LD(1)
    if constrained:
        c = np.clip(c, 0, 1)
    return ScalarFit(float(c), mean((y-c*x)**2,w), (), "weighted_OLS")


def operational_fit(now, static, target_threshold, gamma, w, c_f, constrained=False):
    """Global weighted slope sweep; activation jump -w|b|, match jump +2w|b|."""
    a,x,t,w = vectors(now,static,target_threshold,w)
    if gamma not in GAMMAS or not np.isfinite(c_f):
        raise ValueError("invalid gamma/reference")
    w = weights(w); b = LD(gamma)*x; t = np.maximum(t,0)
    keep = (b != 0) & (w > 0)
    def objective(c):
        return np.sum(w*abs(np.maximum(a+b*c,0)-t), dtype=LD)
    if not keep.any():
        region = (LD(0),LD(1)) if constrained else (LD(-np.inf),LD(np.inf))
        c = _choose([region],LD(c_f))
        return ScalarFit(float(c),float(objective(c)),(tuple(map(float,region)),),"global_slope_sweep")
    ab,bb,tt,ww = a[keep],b[keep],t[keep],w[keep]
    breaks = np.concatenate((-ab/bb,(tt-ab)/bb))
    jumps = np.concatenate((-ww*abs(bb),2*ww*abs(bb)))
    if not np.isfinite(breaks).all():
        raise FloatingPointError("nonfinite operational breakpoint")
    # Domain endpoints are zero-jump events, not fitted bounds on primary c.
    if constrained:
        breaks = np.concatenate((breaks,np.array([0,1],dtype=LD)))
        jumps = np.concatenate((jumps,np.zeros(2,dtype=LD)))
    order = np.argsort(breaks,kind="stable")
    bp, first = np.unique(breaks[order],return_index=True)
    jump = np.add.reduceat(jumps[order],first)
    left = -np.sum(ww[bb<0]*abs(bb[bb<0]),dtype=LD)
    right_slopes = left + np.cumsum(jump,dtype=LD)
    values = np.empty(len(bp),dtype=LD); values[0] = objective(bp[0])
    increments = right_slopes[:-1]*np.diff(bp)
    values[1:] = values[0]+np.cumsum(increments,dtype=LD)
    eps = np.finfo(LD).eps
    slope_tol = 64*eps*len(breaks)*np.sum(abs(jumps),dtype=LD)
    scale = abs(values[0])+np.sum(abs(increments),dtype=LD)
    value_tol = 64*eps*len(breaks)*scale
    domain = (LD(0),LD(1)) if constrained else (LD(-np.inf),LD(np.inf))
    valid = (bp>=domain[0]) & (bp<=domain[1])
    minimum = values[valid].min()
    regions = [(z,z) for z,v in zip(bp[valid],values[valid]) if abs(v-minimum)<=value_tol]
    for i in range(len(bp)-1):
        lo,hi = max(bp[i],domain[0]),min(bp[i+1],domain[1])
        if lo<=hi and abs(right_slopes[i])<=slope_tol and max(abs(values[i]-minimum),abs(values[i+1]-minimum))<=value_tol:
            regions.append((lo,hi))
    if not constrained:
        # Exact sign tests avoid inventing flat tails from tiny nonzero slopes.
        if not np.any(bb<0) and abs(values[0]-minimum)<=value_tol:
            regions.append((LD(-np.inf),bp[0]))
        if not np.any(bb>0) and abs(values[-1]-minimum)<=value_tol:
            regions.append((bp[-1],LD(np.inf)))
    regions = sorted(set(regions))
    merged = []
    for lo,hi in regions:
        if merged and lo<=merged[-1][1]:
            merged[-1]=(merged[-1][0],max(hi,merged[-1][1]))
        else:
            merged.append((lo,hi))
    c = _choose(merged,LD(c_f))
    actual = objective(c)
    if not np.isfinite(actual) or abs(actual-minimum)>value_tol+64*eps*abs(actual):
        raise ArithmeticError("sweep/direct-objective disagreement; do not interpret fit")
    return ScalarFit(float(c),float(actual),tuple((float(l),float(h)) for l,h in merged),
                     "global_slope_sweep",float(value_tol))


def reduction(numerator, denominator):
    if not np.isfinite([numerator,denominator]).all() or min(numerator,denominator)<0:
        raise ValueError("losses must be finite and nonnegative")
    return None if denominator == 0 else 1-float(numerator)/float(denominator)


def comparisons(m0,m1,m2):
    return dict(R1=reduction(m1,m0),R2=reduction(m2,m0),G_2_1=reduction(m2,m1),
                difference_1_0=m1-m0,difference_2_0=m2-m0,difference_2_1=m2-m1)


def feasible_width(model,target):
    model,target = vectors(model,target)
    return abs(np.maximum(model,0)-np.maximum(target,0))


def functional_summary(target,prediction,w):
    target,prediction,w = vectors(target,prediction,w)
    residual = target-prediction
    mse = mean(residual**2,w)
    var = mean((target-mean(target,w))**2,w)
    return dict(loss=mean(abs(residual),w),rmse=float(np.sqrt(mse)),
                r_squared=None if var==0 else 1-mse/var,
                signed_quantiles=quantiles(residual,w),absolute_quantiles=quantiles(abs(residual),w))


def operational_summary(now, static, adapt, prediction, gamma, w):
    now,static,adapt,prediction,w = vectors(now,static,adapt,prediction,w)
    w=weights(w); target=now+gamma*adapt; baseline=now+gamma*static; model=now+gamma*prediction
    width=feasible_width(model,target)
    active=np.maximum(target,baseline)>0; inactive=~active
    return dict(loss=mean(width,w),full_width=mean(abs(model-target),w),
                active_mass=float(w[active].sum()),active_loss=conditional_mean(width,w,active),
                active_quantiles=quantiles(width[active],w[active],(.5,.9,.99)),
                induced_loss=mean(width*inactive,w),
                induced_positive=conditional_mean((model>0).astype(float),w,inactive),
                median_delta_c=quantiles(model-target,w,(.5,))[0])


def disagreement_curve(model,target,w):
    """Right-continuous step curve; decisions query iff cost < threshold."""
    model,target,w=vectors(model,target,w);w=weights(w)
    lo=np.maximum(np.minimum(model,target),0);hi=np.maximum(np.maximum(model,target),0)
    points=np.concatenate(([LD(0)],lo,hi))
    jumps=np.concatenate(([LD(0)],w,-w))
    order=np.argsort(points,kind="stable")
    endpoints,first=np.unique(points[order],return_index=True)
    levels=np.cumsum(np.add.reduceat(jumps[order],first),dtype=LD)
    area=np.sum(np.diff(endpoints)*levels[:-1],dtype=LD)
    direct=mean(feasible_width(model,target),w)
    if not np.isclose(area,direct,rtol=1e-10,atol=1e-12):
        raise ArithmeticError("disagreement curve integral mismatch")
    return dict(costs=endpoints,disagreement=levels,integral=float(area))


@dataclass(frozen=True)
class Calibration:
    """Immutable discovery calibration, explicitly distinct F/O objectives."""
    gamma: float
    configs: tuple[int,...]
    global_f: ScalarFit
    global_o: ScalarFit
    config_f: tuple[ScalarFit,...]
    config_o: tuple[ScalarFit,...]
    global_ols: ScalarFit
    config_ols: tuple[ScalarFit,...]
    global_f_01: ScalarFit
    global_o_01: ScalarFit
    config_f_01: tuple[ScalarFit,...]
    config_o_01: tuple[ScalarFit,...]


def calibrate_discovery(now,deltas,config,seed,split,gamma,expected_configs=PRIMARY):
    """Caller must supply discovery only; mixed arrays fail rather than auto-filter."""
    config=np.asarray(config);seed=np.asarray(seed);split=np.asarray(split)
    if not (config.shape==seed.shape==split.shape==np.asarray(now).shape):
        raise ValueError("unaligned calibration metadata")
    if not np.all(split==0) or not np.isin(seed,range(20)).all():
        raise ValueError("calibration is discovery-only")
    if not set(expected_configs).issubset(PRIMARY) or not np.isin(config,PRIMARY).all():
        raise ValueError("previously exposed configuration in primary calibration")
    w=hierarchical_weights(config,seed,expected_configs)
    v=derived(now,deltas,gamma);x=v['delta_static'];y=v['delta_adapt'];t=v['c_transport']
    now=np.asarray(now)
    def fits(mask):
        f=lad_fit(x[mask],y[mask],w[mask])
        return (f,operational_fit(now[mask],x[mask],t[mask],gamma,w[mask],f.c),
                ols_fit(x[mask],y[mask],w[mask]),lad_fit(x[mask],y[mask],w[mask],True),
                operational_fit(now[mask],x[mask],t[mask],gamma,w[mask],f.c,True))
    global_f,global_o,global_ols,global_f01,global_o01=fits(np.ones(len(config),dtype=bool))
    configs=tuple(sorted(expected_configs));local=[fits(config==c) for c in configs]
    return Calibration(gamma,configs,global_f,global_o,tuple(z[0] for z in local),
                       tuple(z[1] for z in local),global_ols,tuple(z[2] for z in local),
                       global_f01,global_o01,tuple(z[3] for z in local),tuple(z[4] for z in local))


def predictions(calibration,static,config):
    (x,)=vectors(static);config=np.asarray(config)
    if config.shape!=x.shape or not set(np.unique(config)).issubset(calibration.configs):
        raise ValueError("configuration outside frozen calibration")
    def local(fits):
        lookup={c:f.c for c,f in zip(calibration.configs,fits)}
        return x*np.array([lookup[c] for c in config],dtype=LD)
    return dict(M0=x,M1F=x*calibration.global_f.c,M2F=local(calibration.config_f),
                M1O=x*calibration.global_o.c,M2O=local(calibration.config_o),
                M1OLS=x*calibration.global_ols.c,M2OLS=local(calibration.config_ols),
                M1F01=x*calibration.global_f_01.c,M2F01=local(calibration.config_f_01),
                M1O01=x*calibration.global_o_01.c,M2O01=local(calibration.config_o_01))


def evaluate_fixed(calibration,now,deltas,config,seed,split,expected_configs=PRIMARY):
    """Pure evaluation of an already frozen calibration; never calls a fitter.

    Caller must freeze ALL discovery calibrations before calling on confirmation.
    Supports one configuration at a time for configuration reports; the default
    enforces the complete primary grid. Subset callers must report coverage.
    """
    config=np.asarray(config);seed=np.asarray(seed);split=np.asarray(split)
    if not (config.shape==seed.shape==split.shape==np.asarray(now).shape):
        raise ValueError("unaligned evaluation metadata")
    if not np.all(split==1) or not np.isin(seed,range(20,50)).all():
        raise ValueError("fixed evaluation requires confirmation records")
    w=hierarchical_weights(config,seed,expected_configs)
    v=derived(now,deltas,calibration.gamma)
    p=predictions(calibration,v['delta_static'],config)
    functional={k:functional_summary(v['delta_adapt'],p[k],w)
                for k in ('M0','M1F','M2F','M1OLS','M2OLS','M1F01','M2F01')}
    operational={k:operational_summary(now,v['delta_static'],v['delta_adapt'],p[k],calibration.gamma,w)
                 for k in ('M0','M1O','M2O','M1O01','M2O01')}
    curves={k:disagreement_curve(np.asarray(now)+calibration.gamma*p[k],v['c_transport'],w)
            for k in ('M0','M1O','M2O')}
    return dict(functional=functional,operational=operational,curves=curves,
                functional_comparisons=comparisons(*(functional[k]['loss'] for k in ('M0','M1F','M2F'))),
                operational_comparisons=comparisons(*(operational[k]['loss'] for k in ('M0','M1O','M2O'))))


def fitted_scalar_summary(calibration):
    """Configuration coefficients receive equal weight; no real-data invocation here."""
    def summary(fits):
        cs=[f.c for f in fits]
        return dict(coefficients=cs,quantiles=quantiles(cs,np.ones(len(cs))),
                    in_unit_interval=[0<=c<=1 for c in cs])
    return dict(global_functional=calibration.global_f.c,global_operational=calibration.global_o.c,
                configuration_functional=summary(calibration.config_f),
                configuration_operational=summary(calibration.config_o))


def bootstrap_multiplicities(replicates=BOOTSTRAP_REPLICATES):
    """Return [replicate, configuration, confirmation-seed-index] counts."""
    if not isinstance(replicates,int) or replicates<=0:
        raise ValueError("positive replicate count required")
    counts=np.zeros((replicates,76,30),dtype=np.uint8)
    for group in range(19):
        rng=np.random.default_rng(np.random.SeedSequence([20260915,group]))
        draws=rng.integers(0,30,size=(replicates,30))
        group_counts=np.zeros((replicates,30),dtype=np.uint8)
        np.add.at(group_counts,(np.arange(replicates)[:,None],draws),1)
        counts[:,group*4:group*4+4,:]=group_counts[:,None,:]
    return counts


def trajectory_table(values,config,seed):
    """Case averages [76,30,...], for fixed confirmation losses or numerators."""
    config=np.asarray(config);seed=np.asarray(seed);v=np.asarray(values,dtype=LD)
    if v.shape[0]!=len(config) or config.shape!=seed.shape or not np.isfinite(v).all():
        raise ValueError("invalid confirmation arrays")
    if not np.isin(config,PRIMARY).all() or not np.isin(seed,range(20,50)).all():
        raise ValueError("expected primary confirmation only")
    out=np.empty((76,30)+v.shape[1:],dtype=LD)
    for c in PRIMARY:
        for j,s in enumerate(range(20,50)):
            mask=(config==c)&(seed==s)
            if not mask.any():
                raise ValueError("missing confirmation trajectory")
            out[c,j]=v[mask].mean(axis=0)
    return out


def bootstrap_aggregate(table,counts):
    table=np.asarray(table,dtype=LD);counts=np.asarray(counts)
    if table.shape[:2]!=(76,30) or counts.ndim!=3 or counts.shape[1:]!=(76,30):
        raise ValueError("wrong bootstrap shape")
    if np.any(counts<0) or not np.all(counts.sum(2)==30):
        raise ValueError("invalid trajectory multiplicities")
    for group in range(19):
        if not np.all(counts[:,4*group:4*group+4]==counts[:,4*group:4*group+1]):
            raise ValueError("bootstrap must preserve shared quartet")
    by_config=np.einsum('rcs,cs...->rc...',counts,table)/30
    return dict(configuration=by_config,grid=by_config.mean(axis=1))


def bootstrap_case_weights(config,seed,counts_one_replicate):
    """For conditional quantiles/curves: same original rows with repeated mass."""
    config=np.asarray(config);seed=np.asarray(seed)
    if not np.isin(seed,range(20,50)).all():
        raise ValueError("confirmation required")
    base=hierarchical_weights(config,seed,PRIMARY)
    return base*np.asarray(counts_one_replicate)[config,seed-20]


def bootstrap_diagnostics(width,target,baseline,model,config,seed,counts):
    """Fixed-loss secondary diagnostics, using numerator/mass aggregation.

    Quantiles use bootstrap_case_weights with the original active mask. This
    function returns losses/masses/proportions for every replicate and scope;
    it never estimates a model or alters subset membership.
    """
    width,target,baseline,model=vectors(width,target,baseline,model)
    active=np.maximum(target,baseline)>0
    inactive=~active
    table=trajectory_table(np.column_stack((width,width*active,active,
                                            width*inactive,(model>0)*inactive,inactive)),config,seed)
    draws=bootstrap_aggregate(table,counts)
    result={}
    for scope,arr in draws.items():
        def divide(num,den):
            out=np.empty(num.shape,dtype=object);out[:]=None
            positive=den>0
            out[positive]=(num[positive]/den[positive]).astype(float)
            return out
        result[scope]=dict(loss=arr[...,0],active_loss=divide(arr[...,1],arr[...,2]),
                           active_mass=arr[...,2],induced_loss=arr[...,3],
                           induced_positive=divide(arr[...,4],arr[...,5]))
    return result


def percentile_interval(replicates):
    """None explicitly denotes undefined; no finite-only 95% interval."""
    seq=list(replicates)
    undefined=sum(v is None for v in seq)
    finite=[v for v in seq if v is not None]
    if any(not np.isfinite(v) for v in finite):
        raise ValueError("use None, not NaN/inf, for undefined estimands")
    interval=None if undefined or not finite else np.quantile(
        np.asarray(finite,dtype=float),[.025,.975],method='linear').tolist()
    return dict(interval=interval,undefined_replicates=undefined,replicates=len(seq),
                conditional_on_discovery=True)


def bootstrap_comparisons(losses):
    """Input [replicate,3] aggregate M0/M1/M2 losses, never casewise ratios."""
    losses=np.asarray(losses)
    if losses.ndim!=2 or losses.shape[1]!=3:
        raise ValueError("three aggregate model losses required")
    rows=[comparisons(*row) for row in losses]
    return {key:percentile_interval([row[key] for row in rows]) for key in rows[0]}


if __name__ == '__main__':
    raise SystemExit("B2 library only: no real-data execution command is enabled.")
