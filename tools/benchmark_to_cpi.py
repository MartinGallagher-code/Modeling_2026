#!/usr/bin/env python3
"""
Benchmark-to-CPI Conversion Utilities
=======================================

Converts published benchmark results (Dhrystone DMIPS, MIPS ratings,
SPECint scores) into per-workload CPI estimates suitable for calibrating
grey-box processor models.

Conversion formulas:
    CPI = clock_mhz / DMIPS           (for Dhrystone)
    CPI = clock_mhz / MIPS            (for native MIPS ratings)
    CPI ≈ clock_mhz / (specint × k)   (for SPEC, k varies by suite year)

Per-workload adjustment factors account for the fact that published benchmarks
(especially Dhrystone) are integer-heavy and don't represent all workload
types equally.

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

from typing import Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# Workload adjustment factors
# ---------------------------------------------------------------------------
# Dhrystone and most published MIPS ratings reflect "typical integer"
# workloads.  We derive other workload CPI estimates using multipliers.
#
# Rationale:
#   typical  = 1.00  — benchmark baseline IS the typical workload
#   compute  = 0.85  — compute-heavy code has higher IPC (fewer memory stalls)
#   memory   = 1.25  — memory-bound code incurs more stalls
#   control  = 1.10  — branch-heavy code has slightly worse IPC
#   mixed    = 1.00  — mixed workloads are close to typical

WORKLOAD_FACTORS = {
    "typical": 1.00,
    "compute": 0.85,
    "memory":  1.25,
    "control": 1.10,
    "mixed":   1.00,
}

# For pre-cache era processors (before ~1985), memory-bound workloads
# are less differentiated because there's no cache miss penalty.
WORKLOAD_FACTORS_PRE_CACHE = {
    "typical": 1.00,
    "compute": 0.90,
    "memory":  1.15,
    "control": 1.08,
    "mixed":   1.00,
}


# ---------------------------------------------------------------------------
# SPEC-to-MIPS conversion constants
# ---------------------------------------------------------------------------
# SPECint scores are normalized to a reference machine.  We approximate
# MIPS from SPEC using empirically-derived constants per suite generation.
#
# SPECint89: reference = VAX 11/780 @ 1 MIPS ≈ SPECint89=1.0
# SPECint92: reference = VAX 11/780 @ 1 MIPS ≈ SPECint92=1.0 (same basis)
#   But SPECint92 uses different benchmarks, so the scaling differs.
#
# Approximate: MIPS ≈ SPECint89 × 1.0  (VAX MIPS)
#              MIPS ≈ SPECint92 × 1.0  (VAX MIPS, roughly)

SPEC_TO_MIPS_FACTOR = {
    "specint89": 1.0,   # SPECint89=1.0 ≈ 1 VAX MIPS
    "specint92": 1.0,   # SPECint92=1.0 ≈ 1 VAX MIPS (different benchmarks)
    "specfp92":  0.8,   # FP benchmarks — lower MIPS-equivalent
}


# ---------------------------------------------------------------------------
# Core conversion functions
# ---------------------------------------------------------------------------

def dmips_to_cpi(clock_mhz: float, dmips: float) -> float:
    """Convert Dhrystone MIPS to CPI.

    CPI = clock_MHz / DMIPS

    Args:
        clock_mhz: Processor clock speed in MHz.
        dmips: Dhrystone MIPS score.

    Returns:
        Estimated CPI (cycles per instruction).
    """
    if dmips <= 0:
        raise ValueError(f"DMIPS must be positive, got {dmips}")
    return clock_mhz / dmips


def mips_to_cpi(clock_mhz: float, mips: float) -> float:
    """Convert native MIPS rating to CPI.

    CPI = clock_MHz / MIPS

    Args:
        clock_mhz: Processor clock speed in MHz.
        mips: Published MIPS rating.

    Returns:
        Estimated CPI (cycles per instruction).
    """
    if mips <= 0:
        raise ValueError(f"MIPS must be positive, got {mips}")
    return clock_mhz / mips


def spec_to_estimated_cpi(
    clock_mhz: float,
    spec_score: float,
    spec_type: str = "specint92",
) -> float:
    """Estimate CPI from a SPEC benchmark score.

    SPEC scores are normalized to a reference machine (VAX 11/780 ≈ 1 MIPS).
    We convert: estimated_MIPS ≈ spec_score × factor, then CPI = clock / MIPS.

    Args:
        clock_mhz: Processor clock speed in MHz.
        spec_score: Published SPEC score.
        spec_type: One of 'specint89', 'specint92', 'specfp92'.

    Returns:
        Estimated CPI (cycles per instruction).
    """
    if spec_score <= 0:
        raise ValueError(f"SPEC score must be positive, got {spec_score}")
    factor = SPEC_TO_MIPS_FACTOR.get(spec_type, 1.0)
    estimated_mips = spec_score * factor
    return clock_mhz / estimated_mips


def peak_mips_to_cpi(clock_mhz: float, peak_mips: float, utilization: float = 0.6) -> float:
    """Convert datasheet peak MIPS to realistic CPI.

    Datasheet peak MIPS assumes 100% utilization (1 instruction/cycle for
    pipelined processors). Real code achieves lower throughput. We apply
    a utilization factor to estimate sustained CPI.

    Args:
        clock_mhz: Processor clock speed in MHz.
        peak_mips: Datasheet peak MIPS.
        utilization: Fraction of peak throughput achieved (default 0.6).

    Returns:
        Estimated CPI for typical workloads.
    """
    if peak_mips <= 0:
        raise ValueError(f"Peak MIPS must be positive, got {peak_mips}")
    sustained_mips = peak_mips * utilization
    return clock_mhz / sustained_mips


# ---------------------------------------------------------------------------
# Per-workload CPI derivation
# ---------------------------------------------------------------------------

def derive_workload_cpis(
    base_cpi: float,
    year: int = 1980,
    workloads: Optional[list] = None,
) -> Dict[str, float]:
    """Derive per-workload CPI values from a single benchmark CPI.

    Uses era-appropriate adjustment factors.

    Args:
        base_cpi: CPI from the benchmark (treated as "typical" workload).
        year: Processor release year (pre-1985 uses smaller factors).
        workloads: List of workload names to generate. Default: all standard.

    Returns:
        Dict mapping workload name to estimated CPI.
    """
    factors = WORKLOAD_FACTORS if year >= 1985 else WORKLOAD_FACTORS_PRE_CACHE
    if workloads is None:
        workloads = list(factors.keys())

    return {w: round(base_cpi * factors.get(w, 1.0), 4) for w in workloads}


def compute_uncertainty(
    benchmark_type: str,
    base_cpi: float,
) -> float:
    """Compute appropriate uncertainty (±) for a benchmark-derived CPI.

    Args:
        benchmark_type: One of 'dhrystone', 'mips_rating', 'specint92',
                        'specint89', 'datasheet_peak', 'published_mips'.
        base_cpi: The derived CPI value.

    Returns:
        Absolute uncertainty value (±CPI).
    """
    # Relative uncertainty by benchmark type
    relative_uncertainty = {
        "dhrystone":      0.08,  # ±8%  — well-defined benchmark
        "mips_rating":    0.15,  # ±15% — often marketing numbers
        "published_mips": 0.12,  # ±12% — from technical publications
        "specint89":      0.10,  # ±10% — standardized but older
        "specint92":      0.10,  # ±10% — standardized
        "specfp92":       0.12,  # ±12% — FP workloads vary more
        "datasheet_peak": 0.20,  # ±20% — peak != sustained
        "arm_benchmark":  0.08,  # ±8%  — manufacturer benchmarks
        "dsp_peak":       0.25,  # ±25% — DSP peak rates are very optimistic
    }
    pct = relative_uncertainty.get(benchmark_type, 0.15)
    return round(base_cpi * pct, 3)


def compute_confidence(benchmark_type: str) -> str:
    """Determine confidence level for a benchmark type.

    Args:
        benchmark_type: Type of benchmark source.

    Returns:
        'low', 'medium', or 'high'.
    """
    confidence_map = {
        "dhrystone":      "high",
        "specint89":      "high",
        "specint92":      "high",
        "specfp92":       "medium",
        "arm_benchmark":  "high",
        "published_mips": "medium",
        "mips_rating":    "medium",
        "datasheet_peak": "low",
        "dsp_peak":       "low",
    }
    return confidence_map.get(benchmark_type, "medium")
