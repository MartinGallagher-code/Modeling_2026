#!/usr/bin/env python3
"""
System Identification Module for Modeling_2026
================================================

Fits per-category correction terms (cor.*) that minimize CPI prediction
error against measured data. Instruction cycle counts (cat.*) are kept
fixed — they come from datasheets.

Three optimization methods are available:

1. **ridge** (default) — Regularized least-squares (L2 / Ridge).
   Adds a penalty on correction magnitude so that underdetermined systems
   (more parameters than workloads) produce unique, physically plausible
   solutions.  This is the recommended method.

2. **differential_evolution** — Global optimizer that searches the full
   feasible region.  Better for models where the loss surface has local
   minima or where corrections are pinned at bounds.  Slower but more
   robust.

3. **bayesian** — Bayesian optimization via Gaussian process surrogate.
   Sample-efficient, provides uncertainty estimates, good for expensive
   evaluations.  Requires scikit-optimize (``pip install scikit-optimize``).

Usage:
    from common.system_identification import identify_model
    result = identify_model(model, measurements)                    # ridge (default)
    result = identify_model(model, measurements, method='de')       # differential evolution
    result = identify_model(model, measurements, method='bayesian') # bayesian optimization

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
    get_model_parameter_metadata,
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
    method: str = "ridge"                    # which optimizer was used


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
# Common setup
# ---------------------------------------------------------------------------

def _setup_identification(model, measurements):
    """Common setup: find free parameters, compute initial state.

    Returns (free_names, x0, lb, ub, workload_order, norm_weights,
             residuals_before, loss_before, original_params)
    or None if there are no free parameters.
    """
    all_params = get_model_parameters(model)
    original_params = dict(all_params)
    all_bounds = get_model_parameter_bounds(model)

    # Identify free parameters (cor.*, free cache.*, free bp.*)
    all_metadata = get_model_parameter_metadata(model)
    free_names = sorted(
        k for k in all_params
        if k.startswith("cor.")
        or (k.startswith("cache.") and not all_metadata.get(k, {}).get('fixed', True))
        or (k.startswith("bp.") and not all_metadata.get(k, {}).get('fixed', True))
    )
    if not free_names:
        _ensure_corrections_exist(model)
        all_params = get_model_parameters(model)
        all_bounds = get_model_parameter_bounds(model)
        all_metadata = get_model_parameter_metadata(model)
        free_names = sorted(
            k for k in all_params
            if k.startswith("cor.")
            or (k.startswith("cache.") and not all_metadata.get(k, {}).get('fixed', True))
            or (k.startswith("bp.") and not all_metadata.get(k, {}).get('fixed', True))
        )

    if not free_names:
        return None

    # Compute residuals before optimization
    residuals_before = compute_model_residuals(model, measurements)
    loss_before = _mse(residuals_before)

    # Build initial vector and bounds
    x0 = np.array([all_params[k] for k in free_names], dtype=np.float64)
    lb = np.array([all_bounds.get(k, (-5.0, 5.0))[0] for k in free_names])
    ub = np.array([all_bounds.get(k, (-5.0, 5.0))[1] for k in free_names])

    # Clamp x0 to bounds — previous corrections may exceed current bounds
    x0 = np.clip(x0, lb, ub)

    # Normalization weights (1/measured_cpi per workload) so optimizer
    # minimizes relative errors
    workload_order = sorted(measurements.keys())
    norm_weights = np.array(
        [1.0 / measurements[w] for w in workload_order], dtype=np.float64
    )

    return (free_names, x0, lb, ub, workload_order, norm_weights,
            residuals_before, loss_before, original_params)


def _finalize_result(model, measurements, free_names, residuals_before,
                     loss_before, original_params, optimized_x,
                     converged, iterations, message, method_name):
    """Apply optimized values and build IdentificationResult with rollback guard."""
    optimized = {name: float(val) for name, val in zip(free_names, optimized_x)}
    set_model_parameters(model, optimized)

    residuals_after = compute_model_residuals(model, measurements)
    loss_after = _mse(residuals_after)

    typical_err_before = _typical_error_pct(residuals_before, measurements)
    typical_err_after = _typical_error_pct(residuals_after, measurements)

    # Rollback guard: don't accept if typical-workload error got worse
    if typical_err_after > typical_err_before and typical_err_after > 5.0:
        set_model_parameters(model, original_params)
        final_params = get_model_parameters(model)
        corrections = {k: v for k, v in final_params.items() if k.startswith("cor.")}
        return IdentificationResult(
            corrections=corrections,
            loss_before=loss_before,
            loss_after=loss_before,
            residuals_before=residuals_before,
            residuals_after=residuals_before,
            converged=False,
            iterations=iterations,
            cpi_error_percent=typical_err_before,
            message="Rolled back: optimization worsened typical-workload error",
            free_parameters=free_names,
            method=method_name,
        )

    final_params = get_model_parameters(model)
    corrections = {k: v for k, v in final_params.items() if k.startswith("cor.")}

    return IdentificationResult(
        corrections=corrections,
        loss_before=loss_before,
        loss_after=loss_after,
        residuals_before=residuals_before,
        residuals_after=residuals_after,
        converged=converged,
        iterations=iterations,
        cpi_error_percent=typical_err_after,
        message=message,
        free_parameters=free_names,
        method=method_name,
    )


# ---------------------------------------------------------------------------
# Method 1: Ridge (Regularized Least Squares) — DEFAULT
# ---------------------------------------------------------------------------

def _identify_ridge(
    model,
    measurements: Dict[str, float],
    setup,
    *,
    alpha: float = 0.01,
    max_iterations: int = 200,
    ftol: float = 1e-10,
    xtol: float = 1e-10,
    gtol: float = 1e-10,
    verbose: int = 0,
) -> IdentificationResult:
    """Regularized least-squares identification (L2 / Ridge penalty).

    Minimizes:  ||W(predicted - measured)||² + α||corrections||²

    The regularization term α||corrections||² penalizes large correction
    values, which:
    - Produces unique solutions for underdetermined systems
    - Prefers smaller corrections (Occam's razor)
    - Prevents corrections from pinning at bounds
    - Improves numerical stability

    Args:
        alpha: Regularization strength. Higher = smaller corrections.
               0.01 is a good default. Set to 0.0 to disable (plain LS).
    """
    from scipy.optimize import least_squares

    (free_names, x0, lb, ub, workload_order, norm_weights,
     residuals_before, loss_before, original_params) = setup

    n_workloads = len(workload_order)
    n_params = len(free_names)

    # Scale alpha by the ratio of params to workloads — auto-regularize
    # underdetermined systems more strongly
    if n_workloads > 0 and n_params > n_workloads:
        effective_alpha = alpha * (n_params / n_workloads)
    else:
        effective_alpha = alpha

    # Regularization weights: scale by bound range so all corrections
    # are penalized equally relative to their feasible range
    reg_weights = np.zeros(n_params)
    for i, name in enumerate(free_names):
        bound_range = ub[i] - lb[i]
        if bound_range > 0:
            reg_weights[i] = effective_alpha / bound_range
        else:
            reg_weights[i] = effective_alpha

    def objective(x):
        update = {name: float(val) for name, val in zip(free_names, x)}
        set_model_parameters(model, update)
        residuals = compute_model_residuals(model, measurements)
        residual_vals = [residuals.get(w, 0.0) for w in workload_order]
        # Normalized residuals + regularization pseudo-residuals
        data_part = np.array(residual_vals, dtype=np.float64) * norm_weights
        reg_part = x * reg_weights
        return np.concatenate([data_part, reg_part])

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

    converged = result.status > 0
    return _finalize_result(
        model, measurements, free_names, residuals_before, loss_before,
        original_params, result.x, converged, result.nfev, result.message,
        "ridge",
    )


# ---------------------------------------------------------------------------
# Method 2: Differential Evolution (Global Optimizer)
# ---------------------------------------------------------------------------

def _identify_de(
    model,
    measurements: Dict[str, float],
    setup,
    *,
    max_iterations: int = 1000,
    popsize: int = 15,
    tol: float = 1e-8,
    seed: int = 42,
    verbose: int = 0,
) -> IdentificationResult:
    """Global optimization via differential evolution.

    Searches the full feasible region using a population-based stochastic
    optimizer. Better than local methods when:
    - Corrections are pinned at bounds (local optimizer can't escape)
    - Loss surface has multiple local minima
    - The initial point is far from the optimum

    Slower than Ridge but more robust for difficult cases.

    Args:
        max_iterations: Maximum generations.
        popsize: Population size multiplier (total pop = popsize × n_params).
        tol: Convergence tolerance on the loss function.
        seed: Random seed for reproducibility.
    """
    from scipy.optimize import differential_evolution

    (free_names, x0, lb, ub, workload_order, norm_weights,
     residuals_before, loss_before, original_params) = setup

    bounds_list = list(zip(lb, ub))

    def objective(x):
        update = {name: float(val) for name, val in zip(free_names, x)}
        set_model_parameters(model, update)
        residuals = compute_model_residuals(model, measurements)
        residual_vals = [residuals.get(w, 0.0) for w in workload_order]
        weighted = np.array(residual_vals, dtype=np.float64) * norm_weights
        return float(np.sum(weighted ** 2))

    result = differential_evolution(
        objective,
        bounds=bounds_list,
        x0=x0,
        maxiter=max_iterations,
        popsize=popsize,
        tol=tol,
        seed=seed,
        polish=True,  # local refinement after global search
    )

    converged = result.success
    return _finalize_result(
        model, measurements, free_names, residuals_before, loss_before,
        original_params, result.x, converged, result.nfev, result.message,
        "differential_evolution",
    )


# ---------------------------------------------------------------------------
# Method 3: Bayesian Optimization
# ---------------------------------------------------------------------------

def _identify_bayesian(
    model,
    measurements: Dict[str, float],
    setup,
    *,
    n_calls: int = 100,
    n_initial_points: int = 20,
    seed: int = 42,
    verbose: int = 0,
) -> IdentificationResult:
    """Bayesian optimization via Gaussian process surrogate.

    Builds a probabilistic model (Gaussian process) of the loss surface
    and uses an acquisition function (Expected Improvement) to decide
    where to sample next. Advantages:
    - Sample-efficient: needs fewer evaluations than DE
    - Provides uncertainty estimates on the optimum
    - Good for expensive objective functions
    - Naturally handles noise in measurements

    Requires: pip install scikit-optimize

    Args:
        n_calls: Total number of objective evaluations.
        n_initial_points: Random evaluations before GP model kicks in.
        seed: Random seed for reproducibility.
    """
    try:
        from skopt import gp_minimize
        from skopt.space import Real
    except ImportError:
        raise ImportError(
            "Bayesian optimization requires scikit-optimize. "
            "Install with: pip install scikit-optimize"
        )

    (free_names, x0, lb, ub, workload_order, norm_weights,
     residuals_before, loss_before, original_params) = setup

    dimensions = [Real(float(lo), float(hi), name=name)
                  for name, lo, hi in zip(free_names, lb, ub)]

    def objective(x):
        update = {name: float(val) for name, val in zip(free_names, x)}
        set_model_parameters(model, update)
        residuals = compute_model_residuals(model, measurements)
        residual_vals = [residuals.get(w, 0.0) for w in workload_order]
        weighted = np.array(residual_vals, dtype=np.float64) * norm_weights
        return float(np.sum(weighted ** 2))

    result = gp_minimize(
        objective,
        dimensions,
        x0=x0.tolist(),
        n_calls=n_calls,
        n_initial_points=n_initial_points,
        random_state=seed,
        verbose=verbose > 0,
    )

    converged = True  # GP minimize always completes
    return _finalize_result(
        model, measurements, free_names, residuals_before, loss_before,
        original_params, np.array(result.x), converged,
        len(result.func_vals),
        f"Bayesian opt: best loss={result.fun:.6f}",
        "bayesian",
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def identify_model(
    model,
    measurements: Dict[str, float],
    *,
    method: str = "ridge",
    max_iterations: int = 200,
    alpha: float = 0.01,
    ftol: float = 1e-10,
    xtol: float = 1e-10,
    gtol: float = 1e-10,
    verbose: int = 0,
    **kwargs,
) -> IdentificationResult:
    """Run system identification on a processor model.

    Only ``cor.*`` (correction) parameters are free. All ``cat.*`` (instruction
    category cycle counts) are kept fixed at their datasheet values.

    Args:
        model: Any processor model object with analyze(), get_parameters(), etc.
        measurements: Dict mapping workload name → measured CPI.
        method: Optimization method. One of:
            - 'ridge' (default): Regularized least-squares (L2 penalty).
              Best for most models. Fast, handles underdetermined systems.
            - 'de' or 'differential_evolution': Global optimizer.
              Use for models stuck at bounds or with high error.
            - 'bayesian': Bayesian optimization via Gaussian process.
              Sample-efficient, provides uncertainty. Requires scikit-optimize.
            - 'trf': Plain trust-region-reflective (no regularization).
              Legacy method, equivalent to ridge with alpha=0.
        max_iterations: Maximum optimizer iterations/evaluations.
        alpha: Regularization strength for 'ridge' method (default 0.01).
               Higher values produce smaller corrections.
        ftol: Function tolerance (ridge/trf only).
        xtol: Parameter tolerance (ridge/trf only).
        gtol: Gradient tolerance (ridge/trf only).
        verbose: Verbosity level (0=silent).
        **kwargs: Additional keyword arguments passed to the chosen method.

    Returns:
        IdentificationResult with optimized corrections and diagnostics.
    """
    # Common setup
    setup = _setup_identification(model, measurements)
    if setup is None:
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
            method=method,
        )

    # Dispatch to chosen method
    method_lower = method.lower().replace("-", "_")

    if method_lower == "ridge":
        return _identify_ridge(
            model, measurements, setup,
            alpha=alpha,
            max_iterations=max_iterations,
            ftol=ftol, xtol=xtol, gtol=gtol,
            verbose=verbose,
        )
    elif method_lower in ("de", "differential_evolution"):
        return _identify_de(
            model, measurements, setup,
            max_iterations=kwargs.get("de_max_iterations", 1000),
            popsize=kwargs.get("popsize", 15),
            tol=kwargs.get("tol", 1e-8),
            seed=kwargs.get("seed", 42),
            verbose=verbose,
        )
    elif method_lower == "bayesian":
        return _identify_bayesian(
            model, measurements, setup,
            n_calls=kwargs.get("n_calls", 100),
            n_initial_points=kwargs.get("n_initial_points", 20),
            seed=kwargs.get("seed", 42),
            verbose=verbose,
        )
    elif method_lower == "trf":
        # Legacy: plain least-squares without regularization
        return _identify_ridge(
            model, measurements, setup,
            alpha=0.0,
            max_iterations=max_iterations,
            ftol=ftol, xtol=xtol, gtol=gtol,
            verbose=verbose,
        )
    else:
        raise ValueError(
            f"Unknown method '{method}'. "
            f"Choose from: 'ridge', 'de', 'bayesian', 'trf'"
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
