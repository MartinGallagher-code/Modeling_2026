#!/usr/bin/env python3
"""
Intel 8088 Performance Model

Grey-box queueing model for the Intel 8088 microprocessor (1979).

Specifications:
- Clock: 5.0 MHz
- Bus Width: 8-bit
- Transistors: 29,000

Source: Intel 8088 Users Manual
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
    'name': 'Intel 8088',
    'year': 1979,
    'clock_mhz': 5.0,
    'bus_width': 8,
    'transistors': 29000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg_reg': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'MOV r,r',
        'source': 'Intel 8088 Users Manual'
    },
    'mov_reg_mem': {
        'cycles': 16,
        'weight': 0.15,
        'description': 'MOV r,m (slower bus)',
        'source': 'Intel 8088 Users Manual'
    },
    'alu_register': {
        'cycles': 3,
        'weight': 0.2,
        'description': 'ADD/SUB/AND/OR r,r',
        'source': 'Intel 8088 Users Manual'
    },
    'alu_memory': {
        'cycles': 21,
        'weight': 0.1,
        'description': 'ALU with memory',
        'source': 'Intel 8088 Users Manual'
    },
    'immediate': {
        'cycles': 4,
        'weight': 0.12,
        'description': 'MOV r,imm',
        'source': 'Intel 8088 Users Manual'
    },
    'branch_taken': {
        'cycles': 16,
        'weight': 0.08,
        'description': 'Jcc taken',
        'source': 'Intel 8088 Users Manual'
    },
    'branch_not_taken': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'Jcc not taken',
        'source': 'Intel 8088 Users Manual'
    },
    'call_return': {
        'cycles': 28,
        'weight': 0.05,
        'description': 'CALL near',
        'source': 'Intel 8088 Users Manual'
    },
    'string_ops': {
        'cycles': 22,
        'weight': 0.04,
        'description': 'String operations',
        'source': 'Intel 8088 Users Manual'
    },
    'multiply': {
        'cycles': 143,
        'weight': 0.03,
        'description': 'MUL/IMUL',
        'source': 'Intel 8088 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 250000,
    'ips_max': 500000,
    'cpi_min': 10,
    'cpi_max': 20,
    'expected_bottlenecks': ['prefetch', 'bus_width'],
    'source': 'Intel 8088 Users Manual'
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
