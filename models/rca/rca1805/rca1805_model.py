#!/usr/bin/env python3
"""
RCA 1805 Performance Model

Grey-box queueing model for the RCA 1805 microprocessor (1977).

Specifications:
- Clock: 3.0 MHz
- Bus Width: 8-bit
- Transistors: 6,000

Source: RCA CDP1805 Data Sheet
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
    'name': 'RCA 1805',
    'year': 1977,
    'clock_mhz': 3.0,
    'bus_width': 8,
    'transistors': 6000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'short_branch': {
        'cycles': 8,
        'weight': 0.15,
        'description': 'Short branch',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'long_branch': {
        'cycles': 16,
        'weight': 0.08,
        'description': 'Long branch',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'memory_ref': {
        'cycles': 8,
        'weight': 0.2,
        'description': 'Memory reference',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'reg_ops': {
        'cycles': 8,
        'weight': 0.25,
        'description': 'Register ops',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'immediate': {
        'cycles': 16,
        'weight': 0.12,
        'description': 'Immediate',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'io_ops': {
        'cycles': 8,
        'weight': 0.1,
        'description': 'I/O operations',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'control': {
        'cycles': 8,
        'weight': 0.05,
        'description': 'Control',
        'source': 'RCA CDP1805 Data Sheet'
    },
    'subroutine': {
        'cycles': 24,
        'weight': 0.05,
        'description': 'Subroutine',
        'source': 'RCA CDP1805 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 187000,
    'ips_max': 600000,
    'cpi_min': 8,
    'cpi_max': 24,
    'expected_bottlenecks': ['fetch', 'decode'],
    'source': 'RCA CDP1805 Data Sheet'
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
