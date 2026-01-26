"""Standard Workload Profiles for Microprocessor Performance Models.

This module defines standard workload profiles representing different
instruction mixes for benchmarking and analysis.
"""

from typing import Dict, List, Optional

# Standard workload profiles with generic category names
STANDARD_WORKLOADS = {
    'typical': {
        'register_ops': 0.25,
        'alu_register': 0.20,
        'memory_load': 0.15,
        'memory_store': 0.10,
        'branch_taken': 0.10,
        'branch_not_taken': 0.05,
        'immediate': 0.08,
        'call_return': 0.05,
        'stack_ops': 0.02
    },
    'compute': {
        'register_ops': 0.15,
        'alu_register': 0.40,
        'memory_load': 0.10,
        'memory_store': 0.05,
        'branch_taken': 0.12,
        'branch_not_taken': 0.08,
        'immediate': 0.05,
        'call_return': 0.03,
        'stack_ops': 0.02
    },
    'memory': {
        'register_ops': 0.10,
        'alu_register': 0.10,
        'memory_load': 0.30,
        'memory_store': 0.25,
        'branch_taken': 0.08,
        'branch_not_taken': 0.05,
        'immediate': 0.05,
        'call_return': 0.05,
        'stack_ops': 0.02
    },
    'control': {
        'register_ops': 0.15,
        'alu_register': 0.10,
        'memory_load': 0.10,
        'memory_store': 0.05,
        'branch_taken': 0.25,
        'branch_not_taken': 0.15,
        'immediate': 0.05,
        'call_return': 0.10,
        'stack_ops': 0.05
    },
    'gibson_mix': {
        # Gibson mix (1970) - early scientific computing
        'register_ops': 0.30,
        'alu_register': 0.25,
        'memory_load': 0.18,
        'memory_store': 0.08,
        'branch_taken': 0.07,
        'branch_not_taken': 0.04,
        'immediate': 0.05,
        'call_return': 0.02,
        'stack_ops': 0.01
    },
    'sieve': {
        # Sieve of Eratosthenes benchmark pattern
        'register_ops': 0.20,
        'alu_register': 0.15,
        'memory_load': 0.25,
        'memory_store': 0.15,
        'branch_taken': 0.10,
        'branch_not_taken': 0.05,
        'immediate': 0.05,
        'call_return': 0.03,
        'stack_ops': 0.02
    },
    'dhrystone': {
        # Dhrystone benchmark pattern
        'register_ops': 0.22,
        'alu_register': 0.18,
        'memory_load': 0.16,
        'memory_store': 0.10,
        'branch_taken': 0.12,
        'branch_not_taken': 0.07,
        'immediate': 0.06,
        'call_return': 0.06,
        'stack_ops': 0.03
    },
    'embedded': {
        # Embedded systems workload (MCU-focused)
        'register_ops': 0.20,
        'alu_register': 0.15,
        'memory_load': 0.12,
        'memory_store': 0.08,
        'branch_taken': 0.15,
        'branch_not_taken': 0.10,
        'immediate': 0.10,
        'call_return': 0.05,
        'io_ops': 0.05
    }
}

# Era-specific workloads
ERA_WORKLOADS = {
    '4bit_early': {
        # 1971-1975: 4004, 4040 era
        'register_ops': 0.30,
        'accumulator_imm': 0.15,
        'memory_ops': 0.20,
        'bcd_arithmetic': 0.15,
        'jump_unconditional': 0.08,
        'jump_conditional': 0.07,
        'subroutine': 0.03,
        'io_ops': 0.02
    },
    '8bit_home': {
        # 1975-1985: 6502, Z80 home computer era
        'register_ops': 0.22,
        'alu_ops': 0.18,
        'zeropage_load': 0.12,
        'zeropage_store': 0.08,
        'absolute_load': 0.10,
        'absolute_store': 0.06,
        'branch_ops': 0.12,
        'jump_ops': 0.05,
        'stack_ops': 0.04,
        'index_ops': 0.03
    },
    '16bit_business': {
        # 1978-1985: 8086, 68000 business computing
        'register_ops': 0.20,
        'alu_ops': 0.18,
        'memory_load': 0.14,
        'memory_store': 0.10,
        'string_ops': 0.08,
        'branch_ops': 0.12,
        'call_return': 0.08,
        'stack_ops': 0.05,
        'immediate': 0.05
    },
    '32bit_workstation': {
        # 1984+: 68020, 80386 workstation era
        'register_ops': 0.18,
        'alu_ops': 0.20,
        'memory_load': 0.15,
        'memory_store': 0.10,
        'branch_ops': 0.12,
        'call_return': 0.10,
        'stack_ops': 0.05,
        'multiply_divide': 0.05,
        'immediate': 0.05
    }
}


