#!/usr/bin/env python3
"""
Western Digital WD16 Performance Model

Grey-box queueing model for the Western Digital WD16 microprocessor (1977).

Specifications:
- Clock: 3.3 MHz
- Bus Width: 16-bit
- Transistors: ~12,000

Source: Western Digital WD16 Microcomputer Users Manual
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
    'name': 'Western Digital WD16',
    'year': 1977,
    'clock_mhz': 3.3,
    'bus_width': 16,
    'transistors': 12000
}

# Timing categories (5-15 categories capturing major instruction classes)
# Target CPI ~5.0 for LSI-11 compatible architecture
TIMING_CATEGORIES = {
    'register': {
        'cycles': 3,
        'weight': 0.20,
        'description': 'Register operations',
        'source': 'Western Digital WD16 Users Manual'
    },
    'immediate': {
        'cycles': 5,
        'weight': 0.15,
        'description': 'Immediate operand',
        'source': 'Western Digital WD16 Users Manual'
    },
    'memory': {
        'cycles': 7,
        'weight': 0.18,
        'description': 'Memory reference',
        'source': 'Western Digital WD16 Users Manual'
    },
    'indexed': {
        'cycles': 8,
        'weight': 0.10,
        'description': 'Indexed/indirect',
        'source': 'Western Digital WD16 Users Manual'
    },
    'branch': {
        'cycles': 4,
        'weight': 0.12,
        'description': 'Branch instructions',
        'source': 'Western Digital WD16 Users Manual'
    },
    'jsr': {
        'cycles': 6,
        'weight': 0.08,
        'description': 'Subroutine call/return',
        'source': 'Western Digital WD16 Users Manual'
    },
    'byte': {
        'cycles': 5,
        'weight': 0.07,
        'description': 'Byte operations',
        'source': 'Western Digital WD16 Users Manual'
    },
    'trap': {
        'cycles': 10,
        'weight': 0.05,
        'description': 'Trap/interrupt',
        'source': 'Western Digital WD16 Users Manual'
    },
    'misc': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'Miscellaneous',
        'source': 'Western Digital WD16 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 500000,
    'ips_max': 900000,
    'cpi_min': 3,
    'cpi_max': 10,
    'expected_bottlenecks': ['memory', 'decode'],
    'source': 'Western Digital WD16 Users Manual'
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
