#!/usr/bin/env python3
"""
Motorola 68881 Performance Model

Grey-box queueing model for the Motorola 68881 microprocessor (1984).

Specifications:
- Clock: 16.0 MHz
- Bus Width: 32-bit
- Transistors: 155,000

Source: MC68881 Users Manual
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
    'name': 'Motorola 68881',
    'year': 1984,
    'clock_mhz': 16.0,
    'bus_width': 32,
    'transistors': 155000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'fmove': {
        'cycles': 20,
        'weight': 0.2,
        'description': 'FMOVE',
        'source': 'MC68881 Users Manual'
    },
    'fadd': {
        'cycles': 30,
        'weight': 0.2,
        'description': 'FADD',
        'source': 'MC68881 Users Manual'
    },
    'fsub': {
        'cycles': 30,
        'weight': 0.1,
        'description': 'FSUB',
        'source': 'MC68881 Users Manual'
    },
    'fmul': {
        'cycles': 45,
        'weight': 0.2,
        'description': 'FMUL',
        'source': 'MC68881 Users Manual'
    },
    'fdiv': {
        'cycles': 90,
        'weight': 0.1,
        'description': 'FDIV',
        'source': 'MC68881 Users Manual'
    },
    'fsqrt': {
        'cycles': 120,
        'weight': 0.05,
        'description': 'FSQRT',
        'source': 'MC68881 Users Manual'
    },
    'fsin_fcos': {
        'cycles': 200,
        'weight': 0.05,
        'description': 'FSIN, FCOS',
        'source': 'MC68881 Users Manual'
    },
    'fcomp': {
        'cycles': 25,
        'weight': 0.1,
        'description': 'FCMP',
        'source': 'MC68881 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 150000,
    'ips_max': 500000,
    'cpi_min': 30,
    'cpi_max': 120,
    'expected_bottlenecks': ['execute', 'fpu'],
    'source': 'MC68881 Users Manual'
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
