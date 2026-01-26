#!/usr/bin/env python3
"""
Intel 80386 Performance Model

Grey-box queueing model for the Intel 80386 microprocessor (1985).

Specifications:
- Clock: 16.0 MHz
- Bus Width: 32-bit
- Transistors: 275,000

Source: Intel 80386 Programmers Reference Manual
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
    'name': 'Intel 80386',
    'year': 1985,
    'clock_mhz': 16.0,
    'bus_width': 32,
    'transistors': 275000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg_reg': {
        'cycles': 2,
        'weight': 0.22,
        'description': 'MOV r,r',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'mov_reg_mem': {
        'cycles': 4,
        'weight': 0.18,
        'description': 'MOV r,m',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'alu_register': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'ALU r,r',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'alu_memory': {
        'cycles': 6,
        'weight': 0.1,
        'description': 'ALU r,m',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'immediate': {
        'cycles': 2,
        'weight': 0.1,
        'description': 'Immediate ops',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'branch_taken': {
        'cycles': 10,
        'weight': 0.06,
        'description': 'Jcc taken',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'branch_not_taken': {
        'cycles': 3,
        'weight': 0.04,
        'description': 'Jcc not taken',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'call_return': {
        'cycles': 10,
        'weight': 0.03,
        'description': 'CALL/RET',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
    'multiply': {
        'cycles': 14,
        'weight': 0.02,
        'description': 'MUL/IMUL',
        'source': 'Intel 80386 Programmers Reference Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 3000000,
    'ips_max': 11000000,
    'cpi_min': 2,
    'cpi_max': 6,
    'expected_bottlenecks': ['cache', 'memory'],
    'source': 'Intel 80386 Programmers Reference Manual'
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
