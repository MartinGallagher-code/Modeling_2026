#!/usr/bin/env python3
"""
Intel iAPX 432 Performance Model

Grey-box queueing model for the Intel iAPX 432 microprocessor (1981).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 32-bit
- Transistors: 220,000

Source: Intel iAPX 432 General Data Processor
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
    'name': 'Intel iAPX 432',
    'year': 1981,
    'clock_mhz': 8.0,
    'bus_width': 32,
    'transistors': 220000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'simple_ops': {
        'cycles': 20,
        'weight': 0.25,
        'description': 'Simple operations',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'memory_ops': {
        'cycles': 30,
        'weight': 0.2,
        'description': 'Memory access',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'object_ops': {
        'cycles': 50,
        'weight': 0.15,
        'description': 'Object manipulation',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'branch': {
        'cycles': 35,
        'weight': 0.12,
        'description': 'Branch operations',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'call_return': {
        'cycles': 80,
        'weight': 0.1,
        'description': 'Procedure call',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'capability': {
        'cycles': 100,
        'weight': 0.1,
        'description': 'Capability operations',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'context_switch': {
        'cycles': 200,
        'weight': 0.05,
        'description': 'Context switch',
        'source': 'Intel iAPX 432 General Data Processor'
    },
    'misc': {
        'cycles': 25,
        'weight': 0.03,
        'description': 'Other',
        'source': 'Intel iAPX 432 General Data Processor'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 100000,
    'ips_max': 300000,
    'cpi_min': 25,
    'cpi_max': 80,
    'expected_bottlenecks': ['decode', 'microcode'],
    'source': 'Intel iAPX 432 General Data Processor'
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
