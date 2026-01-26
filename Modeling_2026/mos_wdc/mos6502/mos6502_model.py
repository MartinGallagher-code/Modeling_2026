#!/usr/bin/env python3
"""
MOS 6502 Performance Model

Grey-box queueing model for the MOS 6502 microprocessor (1975).

Specifications:
- Clock: 1.0 MHz
- Bus Width: 8-bit
- Transistors: 3,510

Source: MOS 6500 Hardware Manual
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
    'name': 'MOS 6502',
    'year': 1975,
    'clock_mhz': 1.0,
    'bus_width': 8,
    'transistors': 3510
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'implied': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'TAX, INX, etc.',
        'source': 'MOS 6500 Hardware Manual'
    },
    'immediate': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'LDA #imm',
        'source': 'MOS 6500 Hardware Manual'
    },
    'zero_page': {
        'cycles': 3,
        'weight': 0.22,
        'description': 'LDA $00',
        'source': 'MOS 6500 Hardware Manual'
    },
    'zero_page_x': {
        'cycles': 4,
        'weight': 0.1,
        'description': 'LDA $00,X',
        'source': 'MOS 6500 Hardware Manual'
    },
    'absolute': {
        'cycles': 4,
        'weight': 0.1,
        'description': 'LDA $0000',
        'source': 'MOS 6500 Hardware Manual'
    },
    'absolute_x': {
        'cycles': 5,
        'weight': 0.05,
        'description': 'LDA $0000,X (+1 page)',
        'source': 'MOS 6500 Hardware Manual'
    },
    'branch_taken': {
        'cycles': 3,
        'weight': 0.08,
        'description': 'BNE taken',
        'source': 'MOS 6500 Hardware Manual'
    },
    'branch_not_taken': {
        'cycles': 2,
        'weight': 0.04,
        'description': 'BNE not taken',
        'source': 'MOS 6500 Hardware Manual'
    },
    'jsr_rts': {
        'cycles': 6,
        'weight': 0.05,
        'description': 'JSR=6, RTS=6',
        'source': 'MOS 6500 Hardware Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 430000,
    'ips_max': 1000000,
    'cpi_min': 2,
    'cpi_max': 7,
    'expected_bottlenecks': ['memory', 'fetch'],
    'source': 'MOS 6500 Hardware Manual'
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
