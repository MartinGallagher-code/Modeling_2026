#!/usr/bin/env python3
"""
Signetics 2650 Performance Model

Grey-box queueing model for the Signetics 2650 microprocessor (1975).

Specifications:
- Clock: 1.25 MHz
- Bus Width: 8-bit
- Transistors: 6,000

Source: Signetics 2650 Microprocessor Manual
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
    'name': 'Signetics 2650',
    'year': 1975,
    'clock_mhz': 1.25,
    'bus_width': 8,
    'transistors': 6000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'register': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'Register ops',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'immediate': {
        'cycles': 4,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'absolute': {
        'cycles': 6,
        'weight': 0.15,
        'description': 'Absolute',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'relative': {
        'cycles': 6,
        'weight': 0.12,
        'description': 'Relative',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'indirect': {
        'cycles': 9,
        'weight': 0.08,
        'description': 'Indirect',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'branch': {
        'cycles': 5,
        'weight': 0.1,
        'description': 'Branch',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'call_return': {
        'cycles': 9,
        'weight': 0.07,
        'description': 'ZBSR, RETC',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
    'io': {
        'cycles': 6,
        'weight': 0.05,
        'description': 'I/O',
        'source': 'Signetics 2650 Microprocessor Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 200000,
    'ips_max': 500000,
    'cpi_min': 2,
    'cpi_max': 9,
    'expected_bottlenecks': ['fetch', 'decode'],
    'source': 'Signetics 2650 Microprocessor Manual'
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
