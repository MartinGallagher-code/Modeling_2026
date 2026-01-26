#!/usr/bin/env python3
"""
Zilog Z180 Performance Model

Grey-box queueing model for the Zilog Z180 microprocessor (1985).

Specifications:
- Clock: 6.0 MHz
- Bus Width: 8-bit
- Transistors: 20,000

Source: Z180 Users Manual
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
    'name': 'Zilog Z180',
    'year': 1985,
    'clock_mhz': 6.0,
    'bus_width': 8,
    'transistors': 20000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'ld_r_r': {
        'cycles': 3,
        'weight': 0.22,
        'description': 'LD r,r',
        'source': 'Z180 Users Manual'
    },
    'ld_r_n': {
        'cycles': 5,
        'weight': 0.12,
        'description': 'LD r,n',
        'source': 'Z180 Users Manual'
    },
    'ld_r_hl': {
        'cycles': 5,
        'weight': 0.15,
        'description': 'LD r,(HL)',
        'source': 'Z180 Users Manual'
    },
    'alu_r': {
        'cycles': 3,
        'weight': 0.2,
        'description': 'ALU r',
        'source': 'Z180 Users Manual'
    },
    'alu_hl': {
        'cycles': 5,
        'weight': 0.08,
        'description': 'ALU (HL)',
        'source': 'Z180 Users Manual'
    },
    'jp': {
        'cycles': 8,
        'weight': 0.08,
        'description': 'JP',
        'source': 'Z180 Users Manual'
    },
    'jr_taken': {
        'cycles': 10,
        'weight': 0.05,
        'description': 'JR taken',
        'source': 'Z180 Users Manual'
    },
    'call_ret': {
        'cycles': 14,
        'weight': 0.05,
        'description': 'CALL, RET',
        'source': 'Z180 Users Manual'
    },
    'multiply': {
        'cycles': 18,
        'weight': 0.03,
        'description': 'MLT',
        'source': 'Z180 Users Manual'
    },
    'push_pop': {
        'cycles': 9,
        'weight': 0.02,
        'description': 'PUSH, POP',
        'source': 'Z180 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 900000,
    'ips_max': 2000000,
    'cpi_min': 3,
    'cpi_max': 18,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'Z180 Users Manual'
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
