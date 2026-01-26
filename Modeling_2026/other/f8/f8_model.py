#!/usr/bin/env python3
"""
Fairchild F8 Performance Model

Grey-box queueing model for the Fairchild F8 microprocessor (1975).

Specifications:
- Clock: 2.0 MHz
- Bus Width: 8-bit
- Transistors: 4,000

Source: Fairchild F8 Users Guide
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
    'name': 'Fairchild F8',
    'year': 1975,
    'clock_mhz': 2.0,
    'bus_width': 8,
    'transistors': 4000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'accumulator': {
        'cycles': 4,
        'weight': 0.25,
        'description': 'Accumulator ops',
        'source': 'Fairchild F8 Users Guide'
    },
    'scratchpad': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'Scratchpad',
        'source': 'Fairchild F8 Users Guide'
    },
    'memory': {
        'cycles': 8,
        'weight': 0.15,
        'description': 'Memory',
        'source': 'Fairchild F8 Users Guide'
    },
    'immediate': {
        'cycles': 5,
        'weight': 0.15,
        'description': 'Immediate',
        'source': 'Fairchild F8 Users Guide'
    },
    'branch': {
        'cycles': 8,
        'weight': 0.1,
        'description': 'Branch',
        'source': 'Fairchild F8 Users Guide'
    },
    'call_return': {
        'cycles': 13,
        'weight': 0.08,
        'description': 'PI, POP',
        'source': 'Fairchild F8 Users Guide'
    },
    'io': {
        'cycles': 8,
        'weight': 0.05,
        'description': 'I/O',
        'source': 'Fairchild F8 Users Guide'
    },
    'misc': {
        'cycles': 4,
        'weight': 0.02,
        'description': 'Other',
        'source': 'Fairchild F8 Users Guide'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 200000,
    'ips_max': 500000,
    'cpi_min': 4,
    'cpi_max': 13,
    'expected_bottlenecks': ['fetch', 'decode'],
    'source': 'Fairchild F8 Users Guide'
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
