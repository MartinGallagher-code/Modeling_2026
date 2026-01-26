#!/usr/bin/env python3
"""
WDC 65816 Performance Model

Grey-box queueing model for the WDC 65816 microprocessor (1984).

Specifications:
- Clock: 2.8 MHz
- Bus Width: 16-bit
- Transistors: 22,000

Source: WDC 65816 Data Sheet
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
    'name': 'WDC 65816',
    'year': 1984,
    'clock_mhz': 2.8,
    'bus_width': 16,
    'transistors': 22000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'implied': {
        'cycles': 2,
        'weight': 0.15,
        'description': 'Implied',
        'source': 'WDC 65816 Data Sheet'
    },
    'immediate': {
        'cycles': 2,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'WDC 65816 Data Sheet'
    },
    'direct': {
        'cycles': 3,
        'weight': 0.18,
        'description': 'Direct page',
        'source': 'WDC 65816 Data Sheet'
    },
    'direct_x': {
        'cycles': 4,
        'weight': 0.1,
        'description': 'Direct,X',
        'source': 'WDC 65816 Data Sheet'
    },
    'absolute': {
        'cycles': 4,
        'weight': 0.12,
        'description': 'Absolute',
        'source': 'WDC 65816 Data Sheet'
    },
    'long': {
        'cycles': 5,
        'weight': 0.08,
        'description': 'Long addressing',
        'source': 'WDC 65816 Data Sheet'
    },
    'branch_taken': {
        'cycles': 3,
        'weight': 0.08,
        'description': 'Branch taken',
        'source': 'WDC 65816 Data Sheet'
    },
    'branch_not_taken': {
        'cycles': 2,
        'weight': 0.04,
        'description': 'Branch not taken',
        'source': 'WDC 65816 Data Sheet'
    },
    'jsr_rts': {
        'cycles': 8,
        'weight': 0.07,
        'description': 'JSR, RTS',
        'source': 'WDC 65816 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 1000000,
    'ips_max': 2500000,
    'cpi_min': 2,
    'cpi_max': 8,
    'expected_bottlenecks': ['memory', 'fetch'],
    'source': 'WDC 65816 Data Sheet'
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
