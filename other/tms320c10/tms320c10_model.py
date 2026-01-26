#!/usr/bin/env python3
"""
TI TMS320C10 Performance Model

Grey-box queueing model for the TI TMS320C10 microprocessor (1983).

Specifications:
- Clock: 20.0 MHz
- Bus Width: 16-bit
- Transistors: 15,000

Source: TI TMS320C1x Users Guide
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
    'name': 'TI TMS320C10',
    'year': 1983,
    'clock_mhz': 20.0,
    'bus_width': 16,
    'transistors': 15000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'accumulator': {
        'cycles': 1,
        'weight': 0.3,
        'description': 'Accumulator ops',
        'source': 'TI TMS320C1x Users Guide'
    },
    'mac': {
        'cycles': 1,
        'weight': 0.25,
        'description': 'MAC (multiply-accumulate)',
        'source': 'TI TMS320C1x Users Guide'
    },
    'load_store': {
        'cycles': 1,
        'weight': 0.15,
        'description': 'Load/Store',
        'source': 'TI TMS320C1x Users Guide'
    },
    'branch': {
        'cycles': 2,
        'weight': 0.1,
        'description': 'Branch',
        'source': 'TI TMS320C1x Users Guide'
    },
    'call_ret': {
        'cycles': 2,
        'weight': 0.08,
        'description': 'CALL, RET',
        'source': 'TI TMS320C1x Users Guide'
    },
    'io': {
        'cycles': 2,
        'weight': 0.07,
        'description': 'I/O',
        'source': 'TI TMS320C1x Users Guide'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.05,
        'description': 'Other',
        'source': 'TI TMS320C1x Users Guide'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 5000000,
    'ips_max': 10000000,
    'cpi_min': 1,
    'cpi_max': 4,
    'expected_bottlenecks': ['memory', 'pipeline'],
    'source': 'TI TMS320C1x Users Guide'
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
