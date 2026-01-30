#!/usr/bin/env python3
"""
Base Model Classes for Modeling_2026
=====================================

Provides common interfaces and data classes for all processor models.

IMPORTANT: Field order in dataclasses must match how they're called!
WorkloadProfile is called as: WorkloadProfile(name, category_weights_dict, description)

Author: Grey-Box Performance Modeling Research
Date: January 2026
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import math


@dataclass
class InstructionCategory:
    """Represents an instruction category with timing information"""
    name: str
    base_cycles: float
    memory_cycles: float = 0.0
    description: str = ""
    frequency: float = 0.0  # Fraction of instructions in this category
    
    @property
    def total_cycles(self) -> float:
        return self.base_cycles + self.memory_cycles


@dataclass
class WorkloadProfile:
    """Represents a workload with instruction category weights
    
    IMPORTANT: Field order must match calling convention:
    WorkloadProfile('name', {'cat': weight, ...}, 'description')
    """
    name: str
    # category_weights MUST come before description to match calling code!
    category_weights: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    
    def validate(self) -> bool:
        """Check that weights sum to 1.0"""
        if not self.category_weights:
            return False
        total = sum(self.category_weights.values())
        return abs(total - 1.0) < 0.01


@dataclass
class AnalysisResult:
    """Results from model analysis"""
    processor: str
    workload: str
    ipc: float
    cpi: float
    ips: float
    bottleneck: str
    utilizations: Dict[str, float] = field(default_factory=dict)
    stage_details: Dict[str, Any] = field(default_factory=dict)
    base_cpi: float = 0.0          # Physics-only prediction (before corrections)
    correction_delta: float = 0.0   # Total correction applied: cpi = base_cpi + correction_delta

    @classmethod
    def from_cpi(cls, processor: str, workload: str, cpi: float,
                 clock_mhz: float, bottleneck: str,
                 utilizations: Dict[str, float] = None,
                 base_cpi: float = None, correction_delta: float = 0.0):
        """Create result from CPI value"""
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        ips = clock_mhz * 1e6 * ipc
        return cls(
            processor=processor,
            workload=workload,
            ipc=ipc,
            cpi=cpi,
            ips=ips,
            bottleneck=bottleneck,
            utilizations=utilizations or {},
            base_cpi=base_cpi if base_cpi is not None else cpi,
            correction_delta=correction_delta
        )


class BaseProcessorModel(ABC):
    """
    Abstract base class for all processor models.
    
    All processor models should inherit from this class and implement
    the required methods.
    """
    
    # Required class attributes (override in subclass)
    name: str = "Unknown"
    manufacturer: str = "Unknown"
    year: int = 0
    clock_mhz: float = 1.0
    transistor_count: int = 0
    
    def __init__(self):
        """Initialize the model - override in subclass if needed"""
        # Initialize mutable attributes in __init__, not as class attributes
        self._instruction_categories: Dict[str, InstructionCategory] = {}
        self._workload_profiles: Dict[str, WorkloadProfile] = {}
        # Per-category correction terms for system identification (initially zero)
        self.corrections: Dict[str, float] = {}
    
    @abstractmethod
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze processor performance for a given workload.
        
        Args:
            workload: Name of workload profile ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, IPS, and bottleneck information
        """
        pass
    
    def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known data.
        
        Returns:
            Dictionary with validation results including:
            - tests: List of test results
            - passed: Number of tests passed
            - total: Total number of tests
            - accuracy_percent: Overall accuracy
        """
        # Default implementation - override for actual validation
        return {
            "tests": [],
            "passed": 0,
            "total": 0,
            "accuracy_percent": None
        }
    
    def get_instruction_categories(self) -> Dict[str, InstructionCategory]:
        """
        Get all instruction categories with timing.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        return self._instruction_categories
    
    def get_workload_profiles(self) -> Dict[str, WorkloadProfile]:
        """
        Get all available workload profiles.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        return self._workload_profiles
    
    def get_corrections(self) -> Dict[str, float]:
        """Get current per-category correction terms"""
        return dict(self.corrections)

    def set_corrections(self, corrections: Dict[str, float]):
        """Set per-category correction terms"""
        self.corrections = dict(corrections)

    def compute_correction_delta(self, workload: str = 'typical') -> float:
        """Compute total correction delta for a workload's instruction mix"""
        profile = self._workload_profiles.get(workload)
        if not profile or not self.corrections:
            return 0.0
        return sum(
            self.corrections.get(cat, 0.0) * weight
            for cat, weight in profile.category_weights.items()
        )

    def get_parameters(self) -> Dict[str, float]:
        """Extract all tunable parameters as a flat dictionary.

        Keys use dotted notation:
          'cat.<name>.base_cycles'    — base cycle count for category
          'cat.<name>.memory_cycles'  — memory access cycles for category
          'cor.<name>'                — correction term for category

        Returns:
            Flat dict mapping parameter name to current value
        """
        return get_model_parameters(self)

    def set_parameters(self, params: Dict[str, float]):
        """Set tunable parameters from a flat dictionary.

        Args:
            params: Dict with keys matching get_parameters() output
        """
        set_model_parameters(self, params)

    def get_parameter_bounds(self) -> Dict[str, tuple]:
        """Get physically plausible (min, max) bounds for each parameter.

        Defaults:
          base_cycles:   (max(1, 0.5x), 3x current)
          memory_cycles: (0, max(3x current, 10))
          corrections:   (-5, +5)

        Returns:
            Dict mapping parameter name to (min, max) tuple
        """
        return get_model_parameter_bounds(self)

    def get_parameter_metadata(self) -> Dict[str, dict]:
        """Get metadata for each parameter: fixed/free status, source, description.

        Returns:
            Dict mapping parameter name to metadata dict with keys:
              'fixed': bool — True if known from datasheets, False if free for identification
              'source': str — 'datasheet' or 'identification'
              'description': str — human-readable description
        """
        return get_model_parameter_metadata(self)

    def compute_residuals(self, measurements: Dict[str, float]) -> Dict[str, float]:
        """Compute per-workload residuals: predicted CPI - measured CPI.

        This is the objective function for system identification. Positive
        residual means the model over-predicts.

        Args:
            measurements: Dict mapping workload name to measured CPI value.
                          Example: {'typical': 5.5, 'compute': 4.5}

        Returns:
            Dict mapping workload name to residual (predicted - measured)
        """
        return compute_model_residuals(self, measurements)

    def compute_loss(self, measurements: Dict[str, float],
                     loss_type: str = 'mse') -> float:
        """Compute scalar loss value for optimizer minimization.

        Args:
            measurements: Dict mapping workload name to measured CPI
            loss_type: 'mse' (mean squared error), 'mae' (mean absolute error),
                       or 'sse' (sum of squared errors)

        Returns:
            Scalar loss value
        """
        return compute_model_loss(self, measurements, loss_type)

    def summary(self) -> str:
        """Return a summary string for the processor"""
        return f"{self.name} ({self.manufacturer}, {self.year}) @ {self.clock_mhz} MHz"


