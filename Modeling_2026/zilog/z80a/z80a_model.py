#!/usr/bin/env python3
"""
Zilog Z80A Performance Model

Grey-box queueing model for the Zilog Z80A microprocessor (1978).

Specifications:
- Clock: 4.0 MHz
- Bus Width: 8-bit
- Transistors: 8,500

Source: Z80A Data Sheet
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
    'name': 'Zilog Z80A',
    'year': 1978,
    'clock_mhz': 4.0,
    'bus_width': 8,
    'transistors': 8500
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'ld_r_r': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'LD r,r',
        'source': 'Z80A Data Sheet'
    },
    'ld_r_n': {
        'cycles': 7,
        'weight': 0.12,
        'description': 'LD r,n',
        'source': 'Z80A Data Sheet'
    },
    'ld_r_hl': {
        'cycles': 7,
        'weight': 0.15,
        'description': 'LD r,(HL)',
        'source': 'Z80A Data Sheet'
    },
    'ld_r_ix': {
        'cycles': 19,
        'weight': 0.05,
        'description': 'LD r,(IX+d)',
        'source': 'Z80A Data Sheet'
    },
    'alu_r': {
        'cycles': 4,
        'weight': 0.18,
        'description': 'ALU register',
        'source': 'Z80A Data Sheet'
    },
    'alu_hl': {
        'cycles': 7,
        'weight': 0.08,
        'description': 'ALU (HL)',
        'source': 'Z80A Data Sheet'
    },
    'jp': {
        'cycles': 10,
        'weight': 0.08,
        'description': 'JP',
        'source': 'Z80A Data Sheet'
    },
    'jr_taken': {
        'cycles': 12,
        'weight': 0.05,
        'description': 'JR taken',
        'source': 'Z80A Data Sheet'
    },
    'jr_not_taken': {
        'cycles': 7,
        'weight': 0.03,
        'description': 'JR not taken',
        'source': 'Z80A Data Sheet'
    },
    'call_ret': {
        'cycles': 17,
        'weight': 0.04,
        'description': 'CALL, RET',
        'source': 'Z80A Data Sheet'
    },
    'push_pop': {
        'cycles': 11,
        'weight': 0.02,
        'description': 'PUSH, POP',
        'source': 'Z80A Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 460000,
    'ips_max': 1280000,
    'cpi_min': 4,
    'cpi_max': 23,
    'expected_bottlenecks': ['decode', 'fetch'],
    'source': 'Z80A Data Sheet'
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
