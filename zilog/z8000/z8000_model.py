#!/usr/bin/env python3
"""
Zilog Z8000 Performance Model

Grey-box queueing model for the Zilog Z8000 microprocessor (1979).

Specifications:
- Clock: 4.0 MHz
- Bus Width: 16-bit
- Transistors: 17,500

Source: Z8000 CPU Users Manual
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
    'name': 'Zilog Z8000',
    'year': 1979,
    'clock_mhz': 4.0,
    'bus_width': 16,
    'transistors': 17500
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'ld_r_r': {
        'cycles': 3,
        'weight': 0.22,
        'description': 'LD R,R',
        'source': 'Z8000 CPU Users Manual'
    },
    'ld_r_im': {
        'cycles': 4,
        'weight': 0.15,
        'description': 'LD R,#imm',
        'source': 'Z8000 CPU Users Manual'
    },
    'ld_r_mem': {
        'cycles': 7,
        'weight': 0.18,
        'description': 'LD R,@addr',
        'source': 'Z8000 CPU Users Manual'
    },
    'alu_r': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'ADD, SUB, etc.',
        'source': 'Z8000 CPU Users Manual'
    },
    'alu_mem': {
        'cycles': 8,
        'weight': 0.08,
        'description': 'ALU with memory',
        'source': 'Z8000 CPU Users Manual'
    },
    'jp': {
        'cycles': 6,
        'weight': 0.08,
        'description': 'JP cc',
        'source': 'Z8000 CPU Users Manual'
    },
    'call_ret': {
        'cycles': 12,
        'weight': 0.05,
        'description': 'CALL, RET',
        'source': 'Z8000 CPU Users Manual'
    },
    'multiply': {
        'cycles': 70,
        'weight': 0.02,
        'description': 'MULT',
        'source': 'Z8000 CPU Users Manual'
    },
    'divide': {
        'cycles': 107,
        'weight': 0.02,
        'description': 'DIV',
        'source': 'Z8000 CPU Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 500000,
    'ips_max': 1200000,
    'cpi_min': 3,
    'cpi_max': 12,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'Z8000 CPU Users Manual'
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
