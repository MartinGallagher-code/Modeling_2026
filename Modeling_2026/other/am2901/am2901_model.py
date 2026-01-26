#!/usr/bin/env python3
"""
AMD Am2901 Performance Model

Grey-box queueing model for the AMD Am2901 microprocessor (1975).

Specifications:
- Clock: 10.0 MHz
- Bus Width: 4-bit
- Transistors: 1,700

Source: AMD Am2901 Data Sheet
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
    'name': 'AMD Am2901',
    'year': 1975,
    'clock_mhz': 10.0,
    'bus_width': 4,
    'transistors': 1700
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu_pass': {
        'cycles': 1,
        'weight': 0.3,
        'description': 'ALU pass through',
        'source': 'AMD Am2901 Data Sheet'
    },
    'alu_add': {
        'cycles': 1,
        'weight': 0.25,
        'description': 'ALU add',
        'source': 'AMD Am2901 Data Sheet'
    },
    'alu_sub': {
        'cycles': 1,
        'weight': 0.15,
        'description': 'ALU subtract',
        'source': 'AMD Am2901 Data Sheet'
    },
    'alu_logic': {
        'cycles': 1,
        'weight': 0.15,
        'description': 'ALU logic ops',
        'source': 'AMD Am2901 Data Sheet'
    },
    'shift': {
        'cycles': 2,
        'weight': 0.08,
        'description': 'Shift operations',
        'source': 'AMD Am2901 Data Sheet'
    },
    'ram_access': {
        'cycles': 1,
        'weight': 0.05,
        'description': 'RAM access',
        'source': 'AMD Am2901 Data Sheet'
    },
    'output': {
        'cycles': 1,
        'weight': 0.02,
        'description': 'Output',
        'source': 'AMD Am2901 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 2000000,
    'ips_max': 10000000,
    'cpi_min': 1,
    'cpi_max': 5,
    'expected_bottlenecks': ['microcode', 'external'],
    'source': 'AMD Am2901 Data Sheet'
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
