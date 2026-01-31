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

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
import math


@dataclass
class CacheConfig:
    """Memory hierarchy configuration for cache miss modeling.

    Used by post-1985 processors with on-chip or external caches.
    Pre-1985 processors leave cache_config as None.
    """
    has_cache: bool = False
    l1_latency: float = 1.0        # cycles for L1 hit
    l1_hit_rate: float = 0.95      # L1 hit probability
    l2_latency: float = 10.0       # cycles for L2 hit
    l2_hit_rate: float = 0.90      # L2 hit probability (given L1 miss)
    has_l2: bool = False            # whether L2 cache exists
    dram_latency: float = 50.0     # cycles for main memory access

    def effective_memory_penalty(self) -> float:
        """Compute average additional cycles beyond L1 hit for memory ops."""
        if not self.has_cache:
            return 0.0

        l1_miss_rate = 1.0 - self.l1_hit_rate

        if self.has_l2:
            # L1 miss -> check L2
            l2_miss_rate = 1.0 - self.l2_hit_rate
            penalty = l1_miss_rate * (
                self.l2_hit_rate * (self.l2_latency - self.l1_latency) +
                l2_miss_rate * (self.dram_latency - self.l1_latency)
            )
        else:
            # L1 miss -> go to DRAM
            penalty = l1_miss_rate * (self.dram_latency - self.l1_latency)

        return penalty


@dataclass
class BranchPredictionConfig:
    """Branch prediction configuration for pipeline-aware branch cost modeling.

    Models branch cost as:
        effective_branch_cycles =
            predict_accuracy * taken_cycles +
            (1 - predict_accuracy) * (taken_cycles + flush_penalty)

    where flush_penalty ~ pipeline_depth (cycles to refill after misprediction).

    Predictor types by era:
        - No prediction (pre-1985): accuracy=0, always pay full penalty
        - Static predict not-taken (i486): accuracy ~0.60-0.70
        - BTB (Pentium): accuracy ~0.80-0.85
        - 2-level adaptive (PPC604, R10000): accuracy ~0.90-0.93
        - Per-address history (Alpha 21264): accuracy ~0.95+
    """
    has_branch_prediction: bool = False
    predict_accuracy: float = 0.80       # fraction of branches correctly predicted
    pipeline_depth: int = 5              # stages; determines flush penalty
    btb_hit_rate: float = 0.90           # BTB hit rate (for BTB-based predictors)
    taken_cycles: float = 1.0            # cycles for correctly predicted taken branch

    def effective_branch_penalty(self) -> float:
        """Compute average branch cost in cycles.

        Returns the expected cycles per branch instruction, accounting for
        prediction accuracy and pipeline flush cost on misprediction.
        """
        if not self.has_branch_prediction:
            return 0.0  # no prediction = use base_cycles as-is

        flush_penalty = float(self.pipeline_depth)
        correct_cost = self.taken_cycles
        mispredict_cost = self.taken_cycles + flush_penalty
        return (self.predict_accuracy * correct_cost +
                (1.0 - self.predict_accuracy) * mispredict_cost)


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
    cache_miss_cpi: float = 0.0    # CPI contribution from cache miss penalties

    @classmethod
    def from_cpi(cls, processor: str, workload: str, cpi: float,
                 clock_mhz: float, bottleneck: str,
                 utilizations: Dict[str, float] = None,
                 base_cpi: float = None, correction_delta: float = 0.0,
                 cache_miss_cpi: float = 0.0):
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
            correction_delta=correction_delta,
            cache_miss_cpi=cache_miss_cpi,
        )


