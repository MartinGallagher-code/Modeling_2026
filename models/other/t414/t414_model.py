#!/usr/bin/env python3
"""
Inmos T414 Performance Model

Grey-box queueing model for the Inmos T414 microprocessor (1985).

Specifications:
- Clock: 15.0 MHz
- Bus Width: 32-bit
- Transistors: 200,000

Source: Inmos T414 Technical Manual
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
    'name': 'Inmos T414',
    'year': 1985,
    'clock_mhz': 15.0,
    'bus_width': 32,
    'transistors': 200000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'direct': {
        'cycles': 1,
        'weight': 0.35,
        'description': 'Direct functions',
        'source': 'Inmos T414 Technical Manual'
    },
    'indirect': {
        'cycles': 2,
        'weight': 0.2,
        'description': 'Indirect functions',
        'source': 'Inmos T414 Technical Manual'
    },
    'load_store': {
        'cycles': 2,
        'weight': 0.15,
        'description': 'Load/Store',
        'source': 'Inmos T414 Technical Manual'
    },
    'jump': {
        'cycles': 3,
        'weight': 0.1,
        'description': 'Jump',
        'source': 'Inmos T414 Technical Manual'
    },
    'call': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'CALL',
        'source': 'Inmos T414 Technical Manual'
    },
    'channel': {
        'cycles': 6,
        'weight': 0.08,
        'description': 'Channel comms',
        'source': 'Inmos T414 Technical Manual'
    },
    'alt': {
        'cycles': 10,
        'weight': 0.03,
        'description': 'ALT',
        'source': 'Inmos T414 Technical Manual'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.04,
        'description': 'Other',
        'source': 'Inmos T414 Technical Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 5000000,
    'ips_max': 10000000,
    'cpi_min': 1,
    'cpi_max': 6,
    'expected_bottlenecks': ['memory', 'channel'],
    'source': 'Inmos T414 Technical Manual'
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
