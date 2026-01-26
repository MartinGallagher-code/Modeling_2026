#!/usr/bin/env python3
"""
TI TMS9995 Performance Model

Grey-box queueing model for the TI TMS9995 microprocessor (1981).

Specifications:
- Clock: 12.0 MHz
- Bus Width: 8-bit
- Transistors: 24,000

Source: TI TMS9995 Users Guide
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
    'name': 'TI TMS9995',
    'year': 1981,
    'clock_mhz': 12.0,
    'bus_width': 8,
    'transistors': 24000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'register': {
        'cycles': 8,
        'weight': 0.22,
        'description': 'Register-register',
        'source': 'TI TMS9995 Users Guide'
    },
    'immediate': {
        'cycles': 10,
        'weight': 0.15,
        'description': 'Immediate',
        'source': 'TI TMS9995 Users Guide'
    },
    'memory': {
        'cycles': 16,
        'weight': 0.18,
        'description': 'Memory',
        'source': 'TI TMS9995 Users Guide'
    },
    'jump': {
        'cycles': 8,
        'weight': 0.12,
        'description': 'Jump',
        'source': 'TI TMS9995 Users Guide'
    },
    'cru': {
        'cycles': 10,
        'weight': 0.08,
        'description': 'CRU bit ops',
        'source': 'TI TMS9995 Users Guide'
    },
    'shift': {
        'cycles': 14,
        'weight': 0.08,
        'description': 'Shift',
        'source': 'TI TMS9995 Users Guide'
    },
    'multiply': {
        'cycles': 40,
        'weight': 0.05,
        'description': 'MPY',
        'source': 'TI TMS9995 Users Guide'
    },
    'divide': {
        'cycles': 60,
        'weight': 0.02,
        'description': 'DIV',
        'source': 'TI TMS9995 Users Guide'
    },
    'blwp': {
        'cycles': 18,
        'weight': 0.05,
        'description': 'Context switch',
        'source': 'TI TMS9995 Users Guide'
    },
    'misc': {
        'cycles': 8,
        'weight': 0.05,
        'description': 'Other',
        'source': 'TI TMS9995 Users Guide'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 500000,
    'ips_max': 1200000,
    'cpi_min': 8,
    'cpi_max': 40,
    'expected_bottlenecks': ['memory', 'bus_width'],
    'source': 'TI TMS9995 Users Guide'
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
