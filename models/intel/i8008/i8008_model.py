#!/usr/bin/env python3
"""
Intel 8008 Performance Model

Grey-box queueing model for the Intel 8008 microprocessor (1972).

Specifications:
- Clock: 0.5 MHz
- Bus Width: 8-bit
- Transistors: 3,500

Source: Intel 8008 Users Manual
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
    'name': 'Intel 8008',
    'year': 1972,
    'clock_mhz': 0.5,
    'bus_width': 8,
    'transistors': 3500
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg_reg': {
        'cycles': 10,
        'weight': 0.2,
        'description': 'MOV r1,r2 (5 T-states)',
        'source': 'Intel 8008 Users Manual'
    },
    'mov_reg_mem': {
        'cycles': 16,
        'weight': 0.15,
        'description': 'MOV r,M / MOV M,r',
        'source': 'Intel 8008 Users Manual'
    },
    'alu_register': {
        'cycles': 10,
        'weight': 0.2,
        'description': 'ADD/SUB/AND/OR r',
        'source': 'Intel 8008 Users Manual'
    },
    'alu_memory': {
        'cycles': 16,
        'weight': 0.1,
        'description': 'ADD M, etc.',
        'source': 'Intel 8008 Users Manual'
    },
    'immediate': {
        'cycles': 16,
        'weight': 0.1,
        'description': 'MVI, ADI, etc.',
        'source': 'Intel 8008 Users Manual'
    },
    'jump_unconditional': {
        'cycles': 22,
        'weight': 0.08,
        'description': 'JMP',
        'source': 'Intel 8008 Users Manual'
    },
    'jump_conditional': {
        'cycles': 18,
        'weight': 0.07,
        'description': 'Jcc',
        'source': 'Intel 8008 Users Manual'
    },
    'call_return': {
        'cycles': 22,
        'weight': 0.05,
        'description': 'CALL, RET',
        'source': 'Intel 8008 Users Manual'
    },
    'io_ops': {
        'cycles': 16,
        'weight': 0.03,
        'description': 'IN, OUT',
        'source': 'Intel 8008 Users Manual'
    },
    'misc': {
        'cycles': 10,
        'weight': 0.02,
        'description': 'HLT, NOP',
        'source': 'Intel 8008 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 23000,
    'ips_max': 80000,
    'cpi_min': 10,
    'cpi_max': 22,
    'expected_bottlenecks': ['fetch', 'sequential'],
    'source': 'Intel 8008 Users Manual'
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
