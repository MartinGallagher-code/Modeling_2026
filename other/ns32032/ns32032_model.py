#!/usr/bin/env python3
"""
National NS32032 Performance Model

Grey-box queueing model for the National NS32032 microprocessor (1984).

Specifications:
- Clock: 15.0 MHz
- Bus Width: 32-bit
- Transistors: 80,000

Source: NS32032 Data Sheet
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
    'name': 'National NS32032',
    'year': 1984,
    'clock_mhz': 15.0,
    'bus_width': 32,
    'transistors': 80000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg': {
        'cycles': 4,
        'weight': 0.25,
        'description': 'MOV reg,reg',
        'source': 'NS32032 Data Sheet'
    },
    'mov_mem': {
        'cycles': 8,
        'weight': 0.18,
        'description': 'MOV mem,reg',
        'source': 'NS32032 Data Sheet'
    },
    'alu_reg': {
        'cycles': 4,
        'weight': 0.25,
        'description': 'ALU reg,reg',
        'source': 'NS32032 Data Sheet'
    },
    'alu_mem': {
        'cycles': 10,
        'weight': 0.1,
        'description': 'ALU mem,reg',
        'source': 'NS32032 Data Sheet'
    },
    'branch': {
        'cycles': 6,
        'weight': 0.08,
        'description': 'Branch',
        'source': 'NS32032 Data Sheet'
    },
    'call_ret': {
        'cycles': 15,
        'weight': 0.06,
        'description': 'BSR, RET',
        'source': 'NS32032 Data Sheet'
    },
    'multiply': {
        'cycles': 18,
        'weight': 0.04,
        'description': 'MUL',
        'source': 'NS32032 Data Sheet'
    },
    'divide': {
        'cycles': 35,
        'weight': 0.02,
        'description': 'DIV',
        'source': 'NS32032 Data Sheet'
    },
    'misc': {
        'cycles': 4,
        'weight': 0.02,
        'description': 'Other',
        'source': 'NS32032 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 1500000,
    'ips_max': 4000000,
    'cpi_min': 4,
    'cpi_max': 20,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'NS32032 Data Sheet'
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
