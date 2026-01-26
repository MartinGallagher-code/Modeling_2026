#!/usr/bin/env python3
"""
Novix NC4016 Performance Model

Grey-box queueing model for the Novix NC4016 microprocessor (1985).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 16-bit
- Transistors: 12,000

Source: Novix NC4016 Data Sheet
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
    'name': 'Novix NC4016',
    'year': 1985,
    'clock_mhz': 8.0,
    'bus_width': 16,
    'transistors': 12000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu': {
        'cycles': 1,
        'weight': 0.4,
        'description': 'ALU operations',
        'source': 'Novix NC4016 Data Sheet'
    },
    'stack': {
        'cycles': 1,
        'weight': 0.25,
        'description': 'Stack operations',
        'source': 'Novix NC4016 Data Sheet'
    },
    'memory': {
        'cycles': 2,
        'weight': 0.12,
        'description': 'Memory access',
        'source': 'Novix NC4016 Data Sheet'
    },
    'call_ret': {
        'cycles': 1,
        'weight': 0.1,
        'description': 'CALL, RET',
        'source': 'Novix NC4016 Data Sheet'
    },
    'branch': {
        'cycles': 2,
        'weight': 0.08,
        'description': 'Branch',
        'source': 'Novix NC4016 Data Sheet'
    },
    'misc': {
        'cycles': 1,
        'weight': 0.05,
        'description': 'Other',
        'source': 'Novix NC4016 Data Sheet'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 6000000,
    'ips_max': 10000000,
    'cpi_min': 1,
    'cpi_max': 2,
    'expected_bottlenecks': ['stack', 'memory'],
    'source': 'Novix NC4016 Data Sheet'
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
