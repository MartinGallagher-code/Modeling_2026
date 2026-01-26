#!/usr/bin/env python3
"""
TI TMS9900 Performance Model

Grey-box queueing model for the TI TMS9900 microprocessor (1976).

Specifications:
- Clock: 3.0 MHz
- Bus Width: 16-bit
- Transistors: 8,000

Source: TI TMS9900 Users Guide
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
    'name': 'TI TMS9900',
    'year': 1976,
    'clock_mhz': 3.0,
    'bus_width': 16,
    'transistors': 8000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'register': {
        'cycles': 14,
        'weight': 0.2,
        'description': 'Register-register',
        'source': 'TI TMS9900 Users Guide'
    },
    'immediate': {
        'cycles': 14,
        'weight': 0.15,
        'description': 'Immediate',
        'source': 'TI TMS9900 Users Guide'
    },
    'memory': {
        'cycles': 22,
        'weight': 0.18,
        'description': 'Memory',
        'source': 'TI TMS9900 Users Guide'
    },
    'indexed': {
        'cycles': 26,
        'weight': 0.1,
        'description': 'Indexed',
        'source': 'TI TMS9900 Users Guide'
    },
    'jump': {
        'cycles': 10,
        'weight': 0.12,
        'description': 'Jump',
        'source': 'TI TMS9900 Users Guide'
    },
    'cru': {
        'cycles': 12,
        'weight': 0.08,
        'description': 'CRU bit ops',
        'source': 'TI TMS9900 Users Guide'
    },
    'shift': {
        'cycles': 20,
        'weight': 0.05,
        'description': 'Shift',
        'source': 'TI TMS9900 Users Guide'
    },
    'multiply': {
        'cycles': 52,
        'weight': 0.05,
        'description': 'MPY',
        'source': 'TI TMS9900 Users Guide'
    },
    'divide': {
        'cycles': 92,
        'weight': 0.02,
        'description': 'DIV',
        'source': 'TI TMS9900 Users Guide'
    },
    'blwp': {
        'cycles': 26,
        'weight': 0.05,
        'description': 'BLWP context switch',
        'source': 'TI TMS9900 Users Guide'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 300000,
    'ips_max': 700000,
    'cpi_min': 8,
    'cpi_max': 52,
    'expected_bottlenecks': ['memory', 'workspace'],
    'source': 'TI TMS9900 Users Guide'
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
