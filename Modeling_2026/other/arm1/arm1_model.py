#!/usr/bin/env python3
"""
Acorn ARM1 Performance Model

Grey-box queueing model for the Acorn ARM1 microprocessor (1985).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 32-bit
- Transistors: 25,000

Source: ARM1 Technical Reference Manual
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
    'name': 'Acorn ARM1',
    'year': 1985,
    'clock_mhz': 8.0,
    'bus_width': 32,
    'transistors': 25000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'data_proc': {
        'cycles': 1,
        'weight': 0.35,
        'description': 'Data processing',
        'source': 'ARM1 Technical Reference Manual'
    },
    'load_single': {
        'cycles': 3,
        'weight': 0.18,
        'description': 'LDR',
        'source': 'ARM1 Technical Reference Manual'
    },
    'store_single': {
        'cycles': 2,
        'weight': 0.1,
        'description': 'STR',
        'source': 'ARM1 Technical Reference Manual'
    },
    'load_multiple': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'LDM',
        'source': 'ARM1 Technical Reference Manual'
    },
    'branch': {
        'cycles': 3,
        'weight': 0.12,
        'description': 'B, BL',
        'source': 'ARM1 Technical Reference Manual'
    },
    'branch_link': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'BL',
        'source': 'ARM1 Technical Reference Manual'
    },
    'multiply': {
        'cycles': 16,
        'weight': 0.05,
        'description': 'MUL',
        'source': 'ARM1 Technical Reference Manual'
    },
    'swi': {
        'cycles': 4,
        'weight': 0.02,
        'description': 'SWI',
        'source': 'ARM1 Technical Reference Manual'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.08,
        'description': 'Other',
        'source': 'ARM1 Technical Reference Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 4000000,
    'ips_max': 8000000,
    'cpi_min': 1,
    'cpi_max': 4,
    'expected_bottlenecks': ['memory', 'pipeline'],
    'source': 'ARM1 Technical Reference Manual'
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
