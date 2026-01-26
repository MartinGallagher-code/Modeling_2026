#!/usr/bin/env python3
"""
National NS32016 Performance Model

Grey-box queueing model for the National NS32016 microprocessor (1982).

Specifications:
- Clock: 10.0 MHz
- Bus Width: 16-bit
- Transistors: 60,000

Source: NS32016 Data Sheet
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
    'name': 'National NS32016',
    'year': 1982,
    'clock_mhz': 10.0,
    'bus_width': 16,
    'transistors': 60000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg': {
        'cycles': 5,
        'weight': 0.22,
        'description': 'MOV reg,reg',
        'source': 'NS32016 Data Sheet'
    },
    'mov_mem': {
        'cycles': 12,
        'weight': 0.18,
        'description': 'MOV mem,reg',
        'source': 'NS32016 Data Sheet'
    },
    'alu_reg': {
        'cycles': 5,
        'weight': 0.22,
        'description': 'ALU reg,reg',
        'source': 'NS32016 Data Sheet'
    },
    'alu_mem': {
        'cycles': 14,
        'weight': 0.1,
        'description': 'ALU mem,reg',
        'source': 'NS32016 Data Sheet'
    },
    'branch': {
        'cycles': 8,
        'weight': 0.1,
        'description': 'Branch',
        'source': 'NS32016 Data Sheet'
    },
    'call_ret': {
        'cycles': 20,
        'weight': 0.06,
        'description': 'BSR, RET',
        'source': 'NS32016 Data Sheet'
    },
    'multiply': {
        'cycles': 25,
        'weight': 0.05,
        'description': 'MUL',
        'source': 'NS32016 Data Sheet'
    },
    'divide': {
        'cycles': 50,
        'weight': 0.02,
        'description': 'DIV',
        'source': 'NS32016 Data Sheet'
    },
    'misc': {
        'cycles': 5,
        'weight': 0.05,
        'description': 'Other',
        'source': 'NS32016 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 800000,
    'ips_max': 2000000,
    'cpi_min': 5,
    'cpi_max': 25,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'NS32016 Data Sheet'
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
