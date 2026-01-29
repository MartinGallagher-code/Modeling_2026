#!/usr/bin/env python3
"""
National SC/MP Performance Model

Grey-box queueing model for the National SC/MP microprocessor (1974).

Specifications:
- Clock: 1.0 MHz
- Bus Width: 8-bit
- Transistors: 5,000

Source: National SC/MP Programmers Guide
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
    'name': 'National SC/MP',
    'year': 1974,
    'clock_mhz': 1.0,
    'bus_width': 8,
    'transistors': 5000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'implied': {
        'cycles': 7,
        'weight': 0.2,
        'description': 'Implied',
        'source': 'National SC/MP Programmers Guide'
    },
    'immediate': {
        'cycles': 10,
        'weight': 0.18,
        'description': 'Immediate',
        'source': 'National SC/MP Programmers Guide'
    },
    'memory': {
        'cycles': 18,
        'weight': 0.2,
        'description': 'Memory',
        'source': 'National SC/MP Programmers Guide'
    },
    'auto_indexed': {
        'cycles': 18,
        'weight': 0.1,
        'description': 'Auto-indexed',
        'source': 'National SC/MP Programmers Guide'
    },
    'branch': {
        'cycles': 9,
        'weight': 0.12,
        'description': 'Branch',
        'source': 'National SC/MP Programmers Guide'
    },
    'transfer': {
        'cycles': 7,
        'weight': 0.1,
        'description': 'Transfer',
        'source': 'National SC/MP Programmers Guide'
    },
    'io': {
        'cycles': 22,
        'weight': 0.05,
        'description': 'I/O',
        'source': 'National SC/MP Programmers Guide'
    },
    'misc': {
        'cycles': 7,
        'weight': 0.05,
        'description': 'Other',
        'source': 'National SC/MP Programmers Guide'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 50000,
    'ips_max': 150000,
    'cpi_min': 7,
    'cpi_max': 22,
    'expected_bottlenecks': ['fetch', 'serial_bus'],
    'source': 'National SC/MP Programmers Guide'
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
