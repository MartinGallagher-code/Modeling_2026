#!/usr/bin/env python3
"""
Zilog Z80000 Performance Model

Grey-box queueing model for the Zilog Z80000 microprocessor (1986).

Specifications:
- Clock: 25.0 MHz
- Bus Width: 32-bit
- Transistors: 91,000

Source: Z80000 CPU Manual
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
    'name': 'Zilog Z80000',
    'year': 1986,
    'clock_mhz': 25.0,
    'bus_width': 32,
    'transistors': 91000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'ld_r_r': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'LD R,R',
        'source': 'Z80000 CPU Manual'
    },
    'ld_r_mem': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'LD R,@addr',
        'source': 'Z80000 CPU Manual'
    },
    'alu_r': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'ALU register',
        'source': 'Z80000 CPU Manual'
    },
    'alu_mem': {
        'cycles': 5,
        'weight': 0.1,
        'description': 'ALU memory',
        'source': 'Z80000 CPU Manual'
    },
    'jp': {
        'cycles': 4,
        'weight': 0.08,
        'description': 'JP',
        'source': 'Z80000 CPU Manual'
    },
    'call_ret': {
        'cycles': 8,
        'weight': 0.05,
        'description': 'CALL, RET',
        'source': 'Z80000 CPU Manual'
    },
    'multiply': {
        'cycles': 15,
        'weight': 0.04,
        'description': 'MULT',
        'source': 'Z80000 CPU Manual'
    },
    'divide': {
        'cycles': 30,
        'weight': 0.03,
        'description': 'DIV',
        'source': 'Z80000 CPU Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 4000000,
    'ips_max': 10000000,
    'cpi_min': 2,
    'cpi_max': 8,
    'expected_bottlenecks': ['cache', 'memory'],
    'source': 'Z80000 CPU Manual'
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
