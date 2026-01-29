#!/usr/bin/env python3
"""
Ferranti F100-L Performance Model

Grey-box queueing model for the Ferranti F100-L microprocessor (1976).

Specifications:
- Clock: 1.0 MHz
- Bus Width: 16-bit
- Transistors: ~6,000

Source: Ferranti F100-L Programmers Reference Manual
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
    'name': 'Ferranti F100-L',
    'year': 1976,
    'clock_mhz': 1.0,
    'bus_width': 16,
    'transistors': 6000
}

# Timing categories (5-15 categories capturing major instruction classes)
# Target CPI ~4.0 for British military 16-bit processor
TIMING_CATEGORIES = {
    'alu': {
        'cycles': 3,
        'weight': 0.25,
        'description': 'ALU operations',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'memory': {
        'cycles': 5,
        'weight': 0.20,
        'description': 'Memory access',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'immediate': {
        'cycles': 4,
        'weight': 0.15,
        'description': 'Immediate operand',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'branch': {
        'cycles': 3,
        'weight': 0.12,
        'description': 'Branch instructions',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'jump': {
        'cycles': 4,
        'weight': 0.08,
        'description': 'Jump/subroutine',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'shift': {
        'cycles': 4,
        'weight': 0.08,
        'description': 'Shift operations',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'io': {
        'cycles': 5,
        'weight': 0.07,
        'description': 'I/O operations',
        'source': 'Ferranti F100-L Reference Manual'
    },
    'control': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'Control instructions',
        'source': 'Ferranti F100-L Reference Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 200000,
    'ips_max': 400000,
    'cpi_min': 3,
    'cpi_max': 5,
    'expected_bottlenecks': ['memory', 'alu'],
    'source': 'Ferranti F100-L Reference Manual'
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
