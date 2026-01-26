#!/usr/bin/env python3
"""
Intel 80287 Performance Model

Grey-box queueing model for the Intel 80287 microprocessor (1982).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 16-bit
- Transistors: 45,000

Source: Intel 80287 Programmers Reference
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
    'name': 'Intel 80287',
    'year': 1982,
    'clock_mhz': 8.0,
    'bus_width': 16,
    'transistors': 45000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'fld': {
        'cycles': 40,
        'weight': 0.2,
        'description': 'FLD (load)',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fst': {
        'cycles': 50,
        'weight': 0.15,
        'description': 'FST (store)',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fadd': {
        'cycles': 90,
        'weight': 0.2,
        'description': 'FADD',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fsub': {
        'cycles': 90,
        'weight': 0.1,
        'description': 'FSUB',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fmul': {
        'cycles': 140,
        'weight': 0.15,
        'description': 'FMUL',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fdiv': {
        'cycles': 200,
        'weight': 0.1,
        'description': 'FDIV',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fsqrt': {
        'cycles': 180,
        'weight': 0.05,
        'description': 'FSQRT',
        'source': 'Intel 80287 Programmers Reference'
    },
    'fcomp': {
        'cycles': 50,
        'weight': 0.05,
        'description': 'FCOMP',
        'source': 'Intel 80287 Programmers Reference'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 50000,
    'ips_max': 150000,
    'cpi_min': 50,
    'cpi_max': 200,
    'expected_bottlenecks': ['execute', 'fpu'],
    'source': 'Intel 80287 Programmers Reference'
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
