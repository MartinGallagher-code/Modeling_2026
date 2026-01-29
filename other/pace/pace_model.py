#!/usr/bin/env python3
"""
National PACE Performance Model

Grey-box queueing model for the National PACE microprocessor (1975).

Specifications:
- Clock: 2.0 MHz
- Bus Width: 16-bit
- Transistors: ~10,000 (p-channel MOS)

Source: National PACE Users Manual
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
    'name': 'National PACE',
    'year': 1975,
    'clock_mhz': 2.0,
    'bus_width': 16,
    'transistors': 10000
}

# Timing categories (5-15 categories capturing major instruction classes)
# Target CPI ~10.0 for slow p-channel MOS technology
TIMING_CATEGORIES = {
    'register': {
        'cycles': 8,
        'weight': 0.18,
        'description': 'Register-register',
        'source': 'National PACE Users Manual'
    },
    'immediate': {
        'cycles': 10,
        'weight': 0.15,
        'description': 'Immediate operand',
        'source': 'National PACE Users Manual'
    },
    'memory': {
        'cycles': 12,
        'weight': 0.20,
        'description': 'Memory operations',
        'source': 'National PACE Users Manual'
    },
    'indexed': {
        'cycles': 14,
        'weight': 0.10,
        'description': 'Indexed addressing',
        'source': 'National PACE Users Manual'
    },
    'branch': {
        'cycles': 8,
        'weight': 0.12,
        'description': 'Branch instructions',
        'source': 'National PACE Users Manual'
    },
    'jump': {
        'cycles': 10,
        'weight': 0.08,
        'description': 'Jump/subroutine',
        'source': 'National PACE Users Manual'
    },
    'stack': {
        'cycles': 12,
        'weight': 0.07,
        'description': 'Stack operations',
        'source': 'National PACE Users Manual'
    },
    'io': {
        'cycles': 14,
        'weight': 0.05,
        'description': 'I/O operations',
        'source': 'National PACE Users Manual'
    },
    'special': {
        'cycles': 10,
        'weight': 0.05,
        'description': 'Special instructions',
        'source': 'National PACE Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 150000,
    'ips_max': 300000,
    'cpi_min': 8,
    'cpi_max': 14,
    'expected_bottlenecks': ['memory', 'p_channel'],
    'source': 'National PACE Users Manual'
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
