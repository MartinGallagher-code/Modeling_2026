#!/usr/bin/env python3
"""
Data General mN601 Performance Model

Grey-box queueing model for the Data General mN601 (microNova) microprocessor (1977).

Specifications:
- Clock: 4.0 MHz
- Bus Width: 16-bit
- Transistors: ~15,000

Source: Data General microNova Programmers Reference
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
    'name': 'Data General mN601',
    'year': 1977,
    'clock_mhz': 4.0,
    'bus_width': 16,
    'transistors': 15000
}

# Timing categories (5-15 categories capturing major instruction classes)
# Target CPI ~4.0 for microNova architecture
TIMING_CATEGORIES = {
    'alu': {
        'cycles': 3,
        'weight': 0.25,
        'description': 'ALU operations',
        'source': 'Data General microNova Programmers Reference'
    },
    'memory': {
        'cycles': 5,
        'weight': 0.20,
        'description': 'Memory reference',
        'source': 'Data General microNova Programmers Reference'
    },
    'io': {
        'cycles': 5,
        'weight': 0.08,
        'description': 'I/O operations',
        'source': 'Data General microNova Programmers Reference'
    },
    'jump': {
        'cycles': 3,
        'weight': 0.15,
        'description': 'Jump instructions',
        'source': 'Data General microNova Programmers Reference'
    },
    'skip': {
        'cycles': 3,
        'weight': 0.10,
        'description': 'Skip instructions',
        'source': 'Data General microNova Programmers Reference'
    },
    'shift': {
        'cycles': 4,
        'weight': 0.07,
        'description': 'Shift operations',
        'source': 'Data General microNova Programmers Reference'
    },
    'stack': {
        'cycles': 6,
        'weight': 0.08,
        'description': 'Stack operations',
        'source': 'Data General microNova Programmers Reference'
    },
    'byte': {
        'cycles': 4,
        'weight': 0.07,
        'description': 'Byte manipulation',
        'source': 'Data General microNova Programmers Reference'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 800000,
    'ips_max': 1500000,
    'cpi_min': 3,
    'cpi_max': 6,
    'expected_bottlenecks': ['memory', 'stack'],
    'source': 'Data General microNova Programmers Reference'
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
