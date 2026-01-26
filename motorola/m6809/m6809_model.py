#!/usr/bin/env python3
"""
Motorola 6809 Performance Model

Grey-box queueing model for the Motorola 6809 microprocessor (1978).

Specifications:
- Clock: 1.0 MHz
- Bus Width: 8-bit
- Transistors: 9,000

Source: Motorola MC6809 Programming Manual
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
    'name': 'Motorola 6809',
    'year': 1978,
    'clock_mhz': 1.0,
    'bus_width': 8,
    'transistors': 9000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'inherent': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Inherent',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'immediate': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'direct': {
        'cycles': 4,
        'weight': 0.18,
        'description': 'Direct',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'indexed': {
        'cycles': 5,
        'weight': 0.15,
        'description': 'Indexed',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'extended': {
        'cycles': 5,
        'weight': 0.1,
        'description': 'Extended',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'branch_short': {
        'cycles': 3,
        'weight': 0.08,
        'description': 'Short branch',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'branch_long': {
        'cycles': 5,
        'weight': 0.05,
        'description': 'Long branch',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'jsr_rts': {
        'cycles': 7,
        'weight': 0.05,
        'description': 'JSR, RTS',
        'source': 'Motorola MC6809 Programming Manual'
    },
    'multiply': {
        'cycles': 11,
        'weight': 0.03,
        'description': 'MUL',
        'source': 'Motorola MC6809 Programming Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 250000,
    'ips_max': 600000,
    'cpi_min': 2,
    'cpi_max': 8,
    'expected_bottlenecks': ['memory', 'fetch'],
    'source': 'Motorola MC6809 Programming Manual'
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