def get_workload(name: str) -> Dict[str, float]:
    """Get a workload profile by name.
    
    Args:
        name: Workload name (e.g., 'typical', 'compute', 'sieve')
        
    Returns:
        Dict of category -> weight
        
    Raises:
        KeyError: If workload name not found
    """
    if name in STANDARD_WORKLOADS:
        return STANDARD_WORKLOADS[name].copy()
    if name in ERA_WORKLOADS:
        return ERA_WORKLOADS[name].copy()
    raise KeyError(f"Unknown workload: {name}")


def normalize_weights(workload: Dict[str, float]) -> Dict[str, float]:
    """Normalize workload weights to sum to 1.0.
    
    Args:
        workload: Dict of category -> weight
        
    Returns:
        Normalized workload dict
    """
    total = sum(workload.values())
    if total == 0:
        return workload.copy()
    return {k: v / total for k, v in workload.items()}


def map_workload_to_categories(
    workload: Dict[str, float],
    category_mapping: Dict[str, str]
) -> Dict[str, float]:
    """Map generic workload categories to processor-specific categories.
    
    Args:
        workload: Generic workload dict
        category_mapping: Dict mapping generic -> processor-specific
        
    Returns:
        Workload with processor-specific categories
    """
    result = {}
    for generic, weight in workload.items():
        specific = category_mapping.get(generic, generic)
        result[specific] = result.get(specific, 0) + weight
    return normalize_weights(result)


def blend_workloads(
    workloads: List[Dict[str, float]],
    weights: List[float]
) -> Dict[str, float]:
    """Blend multiple workloads with given weights.
    
    Args:
        workloads: List of workload dicts
        weights: Blending weights (should sum to 1.0)
        
    Returns:
        Blended workload dict
    """
    if len(workloads) != len(weights):
        raise ValueError("Number of workloads must match number of weights")
    
    result = {}
    for workload, blend_weight in zip(workloads, weights):
        for cat, cat_weight in workload.items():
            result[cat] = result.get(cat, 0) + cat_weight * blend_weight
    
    return normalize_weights(result)


def create_custom_workload(**kwargs) -> Dict[str, float]:
    """Create a custom workload from keyword arguments.
    
    Args:
        **kwargs: Category names and weights
        
    Returns:
        Normalized workload dict
        
    Example:
        workload = create_custom_workload(
            alu=0.4, memory=0.3, branch=0.2, other=0.1
        )
    """
    return normalize_weights(kwargs)


def get_workload_for_processor(
    base_workload: str,
    timing_categories: Dict[str, Dict]
) -> Dict[str, float]:
    """Get a workload adapted to processor's timing categories.
    
    If the processor's categories don't match the standard workload categories,
    this function uses the processor's own default weights.
    
    Args:
        base_workload: Name of base workload ('typical', 'compute', etc.)
        timing_categories: Processor's timing categories dict
        
    Returns:
        Workload dict compatible with processor's categories
    """
    # Get processor's category names and default weights
    proc_categories = set(timing_categories.keys())
    proc_workload = {
        cat: data.get('weight', 1.0 / len(timing_categories))
        for cat, data in timing_categories.items()
    }
    
    # Try to get standard workload
    try:
        std_workload = get_workload(base_workload)
        std_categories = set(std_workload.keys())
        
        # If good overlap, map and blend
        overlap = proc_categories & std_categories
        if len(overlap) >= 3:
            # Map matching categories
            result = {}
            for cat in proc_categories:
                if cat in std_workload:
                    result[cat] = std_workload[cat]
                else:
                    result[cat] = proc_workload[cat]
            return normalize_weights(result)
    except KeyError:
        pass
    
    # Fall back to processor's default weights
    return normalize_weights(proc_workload)