class BaseProcessorModel:
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
    
    def analyze(self, workload: str = 'typical') -> AnalysisResult:
        """
        Analyze processor performance for a given workload.

        Default implementation computes CPI as a weighted sum of instruction
        category cycles (with cache miss penalties applied to memory categories)
        plus per-category correction terms fitted by system identification.

        Subclasses may override for processor-specific behavior.

        Args:
            workload: Name of workload profile ('typical', 'compute', 'memory', 'control')

        Returns:
            AnalysisResult with IPC, CPI, IPS, and bottleneck information
        """
        categories = self._get_categories_dict()
        profiles = self._get_profiles_dict()
        profile = profiles.get(workload, profiles.get('typical'))
        if profile is None:
            profile = next(iter(profiles.values()))

        # Apply cache miss penalty to memory-accessing categories
        cache_miss_cpi = self._apply_cache_penalty(categories, profile)

        # Apply branch prediction model to branch categories
        self._apply_branch_prediction(categories, profile)

        # Compute base CPI as weighted sum of category cycles
        base_cpi = 0.0
        contributions = {}
        for cat_name, weight in profile.category_weights.items():
            cat = categories.get(cat_name)
            if cat is not None:
                contrib = weight * cat.total_cycles
                base_cpi += contrib
                contributions[cat_name] = contrib

        # Apply correction terms
        corrections = getattr(self, 'corrections', {})
        correction_delta = sum(
            corrections.get(cat_name, 0.0) * weight
            for cat_name, weight in profile.category_weights.items()
        )
        corrected_cpi = base_cpi + correction_delta

        # Identify bottleneck
        bottleneck = max(contributions, key=contributions.get) if contributions else "unknown"

        return AnalysisResult.from_cpi(
            processor=self.name,
            workload=workload,
            cpi=corrected_cpi,
            clock_mhz=self.clock_mhz,
            bottleneck=bottleneck,
            utilizations=contributions,
            base_cpi=base_cpi,
            correction_delta=correction_delta,
            cache_miss_cpi=cache_miss_cpi,
        )

    def _get_categories_dict(self) -> Dict[str, InstructionCategory]:
        """Get instruction categories dict (handles both naming conventions)."""
        return getattr(self, 'instruction_categories',
                       getattr(self, '_instruction_categories', {}))

    def _get_profiles_dict(self) -> Dict[str, WorkloadProfile]:
        """Get workload profiles dict (handles both naming conventions)."""
        return getattr(self, 'workload_profiles',
                       getattr(self, '_workload_profiles', {}))

    def _apply_cache_penalty(self, categories: Dict[str, InstructionCategory],
                             profile: WorkloadProfile) -> float:
        """Apply cache miss penalty to memory-accessing instruction categories.

        Sets memory_cycles on each memory category based on the cache hierarchy.
        Returns the total CPI contribution from cache misses (for decomposition).

        Args:
            categories: Instruction category dict
            profile: Current workload profile

        Returns:
            Cache miss CPI contribution (sum of penalty * weight for memory categories)
        """
        cache_config = getattr(self, 'cache_config', None)
        if cache_config is None or not getattr(cache_config, 'has_cache', False):
            return 0.0

        penalty = cache_config.effective_memory_penalty()
        if penalty <= 0.0:
            return 0.0

        memory_cats = getattr(self, 'memory_categories', [])
        cache_miss_cpi = 0.0
        for cat_name in memory_cats:
            if cat_name in categories:
                categories[cat_name].memory_cycles = penalty
                weight = profile.category_weights.get(cat_name, 0.0)
                cache_miss_cpi += penalty * weight

        return cache_miss_cpi

    def _apply_branch_prediction(self, categories: Dict[str, InstructionCategory],
                                  profile: WorkloadProfile) -> float:
        """Apply branch prediction model to branch instruction categories.

        Replaces the branch category's base_cycles with the expected cost
        accounting for prediction accuracy and pipeline flush penalty.
        Returns the CPI change from branch prediction modeling.

        Args:
            categories: Instruction category dict
            profile: Current workload profile

        Returns:
            Branch prediction CPI delta (positive = slower, negative = faster than base)
        """
        bp_config = getattr(self, 'branch_prediction', None)
        if bp_config is None or not getattr(bp_config, 'has_branch_prediction', False):
            return 0.0

        effective_cost = bp_config.effective_branch_penalty()
        branch_cats = getattr(self, 'branch_categories', ['branch', 'control'])
        bp_delta = 0.0

        for cat_name in branch_cats:
            if cat_name in categories:
                old_cycles = categories[cat_name].base_cycles
                categories[cat_name].base_cycles = effective_cost
                weight = profile.category_weights.get(cat_name, 0.0)
                bp_delta += (effective_cost - old_cycles) * weight

        return bp_delta

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


