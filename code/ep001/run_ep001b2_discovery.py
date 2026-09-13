"""Fit and freeze EP001-B2 discovery calibrations, without confirmation analysis.

This command is intentionally limited to seeds 0--19 and configurations 0--75.
It uses the frozen mathematical implementation in analyze_ep001b2 and writes a
deterministic calibration artifact.  It has no confirmation-analysis path.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

import numpy as np
from numpy.lib import format as npformat

import analyze_ep001b2 as b2


PREREGISTRATION_COMMIT = "09404c92970a909b8263b11e334cb7b29ce7289a"
IMPLEMENTATION_COMMIT = "9ea32d07fac4d4b3663d7e9287be787dd3c43de0"
SCHEMA = "ep001b2.discovery-calibration"
SCHEMA_VERSION = 1
DISCOVERY_SEEDS = tuple(range(20))
PRIMARY_CONFIGS = tuple(range(76))
EXPOSED_CONFIGS = tuple(range(76, 80))
ROWS_PER_SEED = 5 * 64
TOTAL_CONFIGS = 80
TOTAL_SEEDS = 50
REQUIRED_MEMBERS = (
    "config_id",
    "seed",
    "split",
    "checkpoint",
    "query_id",
    "delta_now",
    "deltas",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discovery_ranges(
    primary_configs: int = len(PRIMARY_CONFIGS),
    discovery_seeds: int = len(DISCOVERY_SEEDS),
    total_seeds: int = TOTAL_SEEDS,
    rows_per_seed: int = ROWS_PER_SEED,
) -> list[tuple[int, int]]:
    """Contiguous raw-row ranges selected by the frozen discovery design."""
    if not (0 < primary_configs <= TOTAL_CONFIGS and 0 < discovery_seeds <= total_seeds):
        raise ValueError("invalid discovery range dimensions")
    ranges = []
    rows_per_config = total_seeds * rows_per_seed
    for config_id in range(primary_configs):
        start = config_id * rows_per_config
        ranges.append((start, start + discovery_seeds * rows_per_seed))
    return ranges


def _npy_header(stream) -> tuple[tuple[int, ...], bool, np.dtype]:
    version = npformat.read_magic(stream)
    if version == (1, 0):
        return npformat.read_array_header_1_0(stream)
    if version == (2, 0):
        return npformat.read_array_header_2_0(stream)
    if version == (3, 0):
        return npformat.read_array_header_2_0(stream)
    raise ValueError(f"unsupported NPY version: {version}")


def read_selected_member(
    archive: zipfile.ZipFile,
    name: str,
    ranges: list[tuple[int, int]],
    expected_rows: int,
) -> np.ndarray:
    """Decode only selected row ranges from one compressed NPY member.

    ``ZipExtFile.seek`` may internally decompress bytes while moving forward,
    but rows outside ``ranges`` are never converted to NumPy arrays, retained,
    or passed into any B2 calculation.
    """
    with archive.open(f"{name}.npy", "r") as stream:
        shape, fortran_order, dtype = _npy_header(stream)
        if fortran_order or not shape or shape[0] != expected_rows or dtype.hasobject:
            raise ValueError(f"unsupported source member layout: {name}")
        trailing = int(np.prod(shape[1:], dtype=np.int64)) if len(shape) > 1 else 1
        row_bytes = dtype.itemsize * trailing
        selected = []
        current = 0
        for start, stop in ranges:
            if not (current <= start < stop <= shape[0]):
                raise ValueError("invalid or unordered selected ranges")
            skip = (start - current) * row_bytes
            if skip and stream.seek(skip, io.SEEK_CUR) < 0:
                raise OSError("failed to skip unselected source rows")
            payload = stream.read((stop - start) * row_bytes)
            if len(payload) != (stop - start) * row_bytes:
                raise EOFError(f"truncated source member: {name}")
            selected.append(
                np.frombuffer(payload, dtype=dtype)
                .reshape((stop - start,) + shape[1:])
                .copy()
            )
            current = stop
    return np.concatenate(selected, axis=0)


def load_discovery_only(raw_path: Path) -> tuple[dict[str, np.ndarray], dict, dict]:
    """Materialize only configs 0--75, seeds 0--19 from the preserved archive."""
    manifest_path = raw_path.with_name("run_manifest.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    expected_rows = TOTAL_CONFIGS * TOTAL_SEEDS * ROWS_PER_SEED
    if (
        manifest.get("master_seed") != 20260913
        or manifest.get("row_count") != expected_rows
        or manifest.get("raw_file") != raw_path.name
    ):
        raise ValueError("unexpected EP001-A manifest")
    configurations = manifest.get("configurations", [])
    if [item.get("config_id") for item in configurations] != list(range(TOTAL_CONFIGS)):
        raise ValueError("unexpected configuration grid")

    ranges = discovery_ranges()
    with zipfile.ZipFile(raw_path, "r") as archive:
        members = set(archive.namelist())
        expected_members = {f"{name}.npy" for name in REQUIRED_MEMBERS}
        if not expected_members.issubset(members):
            raise ValueError("preserved archive lacks required B2 members")
        raw = {
            name: read_selected_member(archive, name, ranges, expected_rows)
            for name in REQUIRED_MEMBERS
        }

    expected_count = len(PRIMARY_CONFIGS) * len(DISCOVERY_SEEDS) * ROWS_PER_SEED
    if any(value.shape[0] != expected_count for value in raw.values()):
        raise ValueError("wrong discovery-only row count")
    expected_config = np.repeat(PRIMARY_CONFIGS, len(DISCOVERY_SEEDS) * ROWS_PER_SEED)
    expected_seed = np.tile(
        np.repeat(DISCOVERY_SEEDS, ROWS_PER_SEED), len(PRIMARY_CONFIGS)
    )
    expected_checkpoint = np.tile(
        np.repeat(b2.CHECKPOINTS, 64), len(PRIMARY_CONFIGS) * len(DISCOVERY_SEEDS)
    )
    expected_query = np.tile(np.arange(64), expected_count // 64)
    if not (
        np.array_equal(raw["config_id"], expected_config)
        and np.array_equal(raw["seed"], expected_seed)
        and np.array_equal(raw["split"], np.zeros(expected_count, dtype=raw["split"].dtype))
        and np.array_equal(raw["checkpoint"], expected_checkpoint)
        and np.array_equal(raw["query_id"], expected_query)
    ):
        raise ValueError("source row ordering or discovery split differs from frozen design")
    if np.any(raw["seed"] >= 20) or np.any(raw["config_id"] >= 76):
        raise AssertionError("confirmation or exposed record entered discovery arrays")

    finite = np.isfinite(raw["delta_now"]) & np.isfinite(raw["deltas"][:, :10]).all(1)
    counts = []
    for config_id in PRIMARY_CONFIGS:
        in_config = raw["config_id"] == config_id
        counts.append(
            {
                "config_id": config_id,
                "candidate_cases": int(in_config.sum()),
                "finite_cases": int((in_config & finite).sum()),
                "excluded_nonfinite_cases": int((in_config & ~finite).sum()),
                "seeds_with_finite_cases": int(
                    np.unique(raw["seed"][in_config & finite]).size
                ),
            }
        )
    audit = {
        "candidate_cases": int(expected_count),
        "finite_cases": int(finite.sum()),
        "excluded_nonfinite_cases": int((~finite).sum()),
        "by_configuration": counts,
        "run_manifest_sha256": sha256_bytes(manifest_bytes),
        "raw_archive_filename": raw_path.name,
        "raw_archive_bytes": raw_path.stat().st_size,
        "unselected_rows_materialized": False,
    }
    return {key: value[finite] for key, value in raw.items()}, manifest, audit


def _endpoint(value: float):
    if np.isneginf(value):
        return "-Infinity"
    if np.isposinf(value):
        return "Infinity"
    if not np.isfinite(value):
        raise ValueError("unexpected nonfinite minimizer endpoint")
    return value


def fit_record(fit: b2.ScalarFit) -> dict:
    record = asdict(fit)
    record["regions"] = [
        [_endpoint(lo), _endpoint(hi)] for lo, hi in fit.regions
    ]
    return record


def calibration_record(calibration: b2.Calibration) -> dict:
    return {
        "gamma": calibration.gamma,
        "primary": {
            "functional": {
                "M1": fit_record(calibration.global_f),
                "M2": [
                    {"config_id": config_id, **fit_record(fit)}
                    for config_id, fit in zip(calibration.configs, calibration.config_f)
                ],
            },
            "operational": {
                "M1": fit_record(calibration.global_o),
                "M2": [
                    {"config_id": config_id, **fit_record(fit)}
                    for config_id, fit in zip(calibration.configs, calibration.config_o)
                ],
            },
        },
        "sensitivities": {
            "functional_OLS": {
                "M1": fit_record(calibration.global_ols),
                "M2": [
                    {"config_id": config_id, **fit_record(fit)}
                    for config_id, fit in zip(calibration.configs, calibration.config_ols)
                ],
            },
            "functional_LAD_constrained_0_1": {
                "M1": fit_record(calibration.global_f_01),
                "M2": [
                    {"config_id": config_id, **fit_record(fit)}
                    for config_id, fit in zip(calibration.configs, calibration.config_f_01)
                ],
            },
            "operational_constrained_0_1": {
                "M1": fit_record(calibration.global_o_01),
                "M2": [
                    {"config_id": config_id, **fit_record(fit)}
                    for config_id, fit in zip(calibration.configs, calibration.config_o_01)
                ],
            },
        },
    }


def build_artifact(raw: dict[str, np.ndarray], audit: dict) -> dict:
    if np.any(raw["seed"] >= 20) or np.any(raw["split"] != 0):
        raise ValueError("discovery artifact builder rejects confirmation records")
    if set(np.unique(raw["config_id"])) != set(PRIMARY_CONFIGS):
        raise ValueError("discovery artifact requires exactly configs 0--75")
    calibrations = [
        b2.calibrate_discovery(
            raw["delta_now"],
            raw["deltas"],
            raw["config_id"],
            raw["seed"],
            raw["split"],
            gamma,
        )
        for gamma in b2.GAMMAS
    ]
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "source_preregistration_commit": PREREGISTRATION_COMMIT,
        "source_implementation_commit": IMPLEMENTATION_COMMIT,
        "source": audit,
        "population": {
            "discovery_seeds": list(DISCOVERY_SEEDS),
            "primary_configs": list(PRIMARY_CONFIGS),
            "excluded_motivating_configs": list(EXPOSED_CONFIGS),
            "finite_required_fields": ["delta_now", "delta_0", "...", "delta_9"],
            "eligible_used": False,
            "rho_rev_used": False,
            "confirmation_records_used": False,
        },
        "H": 10,
        "hierarchical_weighting": [
            "equal_configuration",
            "equal_trajectory_within_configuration",
            "equal_case_within_trajectory",
        ],
        "calibrations": [calibration_record(item) for item in calibrations],
        "floating_point": {
            "numpy_version": np.__version__,
            "longdouble_eps": float(np.finfo(np.longdouble).eps),
        },
    }


def artifact_bytes(artifact: dict) -> bytes:
    return (json.dumps(artifact, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def _restore_endpoint(value):
    if value == "-Infinity":
        return -np.inf
    if value == "Infinity":
        return np.inf
    return float(value)


def restore_fit(record: dict) -> b2.ScalarFit:
    return b2.ScalarFit(
        c=float(record["c"]),
        loss=float(record["loss"]),
        regions=tuple(
            (_restore_endpoint(lo), _restore_endpoint(hi))
            for lo, hi in record["regions"]
        ),
        method=str(record["method"]),
        comparison_tolerance=float(record["comparison_tolerance"]),
    )


def load_frozen_discovery_artifact(
    path: Path, expected_sha256: str | None = None
) -> tuple[dict, dict[float, b2.Calibration]]:
    """Confirmation gate: load frozen coefficients without fitting anything."""
    payload = path.read_bytes()
    actual_sha256 = sha256_bytes(payload)
    if expected_sha256 is not None and actual_sha256 != expected_sha256:
        raise ValueError("discovery artifact checksum mismatch")
    artifact = json.loads(payload)
    if (
        artifact.get("schema") != SCHEMA
        or artifact.get("schema_version") != SCHEMA_VERSION
        or artifact.get("source_preregistration_commit") != PREREGISTRATION_COMMIT
        or artifact.get("source_implementation_commit") != IMPLEMENTATION_COMMIT
        or artifact.get("population", {}).get("confirmation_records_used") is not False
        or artifact.get("population", {}).get("discovery_seeds") != list(DISCOVERY_SEEDS)
        or artifact.get("population", {}).get("primary_configs") != list(PRIMARY_CONFIGS)
        or artifact.get("population", {}).get("excluded_motivating_configs")
        != list(EXPOSED_CONFIGS)
    ):
        raise ValueError("artifact does not satisfy the frozen confirmation gate")

    def group(record, name):
        section = record[name]
        local = section["M2"]
        if [item["config_id"] for item in local] != list(PRIMARY_CONFIGS):
            raise ValueError("artifact M2 grid mismatch")
        return restore_fit(section["M1"]), tuple(restore_fit(item) for item in local)

    restored = {}
    for record in artifact.get("calibrations", []):
        gamma = float(record["gamma"])
        functional, config_functional = group(record["primary"], "functional")
        operational, config_operational = group(record["primary"], "operational")
        ols, config_ols = group(record["sensitivities"], "functional_OLS")
        functional_01, config_functional_01 = group(
            record["sensitivities"], "functional_LAD_constrained_0_1"
        )
        operational_01, config_operational_01 = group(
            record["sensitivities"], "operational_constrained_0_1"
        )
        restored[gamma] = b2.Calibration(
            gamma,
            PRIMARY_CONFIGS,
            functional,
            operational,
            config_functional,
            config_operational,
            ols,
            config_ols,
            functional_01,
            operational_01,
            config_functional_01,
            config_operational_01,
        )
    if set(restored) != set(b2.GAMMAS):
        raise ValueError("artifact gamma grid mismatch")
    return artifact, restored


def discovery_report(artifact: dict, artifact_path: Path, checksum: str) -> str:
    globals_rows = []
    for item in artifact["calibrations"]:
        globals_rows.append(
            f"| {item['gamma']} | {item['primary']['functional']['M1']['c']:.17g} | "
            f"{item['primary']['operational']['M1']['c']:.17g} |"
        )
    source = artifact["source"]
    return "\n".join(
        [
            "# EP001-B2 discovery calibration record",
            "",
            "Discovery-only calibration under the frozen EP001-B2 preregistration. "
            "No confirmation performance endpoint or scientific interpretation is included.",
            "",
            f"- Artifact: `{artifact_path.name}`",
            f"- SHA-256: `{checksum}`",
            f"- Preregistration commit: `{PREREGISTRATION_COMMIT}`",
            f"- Implementation commit: `{IMPLEMENTATION_COMMIT}`",
            "- Seeds: 0--19 only",
            "- Primary configurations: 0--75",
            "- Excluded motivating configurations: 76--79",
            "- Population: finite `Delta_now` and `Delta_0,...,Delta_9`; no eligibility or reversal filter",
            f"- Candidate / finite / excluded cases: {source['candidate_cases']} / "
            f"{source['finite_cases']} / {source['excluded_nonfinite_cases']}",
            "- Weighting: equal configuration, then equal trajectory, then equal case",
            "- Primary coefficients per gamma/objective: one M1 and 76 M2",
            "- Sensitivities frozen: functional OLS, functional LAD [0,1], operational [0,1]",
            "- Confirmation seeds processed: no",
            "",
            "## Primary global discovery coefficients",
            "",
            "| gamma | functional M1 c_F^G | operational M1 c_O^G |",
            "|---:|---:|---:|",
            *globals_rows,
            "",
            "All configuration-specific coefficients and exact minimizing-region metadata are in the artifact. "
            "Coefficient values are recorded without a scalar-reducibility interpretation.",
            "",
        ]
    )


def run(raw_path: Path, output_dir: Path) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite frozen discovery output: {output_dir}")
    raw, _, audit = load_discovery_only(raw_path)
    first = build_artifact(raw, audit)
    second = build_artifact(raw, audit)
    first_payload = artifact_bytes(first)
    second_payload = artifact_bytes(second)
    if first_payload != second_payload:
        raise ArithmeticError("repeated discovery calibration is not deterministic")

    output_dir.mkdir(parents=True, exist_ok=False)
    artifact_path = output_dir / "discovery_calibration.json"
    artifact_path.write_bytes(first_payload)
    checksum = sha256_bytes(first_payload)
    loaded, restored = load_frozen_discovery_artifact(artifact_path, checksum)
    if artifact_bytes(loaded) != first_payload or set(restored) != set(b2.GAMMAS):
        raise ArithmeticError("lossless calibration artifact validation failed")
    report_path = output_dir / "discovery_calibration_report.md"
    report_path.write_text(discovery_report(first, artifact_path, checksum), encoding="utf-8")
    return {
        "artifact": str(artifact_path),
        "artifact_sha256": checksum,
        "report": str(report_path),
        "candidate_cases": audit["candidate_cases"],
        "finite_cases": audit["finite_cases"],
        "excluded_nonfinite_cases": audit["excluded_nonfinite_cases"],
        "deterministic_repeat": True,
        "lossless_reload": True,
        "confirmation_records_used": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.raw, args.output_dir)
    json.dump(result, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