# =============================================================================
# Standalone parameter functions — work with ANY model object
# =============================================================================
# These functions use getattr() so they work with models that don't inherit
# from BaseProcessorModel. Use these for the ~38 models that define their
# own classes without inheriting.

def _get_categories(model) -> Dict[str, 'InstructionCategory']:
    """Get instruction categories from any model object."""
    return getattr(model, 'instruction_categories',
                   getattr(model, '_instruction_categories', {}))


def _get_corrections(model) -> Dict[str, float]:
    """Get correction terms from any model object."""
    return getattr(model, 'corrections', {})


def get_model_parameters(model) -> Dict[str, float]:
    """Extract all tunable parameters from any model as a flat dict.

    Works with any model object that has instruction_categories and corrections
    attributes, regardless of whether it inherits from BaseProcessorModel.

    Keys use dotted notation:
      'cat.<name>.base_cycles'    — base cycle count for category
      'cat.<name>.memory_cycles'  — memory access cycles for category
      'cor.<name>'                — correction term for category

    Args:
        model: Any processor model object

    Returns:
        Flat dict mapping parameter name to current value
    """
    params = {}
    categories = _get_categories(model)
    for name, cat in categories.items():
        params[f'cat.{name}.base_cycles'] = cat.base_cycles
        params[f'cat.{name}.memory_cycles'] = cat.memory_cycles

    corrections = _get_corrections(model)
    for name, value in corrections.items():
        params[f'cor.{name}'] = value

    return params


def set_model_parameters(model, params: Dict[str, float]):
    """Set tunable parameters on any model from a flat dict.

    Args:
        model: Any processor model object
        params: Dict with keys matching get_model_parameters() output
    """
    categories = _get_categories(model)
    corrections = _get_corrections(model)

    for key, value in params.items():
        if key.startswith('cat.'):
            parts = key.split('.')
            if len(parts) == 3:
                cat_name, field_name = parts[1], parts[2]
                if cat_name in categories:
                    setattr(categories[cat_name], field_name, value)
        elif key.startswith('cor.'):
            cor_name = key[4:]
            corrections[cor_name] = value