def _get_branch_prediction(model) -> Optional['BranchPredictionConfig']:
    """Get branch prediction configuration from any model object."""
    return getattr(model, 'branch_prediction', None)


def _get_cache_config(model) -> Optional['CacheConfig']:
    """Get cache configuration from any model object."""
    return getattr(model, 'cache_config', None)


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

    cache = _get_cache_config(model)
    if cache is not None and cache.has_cache:
        params['cache.l1_hit_rate'] = cache.l1_hit_rate
        params['cache.l1_latency'] = cache.l1_latency
        params['cache.dram_latency'] = cache.dram_latency
        if cache.has_l2:
            params['cache.l2_hit_rate'] = cache.l2_hit_rate
            params['cache.l2_latency'] = cache.l2_latency

    bp = _get_branch_prediction(model)
    if bp is not None and bp.has_branch_prediction:
        params['bp.predict_accuracy'] = bp.predict_accuracy
        params['bp.pipeline_depth'] = float(bp.pipeline_depth)
        params['bp.btb_hit_rate'] = bp.btb_hit_rate
        params['bp.taken_cycles'] = bp.taken_cycles

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
        elif key.startswith('cache.'):
            cache = _get_cache_config(model)
            if cache is not None:
                field_name = key[6:]  # strip 'cache.'
                if hasattr(cache, field_name):
                    setattr(cache, field_name, value)
        elif key.startswith('bp.'):
            bp = _get_branch_prediction(model)
            if bp is not None:
                field_name = key[3:]  # strip 'bp.'
                if hasattr(bp, field_name):
                    if field_name == 'pipeline_depth':
                        setattr(bp, field_name, int(round(value)))
                    else:
                        setattr(bp, field_name, value)


def get_model_parameter_bounds(model) -> Dict[str, tuple]:
    """Get physically plausible (min, max) bounds for each parameter.

    Default bounds:
      base_cycles:   (max(1, 0.5x), 3x current)
      memory_cycles: (0, max(3x current, 10))
      corrections:   scaled to ±100% of the category's base_cycles
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
                limit = max(5.0, cat.base_cycles)
            else:
                limit = 5.0
            bounds[key] = (-limit, limit)
        elif key.startswith('cache.'):
            field_name = key[6:]
            if field_name == 'l1_hit_rate':
                bounds[key] = (0.80, 0.999)
            elif field_name == 'l2_hit_rate':
                bounds[key] = (0.70, 0.999)
            elif field_name == 'l1_latency':
                bounds[key] = (1.0, 5.0)
            elif field_name == 'l2_latency':
                bounds[key] = (5.0, 30.0)
            elif field_name == 'dram_latency':
                bounds[key] = (20.0, 200.0)
        elif key.startswith('bp.'):
            field_name = key[3:]
            if field_name == 'predict_accuracy':
                bounds[key] = (0.50, 0.99)
            elif field_name == 'pipeline_depth':
                bounds[key] = (3.0, 15.0)
            elif field_name == 'btb_hit_rate':
                bounds[key] = (0.60, 0.99)
            elif field_name == 'taken_cycles':
                bounds[key] = (1.0, 5.0)

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
        elif key.startswith('cache.'):
            field_name = key[6:]
            # Hit rates are free for identification; latencies are fixed from datasheets
            is_hit_rate = field_name.endswith('_hit_rate')
            metadata[key] = {
                'fixed': not is_hit_rate,
                'source': 'identification' if is_hit_rate else 'datasheet',
                'description': f'Cache parameter: {field_name}',
            }
        elif key.startswith('bp.'):
            field_name = key[3:]
            # predict_accuracy is free for identification; others are fixed
            is_accuracy = field_name == 'predict_accuracy'
            metadata[key] = {
                'fixed': not is_accuracy,
                'source': 'identification' if is_accuracy else 'datasheet',
                'description': f'Branch prediction: {field_name}',
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
