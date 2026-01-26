#!/usr/bin/env python3
"""
AMD Am29000 Performance Model

Grey-box queueing model for the AMD Am29000 microprocessor (1987).

Specifications:
- Clock: 25.0 MHz
- Bus Width: 32-bit
- Transistors: 300,000

Source: AMD Am29000 Users Manual
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
    'name': 'AMD Am29000',
    'year': 1987,
    'clock_mhz': 25.0,
    'bus_width': 32,
    'transistors': 300000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu_reg': {
        'cycles': 1,
        'weight': 0.3,
        'description': 'ALU register',
        'source': 'AMD Am29000 Users Manual'
    },
    'load': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Load',
        'source': 'AMD Am29000 Users Manual'
    },
    'store': {
        'cycles': 2,
        'weight': 0.1,
        'description': 'Store',
        'source': 'AMD Am29000 Users Manual'
    },
    'branch': {
        'cycles': 1,
        'weight': 0.12,
        'description': 'Branch (delay slot)',
        'source': 'AMD Am29000 Users Manual'
    },
    'call_ret': {
        'cycles': 4,
        'weight': 0.08,
        'description': 'CALL, RET',
        'source': 'AMD Am29000 Users Manual'
    },
    'multiply': {
        'cycles': 2,
        'weight': 0.1,
        'description': 'Multiply',
        'source': 'AMD Am29000 Users Manual'
    },
    'divide': {
        'cycles': 35,
        'weight': 0.02,
        'description': 'Divide',
        'source': 'AMD Am29000 Users Manual'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.1,
        'description': 'Other',
        'source': 'AMD Am29000 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 15000000,
    'ips_max': 25000000,
    'cpi_min': 1,
    'cpi_max': 4,
    'expected_bottlenecks': ['cache', 'pipeline'],
    'source': 'AMD Am29000 Users Manual'
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
