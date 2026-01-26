#!/usr/bin/env python3
"""
Intel 4040 Performance Model

Grey-box queueing model for the Intel 4040 microprocessor (1974).

Specifications:
- Clock: 0.74 MHz
- Bus Width: 4-bit
- Transistors: 3,000

Source: MCS-40 Users Manual
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
    'name': 'Intel 4040',
    'year': 1974,
    'clock_mhz': 0.74,
    'bus_width': 4,
    'transistors': 3000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'register_ops': {
        'cycles': 8,
        'weight': 0.25,
        'description': 'INC, ADD, SUB, LD, XCH',
        'source': 'MCS-40 Users Manual'
    },
    'accumulator_imm': {
        'cycles': 16,
        'weight': 0.15,
        'description': 'LDM, FIM',
        'source': 'MCS-40 Users Manual'
    },
    'memory_ops': {
        'cycles': 8,
        'weight': 0.18,
        'description': 'RDM, WRM',
        'source': 'MCS-40 Users Manual'
    },
    'bcd_arithmetic': {
        'cycles': 8,
        'weight': 0.1,
        'description': 'DAA operations',
        'source': 'MCS-40 Users Manual'
    },
    'jump_unconditional': {
        'cycles': 16,
        'weight': 0.08,
        'description': 'JUN',
        'source': 'MCS-40 Users Manual'
    },
    'jump_conditional': {
        'cycles': 16,
        'weight': 0.07,
        'description': 'JCN',
        'source': 'MCS-40 Users Manual'
    },
    'subroutine': {
        'cycles': 16,
        'weight': 0.05,
        'description': 'JMS, BBL',
        'source': 'MCS-40 Users Manual'
    },
    'io_ops': {
        'cycles': 8,
        'weight': 0.08,
        'description': 'I/O operations',
        'source': 'MCS-40 Users Manual'
    },
    'interrupt': {
        'cycles': 16,
        'weight': 0.02,
        'description': 'Interrupt handling',
        'source': 'MCS-40 Users Manual'
    },
    'nop_misc': {
        'cycles': 8,
        'weight': 0.02,
        'description': 'NOP, HLT',
        'source': 'MCS-40 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 50000,
    'ips_max': 100000,
    'cpi_min': 7,
    'cpi_max': 15,
    'expected_bottlenecks': ['fetch', 'sequential fetch'],
    'source': 'MCS-40 Users Manual'
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
