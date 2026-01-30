#!/usr/bin/env python3
"""
System Identification Module for Modeling_2026
================================================

Runs scipy.optimize.least_squares to fit per-category correction terms
(cor.*) that minimize CPI prediction error against measured data. Instruction
cycle counts (cat.*) are kept fixed — they come from datasheets.

Usage (from Python):
    from common.system_identification import identify_model, load_measurements_for_model
    model = ...  # any processor model instance
    measurements = load_measurements_for_model(Path("models/zilog/z80"))
    result = identify_model(model, measurements)

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

import json
import math
import numpy as np
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .base_model import (
    get_model_parameters,
    set_model_parameters,
    get_model_parameter_bounds,
    compute_model_residual_vector,
    compute_model_residuals,
)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class IdentificationResult:
    """Result of system identification for a single processor model."""
    corrections: Dict[str, float]            # optimized cor.* values
    loss_before: float                       # MSE before optimization
    loss_after: float                        # MSE after optimization
    residuals_before: Dict[str, float]       # per-workload residual before
    residuals_after: Dict[str, float]        # per-workload residual after
    converged: bool                          # did optimizer converge?
    iterations: int                          # number of optimizer iterations
    cpi_error_percent: float                 # % error on 'typical' workload (or best available)
    message: str = ""                        # optimizer status message
    free_parameters: List[str] = field(default_factory=list)  # names of tuned params


# ---------------------------------------------------------------------------
# Measurement loading
# ---------------------------------------------------------------------------

def load_measurements_for_model(model_dir: Path) -> Dict[str, float]:
    """Load measured CPI values from a processor's measurements directory.

    Reads ``measurements/measured_cpi.json`` and returns a dict mapping
    workload names to measured CPI values, suitable for passing directly
    to ``compute_model_residuals()`` or ``identify_model()``.

    Args:
        model_dir: Path to the processor directory
                   (e.g. ``models/zilog/z80``)

    Returns:
        Dict mapping workload name to measured CPI float.
        Empty dict if file is missing or unreadable.
    """
    path = model_dir / "measurements" / "measured_cpi.json"
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
        # Support both schema variants:
        #   "measurements" (standard schema from common/measurements.py)
        #   "workload_measurements" (alternate schema used by some models)
        entries = data.get("measurements", data.get("workload_measurements", []))
        measurements = {}
        for m in entries:
            workload = m.get("workload")
            cpi = m.get("measured_cpi")
            if workload and isinstance(cpi, (int, float)) and cpi > 0:
                measurements[workload] = float(cpi)
        return measurements
    except (json.JSONDecodeError, KeyError, TypeError):
        return {}


# ---------------------------------------------------------------------------
# Core identification
# ---------------------------------------------------------------------------

def identify_model(
    model,
    measurements: Dict[str, float],
    *,
    max_iterations: int = 200,
    ftol: float = 1e-10,
    xtol: float = 1e-10,
    gtol: float = 1e-10,
    verbose: int = 0,
) -> IdentificationResult:
    """Run system identification on a processor model.

    Only ``cor.*`` (correction) parameters are free. All ``cat.*`` (instruction
    category cycle counts) are kept fixed at their datasheet values.

    Uses ``scipy.optimize.least_squares`` with Levenberg-Marquardt or
    trust-region-reflective depending on whether bounds are finite.

    Args:
        model: Any processor model object with analyze(), get_parameters(), etc.
        measurements: Dict mapping workload name → measured CPI.
        max_iterations: Maximum optimizer iterations.
        ftol: Function tolerance for convergence.
        xtol: Parameter tolerance for convergence.
        gtol: Gradient tolerance for convergence.
        verbose: Verbosity level passed to least_squares (0=silent, 1, 2).

    Returns:
        IdentificationResult with optimized corrections and diagnostics.
    """
    from scipy.optimize import least_squares

    # --- snapshot original state so we can rollback ---
    all_params = get_model_parameters(model)
    original_params = dict(all_params)
    all_bounds = get_model_parameter_bounds(model)

    # --- identify free parameters (cor.* only) ---
    free_names = sorted(k for k in all_params if k.startswith("cor."))
    if not free_names:
        # No correction terms — initialize them from categories
        _ensure_corrections_exist(model)
        all_params = get_model_parameters(model)
        all_bounds = get_model_parameter_bounds(model)
        free_names = sorted(k for k in all_params if k.startswith("cor."))

    if not free_names:
        # Still nothing — can't optimize
        residuals_before = compute_model_residuals(model, measurements)
        loss = _mse(residuals_before)
        return IdentificationResult(
            corrections={},
            loss_before=loss,
            loss_after=loss,
            residuals_before=residuals_before,
            residuals_after=residuals_before,
            converged=False,
            iterations=0,
            cpi_error_percent=_typical_error_pct(residuals_before, measurements),
            message="No correction parameters available",
            free_parameters=[],
        )

    # --- compute residuals before optimization ---
    residuals_before = compute_model_residuals(model, measurements)
    loss_before = _mse(residuals_before)

    # --- build initial vector and bounds ---
    x0 = np.array([all_params[k] for k in free_names], dtype=np.float64)
    lb = np.array([all_bounds.get(k, (-5.0, 5.0))[0] for k in free_names])
    ub = np.array([all_bounds.get(k, (-5.0, 5.0))[1] for k in free_names])

    # --- build normalization weights (1/measured_cpi per workload) ---
    # This makes the optimizer minimize relative errors, preventing
    # high-CPI workloads from dominating the loss.
    workload_order = sorted(measurements.keys())
    norm_weights = np.array(
        [1.0 / measurements[w] for w in workload_order], dtype=np.float64
    )

    # --- objective function ---
    def objective(x):
        # Set free parameters on the model
        update = {name: float(val) for name, val in zip(free_names, x)}
        set_model_parameters(model, update)
        # Compute residual vector in consistent order
        residuals = compute_model_residuals(model, measurements)
        residual_vals = [residuals.get(w, 0.0) for w in workload_order]
        # Normalize by measured CPI → optimizer minimizes relative error
        return np.array(residual_vals, dtype=np.float64) * norm_weights

    # --- run optimizer ---
    result = least_squares(
        objective,
        x0,
        bounds=(lb, ub),
        method="trf",
        max_nfev=max_iterations,
        ftol=ftol,
        xtol=xtol,
        gtol=gtol,
        verbose=verbose,
    )

    # --- apply optimized values ---
    optimized = {name: float(val) for name, val in zip(free_names, result.x)}
    set_model_parameters(model, optimized)

    # --- compute residuals after optimization ---
    residuals_after = compute_model_residuals(model, measurements)
    loss_after = _mse(residuals_after)

    converged = result.status > 0  # status > 0 means converged

    # --- guard: rollback if typical-workload error got worse ---
    typical_err_before = _typical_error_pct(residuals_before, measurements)
    typical_err_after = _typical_error_pct(residuals_after, measurements)

    if typical_err_after > typical_err_before and typical_err_after > 5.0:
        # Optimization hurt the primary metric — rollback to original state
        set_model_parameters(model, original_params)
        final_params = get_model_parameters(model)
        corrections = {k: v for k, v in final_params.items() if k.startswith("cor.")}
        return IdentificationResult(
            corrections=corrections,
            loss_before=loss_before,
            loss_after=loss_before,  # unchanged
            residuals_before=residuals_before,
            residuals_after=residuals_before,
            converged=False,
            iterations=result.nfev,
            cpi_error_percent=typical_err_before,
            message="Rolled back: optimization worsened typical-workload error",
            free_parameters=free_names,
        )

    # --- extract only cor.* values for the result ---
    final_params = get_model_parameters(model)
    corrections = {k: v for k, v in final_params.items() if k.startswith("cor.")}

    return IdentificationResult(
        corrections=corrections,
        loss_before=loss_before,
        loss_after=loss_after,
        residuals_before=residuals_before,
        residuals_after=residuals_after,
        converged=converged,
        iterations=result.nfev,
        cpi_error_percent=typical_err_after,
        message=result.message,
        free_parameters=free_names,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_corrections_exist(model):
    """Initialize correction terms if the model has categories but no corrections."""
    categories = getattr(model, "instruction_categories",
                         getattr(model, "_instruction_categories", {}))
    corrections = getattr(model, "corrections", None)
    if corrections is None:
        model.corrections = {}
        corrections = model.corrections
    if not corrections and categories:
        for cat_name in categories:
            corrections[cat_name] = 0.0


def _mse(residuals: Dict[str, float]) -> float:
    """Mean squared error from a residual dict."""
    if not residuals:
        return float("inf")
    vals = list(residuals.values())
    return sum(r ** 2 for r in vals) / len(vals)


def _typical_error_pct(
    residuals: Dict[str, float],
    measurements: Dict[str, float],
) -> float:
    """Compute CPI error % on the 'typical' workload (or first available)."""
    # Prefer 'typical' workload
    for workload in ["typical"] + sorted(residuals.keys()):
        if workload in residuals and workload in measurements:
            measured = measurements[workload]
            if measured > 0:
                return abs(residuals[workload]) / measured * 100.0
    return float("inf")
