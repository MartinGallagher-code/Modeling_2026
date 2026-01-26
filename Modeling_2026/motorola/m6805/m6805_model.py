#!/usr/bin/env python3
"""
Motorola 6805 Performance Model

Grey-box queueing model for the Motorola 6805 microprocessor (1979).

Specifications:
- Clock: 2.0 MHz
- Bus Width: 8-bit
- Transistors: 8,000

Source: MC6805 Data Sheet
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
    'name': 'Motorola 6805',
    'year': 1979,
    'clock_mhz': 2.0,
    'bus_width': 8,
    'transistors': 8000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'inherent': {
        'cycles': 3,
        'weight': 0.2,
        'description': 'Inherent',
        'source': 'MC6805 Data Sheet'
    },
    'immediate': {
        'cycles': 4,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'MC6805 Data Sheet'
    },
    'direct': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'Direct',
        'source': 'MC6805 Data Sheet'
    },
    'indexed': {
        'cycles': 5,
        'weight': 0.15,
        'description': 'Indexed',
        'source': 'MC6805 Data Sheet'
    },
    'extended': {
        'cycles': 5,
        'weight': 0.1,
        'description': 'Extended',
        'source': 'MC6805 Data Sheet'
    },
    'branch': {
        'cycles': 5,
        'weight': 0.08,
        'description': 'Branch',
        'source': 'MC6805 Data Sheet'
    },
    'jsr_rts': {
        'cycles': 9,
        'weight': 0.05,
        'description': 'JSR, RTS',
        'source': 'MC6805 Data Sheet'
    },
    'bit_ops': {
        'cycles': 5,
        'weight': 0.02,
        'description': 'BSET, BCLR',
        'source': 'MC6805 Data Sheet'
    },
    'misc': {
        'cycles': 3,
        'weight': 0.02,
        'description': 'Other',
        'source': 'MC6805 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 300000,
    'ips_max': 600000,
    'cpi_min': 3,
    'cpi_max': 11,
    'expected_bottlenecks': ['fetch', 'decode'],
    'source': 'MC6805 Data Sheet'
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
