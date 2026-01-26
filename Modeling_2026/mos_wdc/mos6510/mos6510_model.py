#!/usr/bin/env python3
"""
MOS 6510 Performance Model

Grey-box queueing model for the MOS 6510 microprocessor (1982).

Specifications:
- Clock: 1.0 MHz
- Bus Width: 8-bit
- Transistors: 4,000

Source: MOS 6510 Data Sheet
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
    'name': 'MOS 6510',
    'year': 1982,
    'clock_mhz': 1.0,
    'bus_width': 8,
    'transistors': 4000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'implied': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Implied',
        'source': 'MOS 6510 Data Sheet'
    },
    'immediate': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'MOS 6510 Data Sheet'
    },
    'zero_page': {
        'cycles': 3,
        'weight': 0.22,
        'description': 'Zero page',
        'source': 'MOS 6510 Data Sheet'
    },
    'zero_page_x': {
        'cycles': 4,
        'weight': 0.1,
        'description': 'Zero page,X',
        'source': 'MOS 6510 Data Sheet'
    },
    'absolute': {
        'cycles': 4,
        'weight': 0.1,
        'description': 'Absolute',
        'source': 'MOS 6510 Data Sheet'
    },
    'absolute_x': {
        'cycles': 5,
        'weight': 0.05,
        'description': 'Absolute,X',
        'source': 'MOS 6510 Data Sheet'
    },
    'branch_taken': {
        'cycles': 3,
        'weight': 0.08,
        'description': 'Branch taken',
        'source': 'MOS 6510 Data Sheet'
    },
    'branch_not_taken': {
        'cycles': 2,
        'weight': 0.04,
        'description': 'Branch not taken',
        'source': 'MOS 6510 Data Sheet'
    },
    'jsr_rts': {
        'cycles': 6,
        'weight': 0.05,
        'description': 'JSR, RTS',
        'source': 'MOS 6510 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 430000,
    'ips_max': 1000000,
    'cpi_min': 2,
    'cpi_max': 7,
    'expected_bottlenecks': ['memory', 'fetch'],
    'source': 'MOS 6510 Data Sheet'
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
