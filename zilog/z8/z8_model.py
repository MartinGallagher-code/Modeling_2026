#!/usr/bin/env python3
"""
Zilog Z8 Performance Model

Grey-box queueing model for the Zilog Z8 microprocessor (1979).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 8-bit
- Transistors: 9,000

Source: Z8 MCU Users Manual
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
    'name': 'Zilog Z8',
    'year': 1979,
    'clock_mhz': 8.0,
    'bus_width': 8,
    'transistors': 9000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'ld_r_r': {
        'cycles': 6,
        'weight': 0.22,
        'description': 'LD r,r',
        'source': 'Z8 MCU Users Manual'
    },
    'ld_r_im': {
        'cycles': 6,
        'weight': 0.15,
        'description': 'LD r,#imm',
        'source': 'Z8 MCU Users Manual'
    },
    'ld_r_ir': {
        'cycles': 8,
        'weight': 0.15,
        'description': 'LD r,@Rr',
        'source': 'Z8 MCU Users Manual'
    },
    'alu_r': {
        'cycles': 6,
        'weight': 0.2,
        'description': 'ALU r,r',
        'source': 'Z8 MCU Users Manual'
    },
    'jp': {
        'cycles': 10,
        'weight': 0.1,
        'description': 'JP cc',
        'source': 'Z8 MCU Users Manual'
    },
    'call_ret': {
        'cycles': 14,
        'weight': 0.08,
        'description': 'CALL, RET',
        'source': 'Z8 MCU Users Manual'
    },
    'djnz': {
        'cycles': 12,
        'weight': 0.05,
        'description': 'DJNZ',
        'source': 'Z8 MCU Users Manual'
    },
    'misc': {
        'cycles': 6,
        'weight': 0.05,
        'description': 'Other',
        'source': 'Z8 MCU Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 500000,
    'ips_max': 1000000,
    'cpi_min': 6,
    'cpi_max': 20,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'Z8 MCU Users Manual'
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
