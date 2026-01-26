#!/usr/bin/env python3
"""
Sun SPARC Performance Model

Grey-box queueing model for the Sun SPARC microprocessor (1987).

Specifications:
- Clock: 16.0 MHz
- Bus Width: 32-bit
- Transistors: 100,000

Source: SPARC Architecture Manual
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
    'name': 'Sun SPARC',
    'year': 1987,
    'clock_mhz': 16.0,
    'bus_width': 32,
    'transistors': 100000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu_reg': {
        'cycles': 1,
        'weight': 0.32,
        'description': 'ALU register',
        'source': 'SPARC Architecture Manual'
    },
    'load': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Load (delay slot)',
        'source': 'SPARC Architecture Manual'
    },
    'store': {
        'cycles': 1,
        'weight': 0.1,
        'description': 'Store',
        'source': 'SPARC Architecture Manual'
    },
    'branch': {
        'cycles': 1,
        'weight': 0.12,
        'description': 'Branch (delay slot)',
        'source': 'SPARC Architecture Manual'
    },
    'call_ret': {
        'cycles': 2,
        'weight': 0.08,
        'description': 'CALL, RET',
        'source': 'SPARC Architecture Manual'
    },
    'save_restore': {
        'cycles': 1,
        'weight': 0.05,
        'description': 'Register windows',
        'source': 'SPARC Architecture Manual'
    },
    'immediate': {
        'cycles': 1,
        'weight': 0.08,
        'description': 'Immediate',
        'source': 'SPARC Architecture Manual'
    },
    'multiply': {
        'cycles': 5,
        'weight': 0.05,
        'description': 'SMUL',
        'source': 'SPARC Architecture Manual'
    },
    'divide': {
        'cycles': 18,
        'weight': 0.02,
        'description': 'SDIV',
        'source': 'SPARC Architecture Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 10000000,
    'ips_max': 20000000,
    'cpi_min': 1,
    'cpi_max': 3,
    'expected_bottlenecks': ['pipeline', 'cache'],
    'source': 'SPARC Architecture Manual'
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
