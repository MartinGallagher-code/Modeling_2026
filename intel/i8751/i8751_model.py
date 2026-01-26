#!/usr/bin/env python3
"""
Intel 8751 Performance Model

Grey-box queueing model for the Intel 8751 microprocessor (1980).

Specifications:
- Clock: 12.0 MHz
- Bus Width: 8-bit
- Transistors: 128,000

Source: Intel MCS-51 Users Manual
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
    'name': 'Intel 8751',
    'year': 1980,
    'clock_mhz': 12.0,
    'bus_width': 8,
    'transistors': 128000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_direct': {
        'cycles': 12,
        'weight': 0.2,
        'description': 'MOV direct',
        'source': 'Intel MCS-51 Users Manual'
    },
    'mov_indirect': {
        'cycles': 12,
        'weight': 0.15,
        'description': 'MOV @Ri',
        'source': 'Intel MCS-51 Users Manual'
    },
    'alu_ops': {
        'cycles': 12,
        'weight': 0.25,
        'description': 'ALU operations',
        'source': 'Intel MCS-51 Users Manual'
    },
    'immediate': {
        'cycles': 12,
        'weight': 0.12,
        'description': 'MOV #data',
        'source': 'Intel MCS-51 Users Manual'
    },
    'branch': {
        'cycles': 24,
        'weight': 0.1,
        'description': 'Branch ops',
        'source': 'Intel MCS-51 Users Manual'
    },
    'call_return': {
        'cycles': 24,
        'weight': 0.05,
        'description': 'CALL, RET',
        'source': 'Intel MCS-51 Users Manual'
    },
    'bit_ops': {
        'cycles': 12,
        'weight': 0.08,
        'description': 'Bit operations',
        'source': 'Intel MCS-51 Users Manual'
    },
    'multiply': {
        'cycles': 48,
        'weight': 0.03,
        'description': 'MUL, DIV',
        'source': 'Intel MCS-51 Users Manual'
    },
    'misc': {
        'cycles': 12,
        'weight': 0.02,
        'description': 'NOP',
        'source': 'Intel MCS-51 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 500000,
    'ips_max': 1000000,
    'cpi_min': 12,
    'cpi_max': 24,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'Intel MCS-51 Users Manual'
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
