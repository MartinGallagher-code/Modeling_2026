#!/usr/bin/env python3
"""
MIPS R2000 Performance Model

Grey-box queueing model for the MIPS R2000 microprocessor (1985).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 32-bit
- Transistors: 110,000

Source: MIPS R2000 Users Manual
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
    'name': 'MIPS R2000',
    'year': 1985,
    'clock_mhz': 8.0,
    'bus_width': 32,
    'transistors': 110000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'alu_reg': {
        'cycles': 1,
        'weight': 0.3,
        'description': 'ALU R-type',
        'source': 'MIPS R2000 Users Manual'
    },
    'load': {
        'cycles': 2,
        'weight': 0.2,
        'description': 'LW (load delay)',
        'source': 'MIPS R2000 Users Manual'
    },
    'store': {
        'cycles': 1,
        'weight': 0.12,
        'description': 'SW',
        'source': 'MIPS R2000 Users Manual'
    },
    'branch': {
        'cycles': 1,
        'weight': 0.12,
        'description': 'BEQ, BNE (delay slot)',
        'source': 'MIPS R2000 Users Manual'
    },
    'jump': {
        'cycles': 1,
        'weight': 0.08,
        'description': 'J, JAL',
        'source': 'MIPS R2000 Users Manual'
    },
    'immediate': {
        'cycles': 1,
        'weight': 0.1,
        'description': 'ADDI, ORI, etc.',
        'source': 'MIPS R2000 Users Manual'
    },
    'multiply': {
        'cycles': 12,
        'weight': 0.05,
        'description': 'MULT',
        'source': 'MIPS R2000 Users Manual'
    },
    'divide': {
        'cycles': 35,
        'weight': 0.03,
        'description': 'DIV',
        'source': 'MIPS R2000 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 5000000,
    'ips_max': 10000000,
    'cpi_min': 1,
    'cpi_max': 3,
    'expected_bottlenecks': ['pipeline', 'cache'],
    'source': 'MIPS R2000 Users Manual'
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