def get_model_parameter_bounds(model) -> Dict[str, tuple]:
    """Get physically plausible (min, max) bounds for each parameter.

    Default bounds:
      base_cycles:   (max(1, 0.5x), 3x current)
      memory_cycles: (0, max(3x current, 10))
      corrections:   scaled to ±50% of the category's base_cycles
                     (min ±5.0 for low-cycle instructions)

    Correction bounds scale with base_cycles so that high-cycle categories
    (e.g. multiply @ 70, divide @ 140) can receive proportionally larger
    corrections, while low-cycle categories stay bounded.

    Args:
        model: Any processor model object

    Returns:
        Dict mapping parameter name to (min, max) tuple
    """
    params = get_model_parameters(model)
    categories = _get_categories(model)
    bounds = {}

    for key, value in params.items():
        if key.endswith('.base_cycles'):
            bounds[key] = (max(1.0, value * 0.5), max(value * 3.0, 3.0))
        elif key.endswith('.memory_cycles'):
            bounds[key] = (0.0, max(value * 3.0, 10.0))
        elif key.startswith('cor.'):
            # Scale correction bounds with the category's base cycles
            cat_name = key[4:]  # strip 'cor.' prefix
            cat = categories.get(cat_name)
            if cat is not None:
                half_base = cat.base_cycles * 0.5
                limit = max(5.0, half_base)
            else:
                limit = 5.0
            bounds[key] = (-limit, limit)

    return bounds


def get_model_parameter_metadata(model) -> Dict[str, dict]:
    """Get metadata for each parameter: fixed/free, source, description.

    Parameters from instruction categories are tagged as 'fixed' (known from
    datasheets). Correction terms are tagged as 'free' (to be identified).

    Args:
        model: Any processor model object

    Returns:
        Dict mapping parameter name to metadata dict
    """
    params = get_model_parameters(model)
    metadata = {}

    for key in params:
        if key.endswith('.base_cycles'):
            cat_name = key.split('.')[1]
            metadata[key] = {
                'fixed': True,
                'source': 'datasheet',
                'description': f'Base instruction cycles for {cat_name}',
            }
        elif key.endswith('.memory_cycles'):
            cat_name = key.split('.')[1]
            metadata[key] = {
                'fixed': True,
                'source': 'datasheet',
                'description': f'Memory access cycles for {cat_name}',
            }
        elif key.startswith('cor.'):
            cat_name = key[4:]
            metadata[key] = {
                'fixed': False,
                'source': 'identification',
                'description': f'Correction term for {cat_name}',
            }

    return metadata


# =============================================================================
# Standalone residual/loss functions — work with ANY model object
# =============================================================================

def compute_model_residuals(model, measurements: Dict[str, float]) -> Dict[str, float]:
    """Compute per-workload residuals: predicted CPI - measured CPI.

    Works with any model object that has an analyze() method.

    Args:
        model: Any processor model object with analyze(workload) method
        measurements: Dict mapping workload name to measured CPI value.
                      Example: {'typical': 5.5, 'compute': 4.5}

    Returns:
        Dict mapping workload name to residual (predicted - measured).
        Positive means model over-predicts.
    """
    residuals = {}
    for workload, measured_cpi in measurements.items():
        try:
            result = model.analyze(workload)
            residuals[workload] = result.cpi - measured_cpi
        except Exception:
            pass  # skip workloads the model doesn't support
    return residuals


def compute_model_loss(model, measurements: Dict[str, float],
                       loss_type: str = 'mse') -> float:
    """Compute scalar loss for optimizer minimization.

    Works with any model object that has an analyze() method.

    Args:
        model: Any processor model object
        measurements: Dict mapping workload name to measured CPI
        loss_type: Loss function type:
            'mse' — mean squared error (default, good for least_squares)
            'mae' — mean absolute error (robust to outliers)
            'sse' — sum of squared errors (for scipy.optimize)
            'rmse' — root mean squared error

    Returns:
        Scalar loss value. Returns inf if no valid residuals.
    """
    residuals = compute_model_residuals(model, measurements)
    if not residuals:
        return float('inf')

    values = list(residuals.values())
    n = len(values)

    if loss_type == 'sse':
        return sum(r ** 2 for r in values)
    elif loss_type == 'mse':
        return sum(r ** 2 for r in values) / n
    elif loss_type == 'rmse':
        return math.sqrt(sum(r ** 2 for r in values) / n)
    elif loss_type == 'mae':
        return sum(abs(r) for r in values) / n
    else:
        raise ValueError(f"Unknown loss_type: {loss_type!r}. Use 'mse', 'mae', 'sse', or 'rmse'.")


def compute_model_residual_vector(model, measurements: Dict[str, float]) -> Tuple[List[str], List[float]]:
    """Return residuals as ordered lists for scipy.optimize.least_squares.

    Args:
        model: Any processor model object
        measurements: Dict mapping workload name to measured CPI

    Returns:
        Tuple of (workload_names, residual_values) in consistent order.
        Use residual_values directly as the return from a least_squares cost function.
    """
    residuals = compute_model_residuals(model, measurements)
    names = sorted(residuals.keys())
    values = [residuals[n] for n in names]
    return names, values


# Convenience function for creating models
def create_model(family: str, processor: str):
    """
    Factory function to create a processor model.

    Args:
        family: Processor family ('intel', 'motorola', etc.)
        processor: Processor name ('i8086', 'm68000', etc.)

    Returns:
        Instantiated processor model
    """
    # This would be implemented with dynamic imports
    raise NotImplementedError("Use direct imports for now")
