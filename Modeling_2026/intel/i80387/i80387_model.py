#!/usr/bin/env python3
"""
Intel 80387 Performance Model

Grey-box queueing model for the Intel 80387 microprocessor (1987).

Specifications:
- Clock: 16.0 MHz
- Bus Width: 32-bit
- Transistors: 104,000

Source: Intel 80387 Programmers Reference
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from common.queueing import QueueingModel
from common.validation import create_standard_suite


# Processor configuration
CONFIG = {
    'name': 'Intel 80387',
    'year': 1987,
    'clock_mhz': 16.0,
    'bus_width': 32,
    'transistors': 104000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'fld': {
        'cycles': 20,
        'weight': 0.2,
        'description': 'FLD (load)',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fst': {
        'cycles': 25,
        'weight': 0.15,
        'description': 'FST (store)',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fadd': {
        'cycles': 30,
        'weight': 0.2,
        'description': 'FADD',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fsub': {
        'cycles': 30,
        'weight': 0.1,
        'description': 'FSUB',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fmul': {
        'cycles': 50,
        'weight': 0.15,
        'description': 'FMUL',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fdiv': {
        'cycles': 90,
        'weight': 0.1,
        'description': 'FDIV',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fsqrt': {
        'cycles': 120,
        'weight': 0.05,
        'description': 'FSQRT',
        'source': 'Intel 80387 Programmers Reference'
    },
    'fcomp': {
        'cycles': 25,
        'weight': 0.05,
        'description': 'FCOMP',
        'source': 'Intel 80387 Programmers Reference'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 150000,
    'ips_max': 500000,
    'cpi_min': 30,
    'cpi_max': 120,
    'expected_bottlenecks': ['execute', 'fpu'],
    'source': 'Intel 80387 Programmers Reference'
}

# Create the queueing model
MODEL = QueueingModel(
    clock_mhz=CONFIG['clock_mhz'],
    timing_categories=TIMING_CATEGORIES,
    bus_width=CONFIG['bus_width']
)


def analyze(workload='typical'):
    """Analyze processor performance with given workload."""
    return MODEL.analyze(workload)


def validate():
    """Run validation suite."""
    result = analyze('typical')
    suite = create_standard_suite(
        CONFIG['name'],
        (VALIDATION_TARGETS['ips_min'], VALIDATION_TARGETS['ips_max']),
        (VALIDATION_TARGETS['cpi_min'], VALIDATION_TARGETS['cpi_max']),
        VALIDATION_TARGETS['expected_bottlenecks'],
        TIMING_CATEGORIES,
        [VALIDATION_TARGETS['source']],
        result.ips,
        result.cpi,
        result.bottleneck
    )
    return suite


def main():
    """Main entry point."""
    print(f"{CONFIG['name']} Performance Model")
    print("=" * 50)
    print(f"Clock: {CONFIG['clock_mhz']} MHz")
    print(f"Bus: {CONFIG['bus_width']}-bit")
    print(f"Transistors: {CONFIG['transistors']:,}")
    print()
    
    # Analyze with typical workload
    result = analyze('typical')
    print(f"IPS: {result.ips:,.0f}")
    print(f"CPI: {result.cpi:.2f}")
    print(f"Bottleneck: {result.bottleneck}")
    print()
    
    # Run validation
    suite = validate()
    results, all_passed = suite.run()
    print(suite.summary())


if __name__ == '__main__':
    main()
