#!/usr/bin/env python3
"""
Harris RTX2000 Performance Model

Grey-box queueing model for the Harris RTX2000 microprocessor (1988).

Specifications:
- Clock: 10.0 MHz
- Bus Width: 16-bit
- Transistors: 15,000

Source: Harris RTX2000 Data Sheet
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
    'name': 'Harris RTX2000',
    'year': 1988,
    'clock_mhz': 10.0,
    'bus_width': 16,
    'transistors': 15000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu': {
        'cycles': 1,
        'weight': 0.4,
        'description': 'ALU operations',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'stack': {
        'cycles': 1,
        'weight': 0.2,
        'description': 'Stack operations',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'memory': {
        'cycles': 2,
        'weight': 0.15,
        'description': 'Memory access',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'call_ret': {
        'cycles': 1,
        'weight': 0.1,
        'description': 'CALL, RET',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'branch': {
        'cycles': 2,
        'weight': 0.08,
        'description': 'Branch',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'multiply': {
        'cycles': 2,
        'weight': 0.05,
        'description': 'Multiply',
        'source': 'Harris RTX2000 Data Sheet'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.02,
        'description': 'Other',
        'source': 'Harris RTX2000 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 8000000,
    'ips_max': 12000000,
    'cpi_min': 1,
    'cpi_max': 2,
    'expected_bottlenecks': ['stack', 'memory'],
    'source': 'Harris RTX2000 Data Sheet'
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
