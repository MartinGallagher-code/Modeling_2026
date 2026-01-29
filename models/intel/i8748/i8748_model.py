#!/usr/bin/env python3
"""
Intel 8748 Performance Model

Grey-box queueing model for the Intel 8748 microprocessor (1977).

Specifications:
- Clock: 6.0 MHz
- Bus Width: 8-bit
- Transistors: 8,000

Source: Intel MCS-48 Users Manual
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
    'name': 'Intel 8748',
    'year': 1977,
    'clock_mhz': 6.0,
    'bus_width': 8,
    'transistors': 8000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_a_r': {
        'cycles': 15,
        'weight': 0.25,
        'description': 'MOV A,Rn',
        'source': 'Intel MCS-48 Users Manual'
    },
    'mov_a_mem': {
        'cycles': 15,
        'weight': 0.15,
        'description': 'MOV A,@Ri',
        'source': 'Intel MCS-48 Users Manual'
    },
    'alu_ops': {
        'cycles': 15,
        'weight': 0.25,
        'description': 'ALU operations',
        'source': 'Intel MCS-48 Users Manual'
    },
    'immediate': {
        'cycles': 30,
        'weight': 0.1,
        'description': 'MOV A,#data',
        'source': 'Intel MCS-48 Users Manual'
    },
    'jump': {
        'cycles': 30,
        'weight': 0.1,
        'description': 'JMP, CALL',
        'source': 'Intel MCS-48 Users Manual'
    },
    'conditional': {
        'cycles': 30,
        'weight': 0.08,
        'description': 'Conditional jumps',
        'source': 'Intel MCS-48 Users Manual'
    },
    'io_ops': {
        'cycles': 30,
        'weight': 0.05,
        'description': 'I/O operations',
        'source': 'Intel MCS-48 Users Manual'
    },
    'misc': {
        'cycles': 15,
        'weight': 0.02,
        'description': 'NOP',
        'source': 'Intel MCS-48 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 400000,
    'ips_max': 750000,
    'cpi_min': 8,
    'cpi_max': 15,
    'expected_bottlenecks': ['fetch'],
    'source': 'Intel MCS-48 Users Manual'
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
