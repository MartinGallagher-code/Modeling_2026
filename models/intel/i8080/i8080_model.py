#!/usr/bin/env python3
"""
Intel 8080 Performance Model

Grey-box queueing model for the Intel 8080 microprocessor (1974).

Specifications:
- Clock: 2.0 MHz
- Bus Width: 8-bit
- Transistors: 4,500

Source: Intel 8080 Microcomputer Systems User Manual
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
    'name': 'Intel 8080',
    'year': 1974,
    'clock_mhz': 2.0,
    'bus_width': 8,
    'transistors': 4500
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg_reg': {
        'cycles': 5,
        'weight': 0.2,
        'description': 'MOV r1,r2',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'mov_reg_mem': {
        'cycles': 7,
        'weight': 0.15,
        'description': 'MOV r,M / MOV M,r',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'alu_register': {
        'cycles': 4,
        'weight': 0.25,
        'description': 'ADD/SUB/AND/OR r',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'alu_memory': {
        'cycles': 7,
        'weight': 0.1,
        'description': 'ADD M, etc.',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'immediate': {
        'cycles': 7,
        'weight': 0.1,
        'description': 'MVI, ADI, etc.',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'branch_taken': {
        'cycles': 10,
        'weight': 0.08,
        'description': 'JZ, JNZ taken',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'branch_not_taken': {
        'cycles': 10,
        'weight': 0.04,
        'description': 'Jcc not taken',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'call_return': {
        'cycles': 17,
        'weight': 0.05,
        'description': 'CALL=17, RET=10',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
    'stack_ops': {
        'cycles': 11,
        'weight': 0.03,
        'description': 'PUSH/POP',
        'source': 'Intel 8080 Microcomputer Systems User Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 290000,
    'ips_max': 500000,
    'cpi_min': 4,
    'cpi_max': 18,
    'expected_bottlenecks': ['decode', 'fetch'],
    'source': 'Intel 8080 Microcomputer Systems User Manual'
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
