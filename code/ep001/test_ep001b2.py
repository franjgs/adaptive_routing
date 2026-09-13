"""Synthetic-only EP001-B2 validation. Never opens preserved experiment files."""
import unittest
from unittest.mock import patch
from pathlib import Path
import json
import tempfile
import numpy as np

import analyze_ep001b2 as b
from analyze_ep001b import transport_values
import run_ep001b2_discovery as discovery
import run_ep001b2_confirmation as confirmation


class B2Tests(unittest.TestCase):
    def test_transport_identities_and_old_formulas(self):
        rng=np.random.default_rng(12)
        now=rng.normal(size=7);d=rng.normal(size=(7,11))
        for gamma in b.GAMMAS:
            new=b.derived(now,d,gamma);old=transport_values(d,now,gamma)
            for key in ('delta_static','delta_adapt','e_transport','c_static','c_transport','delta_c'):
                np.testing.assert_allclose(new[key],old[key],atol=1e-14)
        self.assertEqual(b.derived(now,d,1)['B_H'],10)
        np.testing.assert_allclose(b.derived(now,d,1)['delta_adapt'],d[:,:10].sum(1))
        d[:,10]=np.nan
        self.assertTrue(np.isfinite(b.derived(now,d,.9)['delta_adapt']).all())

    def test_population_ignores_eligibility_and_reversal_diagnostics(self):
        raw=dict(config_id=np.array([0,75,76,79,0,0]),split=np.array([0,1,1,0,1,1]),
                 deltas=np.ones((6,11)),delta_now=np.ones(6),eligible=np.zeros(6,bool),
                 rho_rev=np.full(6,np.nan))
        raw['deltas'][:,10]=np.nan;raw['deltas'][4,9]=np.nan;raw['delta_now'][5]=np.inf
        np.testing.assert_array_equal(b.finite_population(raw,1),[False,True,False,False,False,False])
        raw['eligible'][:]=True
        np.testing.assert_array_equal(b.finite_population(raw,1),[False,True,False,False,False,False])
        self.assertEqual(b.finite_population(raw,1,'exposed').sum(),1)

    def test_hierarchical_unequal_counts_and_configs(self):
        c=np.array([0,0,0,1]);s=np.array([0,0,1,0])
        w=b.hierarchical_weights(c,s)
        np.testing.assert_allclose(w,[.125,.125,.25,.5])
        self.assertAlmostEqual(b.mean([0,0,8,4],w),4)
        self.assertNotEqual(b.mean([0,0,8,4],w),np.mean([0,0,8,4]))
        with self.assertRaises(ValueError):b.hierarchical_weights(c,s,range(3))

    def test_active_conditioning_restricts_original_measure(self):
        w=b.hierarchical_weights([0,0,0,1],[0,0,1,0])
        mask=np.array([True,False,False,True])
        self.assertAlmostEqual(b.conditional_mean([2,0,0,10],w,mask),8.4)
        self.assertEqual(b.quantiles(np.array([2,0,0,10])[mask],w[mask],(.5,.9,.99)),[10,10,10])
        self.assertIsNone(b.conditional_mean([1]*4,w,[False]*4))

    def test_lad_unique_flat_zero_and_constraint(self):
        self.assertEqual(b.lad_fit([1,2,0],[3,6,100],[1,1,1]).c,3)
        self.assertAlmostEqual(b.lad_fit([1,2,0],[3,6,100],[1,1,1]).loss,100/3)
        flat=b.lad_fit([1,1],[0,2],[1,1])
        self.assertEqual(flat.c,1);self.assertEqual(flat.regions,((0.,2.),))
        self.assertEqual(b.lad_fit([1,1],[2,4],[1,1]).c,2)
        self.assertEqual(b.lad_fit([0,0],[7,-5],[1,1]).c,1)
        self.assertEqual(b.lad_fit([1],[3],[1],True).c,1)
        self.assertEqual(b.lad_fit([-1],[2],[1],True).c,0)

    def test_lad_weighted_median_not_unweighted_ratios(self):
        fit=b.lad_fit([1,10],[0,30],[1,1])
        self.assertEqual(fit.c,3)

    def test_lad_brute_force_property(self):
        rng=np.random.default_rng(40)
        grid=np.linspace(-12,12,2401)
        for _ in range(25):
            x=rng.integers(-4,5,8);y=rng.integers(-5,6,8);w=rng.uniform(.1,2,8)
            fit=b.lad_fit(x,y,w)
            losses=np.average(abs(y[:,None]-x[:,None]*grid),weights=w,axis=0)
            self.assertLessEqual(fit.loss,losses.min()+1e-12)

    def test_operational_isolated_breakpoint(self):
        fit=b.operational_fit([1],[2],[5],.5,[1],0)
        self.assertEqual(fit.c,4);self.assertEqual(fit.loss,0)
        self.assertEqual(fit.regions,((4.,4.),))

    def test_operational_flat_interval_and_tie(self):
        # ReLU(c-2) + ReLU(-c) has minimizers [0,2].
        for reference,expected in [(-1,0),(.7,.7),(4,2)]:
            fit=b.operational_fit([-2,0],[1,-1],[0,0],1,[1,1],reference)
            self.assertAlmostEqual(fit.c,expected)
            self.assertEqual(fit.regions,((0.,2.),))

    def test_operational_disconnected_minimizers_lexicographic(self):
        # |ReLU(c)-1|+|ReLU(-c)-1| minimized at {-1,+1}.
        fit=b.operational_fit([0,0],[1,-1],[1,1],1,[1,1],0)
        self.assertEqual(fit.c,-1)
        self.assertEqual(fit.regions,((-1.,-1.),(1.,1.)))
        self.assertEqual(b.operational_fit([0,0],[1,-1],[1,1],1,[1,1],.1).c,1)
        self.assertEqual(b._choose([(-2,-2),(1,1)],b.LD(-.5)),1)

    def test_operational_multiple_flat_regions(self):
        # Sum of positive/negative ramps matching targets 1 and 2:
        # minima [-2,-1] and [1,2], separated by higher loss.
        fit=b.operational_fit([0]*4,[1,1,-1,-1],[1,2,1,2],1,[1]*4,1.4)
        self.assertAlmostEqual(fit.c,1.4)
        self.assertEqual(fit.regions,((-2.,-1.),(1.,2.)))

    def test_operational_tails_zero_and_constraint(self):
        left=b.operational_fit([1],[1],[0],1,[1],-5)
        self.assertEqual(left.c,-5);self.assertEqual(left.regions,((-np.inf,-1.),))
        right=b.operational_fit([1],[-1],[0],1,[1],5)
        self.assertEqual(right.c,5);self.assertEqual(right.regions,((1.,np.inf),))
        zero=b.operational_fit([2],[0],[7],1,[1],3)
        self.assertEqual(zero.c,3);self.assertEqual(zero.loss,5)
        self.assertEqual(b.operational_fit([2],[0],[7],1,[1],3,True).c,1)
        self.assertEqual(b.operational_fit([0],[1],[3],1,[1],0,True).c,1)

    def test_operational_near_breakpoint(self):
        target=1+2**-40
        fit=b.operational_fit([0],[1],[target],1,[1],0)
        self.assertEqual(fit.c,target)

    def test_operational_brute_force_property(self):
        rng=np.random.default_rng(98)
        for _ in range(40):
            a=rng.integers(-3,4,6);x=rng.integers(-3,4,6)
            t=rng.integers(-2,5,6);w=rng.uniform(.1,2,6)
            for constrained in (False,True):
                fit=b.operational_fit(a,x,t,.9,w,.75,constrained)
                grid=np.linspace(0,1,501) if constrained else np.linspace(-12,12,2401)
                loss=np.average(abs(np.maximum(a[:,None]+.9*x[:,None]*grid,0)-np.maximum(t[:,None],0)),weights=w,axis=0)
                self.assertLessEqual(fit.loss,loss.min()+1e-11)

    def test_operational_scale_equivariance(self):
        for scale in (1e-20,1.,1e20):
            f=b.operational_fit(np.array([0,0])*scale,np.array([1,-1])*scale,
                                np.array([1,1])*scale,1,[1,1],0)
            self.assertEqual(f.c,-1)

    def test_operational_independent_breakpoint_oracle(self):
        rng=np.random.default_rng(193)
        for _ in range(40):
            a=rng.normal(size=9);x=rng.normal(size=9);t=rng.normal(size=9)
            w=rng.uniform(.01,3,size=9);gamma=.5
            bp=np.r_[-a/(gamma*x),(np.maximum(t,0)-a)/(gamma*x)]
            losses=np.average(abs(np.maximum(a[:,None]+gamma*x[:,None]*bp,0)-np.maximum(t[:,None],0)),axis=0,weights=w)
            f=b.operational_fit(a,x,t,gamma,w,.32)
            self.assertAlmostEqual(f.loss,float(losses.min()),places=12)

    def test_feasible_width_four_sign_cases(self):
        np.testing.assert_array_equal(b.feasible_width([-2,-2,3,3],[-1,4,-1,5]),[0,4,3,2])

    def test_active_and_induced_diagnostics_and_gamma_regression(self):
        now=np.array([-2,-2,1,1]);static=np.zeros(4);adapt=np.zeros(4)
        prediction=np.array([6,0,2,0]);w=np.array([.125,.125,.25,.5])
        r=b.operational_summary(now,static,adapt,prediction,.5,w)
        self.assertAlmostEqual(r['loss'],.375)
        self.assertAlmostEqual(r['active_mass'],.75)
        self.assertAlmostEqual(r['active_loss'],1/3)
        self.assertAlmostEqual(r['induced_loss'],.125)
        self.assertAlmostEqual(r['induced_positive'],.5)
        self.assertEqual(r['active_quantiles'],[0,1,1])
        v=b.operational_summary([1],[1],[2],[1],.5,[1])
        self.assertEqual(v['median_delta_c'],-.5)
        empty=b.operational_summary([-2],[0],[0],[0],1,[1])
        self.assertIsNone(empty['active_loss']);self.assertEqual(empty['active_quantiles'],[None]*3)

    def test_curve_integral_and_equality(self):
        model=np.array([-1,2,4,3]);target=np.array([-2,4,-2,3]);w=[1,2,3,4]
        curve=b.disagreement_curve(model,target,w)
        self.assertAlmostEqual(curve['integral'],b.mean(b.feasible_width(model,target),w))
        for cost,level in zip(curve['costs'],curve['disagreement']):
            self.assertAlmostEqual(float(level),b.mean((cost<model)!=(cost<target),w))
        zero=b.disagreement_curve([-1],[-2],[1]);self.assertEqual(zero['integral'],0)

    def test_zero_denominators_and_negative_improvement(self):
        self.assertEqual(b.reduction(2,4),.5)
        self.assertEqual(b.reduction(0,4),1)
        self.assertEqual(b.reduction(8,4),-1)
        self.assertIsNone(b.reduction(0,0));self.assertIsNone(b.reduction(4,0))
        with self.assertRaises(ValueError):b.reduction(np.nan,1)
        self.assertIsNone(b.percentile_interval([0,None,1])['interval'])
        self.assertEqual(b.percentile_interval([0,None,1])['undefined_replicates'],1)
        np.testing.assert_allclose(b.percentile_interval([0,1])['interval'],[.025,.975])
        with self.assertRaises(ValueError):b.percentile_interval([np.nan])

    def test_ols_and_r_squared_degeneracy(self):
        self.assertEqual(b.ols_fit([1,2],[3,6],[1,1]).c,3)
        self.assertEqual(b.ols_fit([0],[3],[1]).c,1)
        self.assertIsNone(b.functional_summary([1,1],[1,1],[1,1])['r_squared'])

    def test_discovery_gate_and_prediction_models(self):
        now=np.ones(4);d=np.tile(np.linspace(1,.4,11),(4,1));c=np.array([0,0,1,1]);s=np.array([0,1,0,1])
        cal=b.calibrate_discovery(now,d,c,s,np.zeros(4),.9,expected_configs=(0,1))
        self.assertEqual(set(b.predictions(cal,np.ones(4),c)),
                         {'M0','M1F','M2F','M1O','M2O','M1OLS','M2OLS','M1F01','M2F01','M1O01','M2O01'})
        with self.assertRaises(ValueError):b.calibrate_discovery(now,d,c,s+20,np.ones(4),.9,(0,1))
        with self.assertRaises(ValueError):b.calibrate_discovery(now,d,c+76,s,np.zeros(4),.9,(76,77))

    def test_bootstrap_quartets_and_fixed_losses_no_refit(self):
        counts=b.bootstrap_multiplicities(7)
        np.testing.assert_array_equal(counts.sum(2),30)
        for start in range(0,76,4):
            for c in range(start,start+4):np.testing.assert_array_equal(counts[:,start],counts[:,c])
        self.assertFalse(np.array_equal(counts[:,0],counts[:,4]))
        np.testing.assert_array_equal(counts,b.bootstrap_multiplicities(7))
        table=np.arange(76*30,dtype=float).reshape(76,30)
        models=np.stack([table,table*.5,table*.25],axis=-1)
        with patch.object(b,'lad_fit',side_effect=AssertionError('refit')),patch.object(b,'operational_fit',side_effect=AssertionError('refit')):
            draws=b.bootstrap_aggregate(models,counts)
            ci=b.bootstrap_comparisons(draws['grid'])
        np.testing.assert_allclose(ci['R1']['interval'],[.5,.5])
        np.testing.assert_allclose(ci['R2']['interval'],[.75,.75])
        np.testing.assert_allclose(draws['grid'][:,1]-draws['grid'][:,0],-.5*draws['grid'][:,0])

    def test_bootstrap_conditional_weights_and_table(self):
        config=np.repeat(np.arange(76),30);seed=np.tile(np.arange(20,50),76)
        values=np.arange(len(config),dtype=float)
        table=b.trajectory_table(values,config,seed);counts=b.bootstrap_multiplicities(2)
        for i in range(2):
            w=b.bootstrap_case_weights(config,seed,counts[i])
            self.assertAlmostEqual(float(w.sum()),1)
            expected=b.bootstrap_aggregate(table,counts)['grid'][i]
            self.assertAlmostEqual(b.mean(values,w),float(expected))
        with self.assertRaises(ValueError):b.trajectory_table(values,config+4,seed)
        with self.assertRaises(ValueError):b.validate_structure({}, {})

    def test_fixed_evaluation_never_refits(self):
        d=np.tile(np.linspace(1,.4,11),(4,1));now=np.ones(4)
        config=np.array([0,0,1,1]);seed=np.array([0,1,0,1])
        cal=b.calibrate_discovery(now,d,config,seed,np.zeros(4),.5,(0,1))
        with patch.object(b,'lad_fit',side_effect=AssertionError('refit')),patch.object(b,'operational_fit',side_effect=AssertionError('refit')):
            result=b.evaluate_fixed(cal,now,d,config,seed+20,np.ones(4),(0,1))
        self.assertIn('operational_comparisons',result)
        self.assertEqual(b.fitted_scalar_summary(cal)['global_functional'],cal.global_f.c)

    def test_secondary_bootstrap_original_mass(self):
        config=np.repeat(np.arange(76),30);seed=np.tile(np.arange(20,50),76)
        baseline=np.where(seed%2,1.,-1.);target=baseline.copy()
        model=target+2.;width=b.feasible_width(model,target)
        counts=b.bootstrap_multiplicities(3)
        result=b.bootstrap_diagnostics(width,target,baseline,model,config,seed,counts)
        for i in range(3):
            w=b.bootstrap_case_weights(config,seed,counts[i]);active=baseline>0
            self.assertAlmostEqual(result['grid']['active_loss'][i],b.conditional_mean(width,w,active))
            self.assertAlmostEqual(float(result['grid']['induced_loss'][i]),b.mean(width*~active,w))
            self.assertAlmostEqual(result['grid']['induced_positive'][i],1.)

    def test_structural_schema_full_synthetic_metadata(self):
        from run_ep001a import build_configurations
        n=80*50*5*64
        i=np.arange(n,dtype=np.int64)
        raw=dict(config_id=i//16000,seed=(i//320)%50,
                 checkpoint=np.asarray(b.CHECKPOINTS)[(i//64)%5],query_id=i%64,
                 delta_now=np.ones(n),deltas=np.broadcast_to(np.ones(11),(n,11)))
        raw['split']=(raw['seed']>=20).astype(int)
        manifest=dict(master_seed=20260913,row_count=n,configurations=build_configurations())
        self.assertEqual(b.validate_structure(raw,manifest),{'finite_exclusions':[]})
        raw['query_id'][1]=raw['query_id'][0]
        with self.assertRaises(ValueError):b.validate_structure(raw,manifest)
        raw['query_id'][1]=1;raw['split'][0]=1
        with self.assertRaises(ValueError):b.validate_structure(raw,manifest)

    def test_discovery_artifact_round_trip_and_confirmation_gate(self):
        configs=tuple(range(76));fits=tuple(b.ScalarFit(1.,0.,((1.,1.),),'synthetic') for _ in configs)
        calibrations=[b.Calibration(gamma,configs,fits[0],fits[0],fits,fits,fits[0],fits,
                                    fits[0],fits[0],fits,fits) for gamma in b.GAMMAS]
        audit=dict(candidate_cases=1,finite_cases=1,excluded_nonfinite_cases=0,
                   by_configuration=[],run_manifest_sha256='synthetic',
                   raw_archive_filename='synthetic.npz',raw_archive_bytes=1,
                   unselected_rows_materialized=False)
        with patch.object(discovery.b2,'calibrate_discovery',side_effect=calibrations):
            raw=dict(seed=np.zeros(76,dtype=int),split=np.zeros(76,dtype=int),
                     config_id=np.arange(76),delta_now=np.ones(76),deltas=np.ones((76,11)))
            artifact=discovery.build_artifact(raw,audit)
        payload=discovery.artifact_bytes(artifact)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'calibration.json';path.write_bytes(payload)
            loaded,restored=discovery.load_frozen_discovery_artifact(
                path,discovery.sha256_bytes(payload))
            self.assertEqual(discovery.artifact_bytes(loaded),payload)
            self.assertEqual(restored[.5],calibrations[0])
            with self.assertRaises(ValueError):
                discovery.load_frozen_discovery_artifact(path,'0'*64)
            changed=json.loads(payload);changed['population']['confirmation_records_used']=True
            path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):discovery.load_frozen_discovery_artifact(path)

    def test_discovery_range_selection_is_primary_discovery_only(self):
        ranges=discovery.discovery_ranges(primary_configs=2,discovery_seeds=2,
                                           total_seeds=3,rows_per_seed=2)
        self.assertEqual(ranges,[(0,4),(6,10)])
        source=np.arange(12,dtype=np.int16)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'source.npz';np.savez_compressed(path,value=source)
            with np.load(path,allow_pickle=False) as check:
                self.assertEqual(check['value'].tolist(),source.tolist())
            with discovery.zipfile.ZipFile(path) as archive:
                selected=discovery.read_selected_member(archive,'value',ranges,12)
        self.assertEqual(selected.tolist(),[0,1,2,3,6,7,8,9])

    def test_confirmation_ranges_and_reduction_intervals(self):
        self.assertEqual(confirmation.confirmation_ranges((0,)),[(6400,16000)])
        self.assertEqual(confirmation.confirmation_ranges((76,))[0],
                         (76*16000+6400,77*16000))
        values=confirmation.reduction_array([1,0,2],[2,0,0])
        self.assertEqual(values[0],.5)
        self.assertTrue(np.isnan(values[1:]).all())

    def test_confirmation_primary_path_never_refits(self):
        configs=np.repeat(np.arange(76),30);seeds=np.tile(np.arange(20,50),76)
        raw=dict(config_id=configs,seed=seeds,split=np.ones(len(configs)),
                 delta_now=np.ones(len(configs)),deltas=np.ones((len(configs),11)))
        fit=b.ScalarFit(1.,0.,((1.,1.),),'synthetic');fits=tuple(fit for _ in range(76))
        calibration=b.Calibration(.5,tuple(range(76)),fit,fit,fits,fits,fit,fits,
                                  fit,fit,fits,fits)
        counts=b.bootstrap_multiplicities(2)
        with patch.object(b,'lad_fit',side_effect=AssertionError('refit')), \
             patch.object(b,'operational_fit',side_effect=AssertionError('refit')):
            point,boot,curves,trajectory=confirmation.analyze_primary_gamma(raw,calibration,counts)
        self.assertEqual(point['gamma'],.5)
        self.assertEqual(boot['functional']['grid']['losses']['M0']['replicates'],2)
        self.assertIn('gamma_0.5_M0_integral',curves)
        self.assertEqual(trajectory['gamma_0.5_functional_losses'].shape,(76,30,3))


if __name__=='__main__':
    unittest.main()
