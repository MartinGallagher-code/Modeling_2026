#!/usr/bin/env python3
"""
National IMP-16 Performance Model

Grey-box queueing model for the National IMP-16 microprocessor (1973).

Specifications:
- Clock: 0.5 MHz
- Bus Width: 16-bit
- Transistors: ~6,000 (bit-slice based)

Source: National IMP-16 Users Manual
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
    'name': 'National IMP-16',
    'year': 1973,
    'clock_mhz': 0.5,
    'bus_width': 16,
    'transistors': 6000
}

# Timing categories (5-15 categories capturing major instruction classes)
# Target CPI ~8.0 for early bit-slice architecture
TIMING_CATEGORIES = {
    'register': {
        'cycles': 6,
        'weight': 0.20,
        'description': 'Register-register',
        'source': 'National IMP-16 Users Manual'
    },
    'immediate': {
        'cycles': 8,
        'weight': 0.15,
        'description': 'Immediate operand',
        'source': 'National IMP-16 Users Manual'
    },
    'memory': {
        'cycles': 10,
        'weight': 0.20,
        'description': 'Memory operations',
        'source': 'National IMP-16 Users Manual'
    },
    'indexed': {
        'cycles': 12,
        'weight': 0.10,
        'description': 'Indexed addressing',
        'source': 'National IMP-16 Users Manual'
    },
    'branch': {
        'cycles': 6,
        'weight': 0.15,
        'description': 'Branch instructions',
        'source': 'National IMP-16 Users Manual'
    },
    'jump': {
        'cycles': 8,
        'weight': 0.08,
        'description': 'Jump/subroutine',
        'source': 'National IMP-16 Users Manual'
    },
    'shift': {
        'cycles': 10,
        'weight': 0.07,
        'description': 'Shift operations',
        'source': 'National IMP-16 Users Manual'
    },
    'io': {
        'cycles': 12,
        'weight': 0.05,
        'description': 'I/O operations',
        'source': 'National IMP-16 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 50000,
    'ips_max': 100000,
    'cpi_min': 6,
    'cpi_max': 12,
    'expected_bottlenecks': ['memory', 'bit_slice'],
    'source': 'National IMP-16 Users Manual'
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
