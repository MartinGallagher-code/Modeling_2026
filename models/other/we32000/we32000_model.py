#!/usr/bin/env python3
"""
AT&T WE 32000 Performance Model

Grey-box queueing model for the AT&T WE 32000 microprocessor (1982).

Specifications:
- Clock: 14.0 MHz
- Bus Width: 32-bit
- Transistors: 145,000

Source: WE 32000 Users Manual
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
    'name': 'AT&T WE 32000',
    'year': 1982,
    'clock_mhz': 14.0,
    'bus_width': 32,
    'transistors': 145000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'mov_reg': {
        'cycles': 4,
        'weight': 0.22,
        'description': 'MOV reg,reg',
        'source': 'WE 32000 Users Manual'
    },
    'mov_mem': {
        'cycles': 8,
        'weight': 0.18,
        'description': 'MOV mem,reg',
        'source': 'WE 32000 Users Manual'
    },
    'alu_reg': {
        'cycles': 4,
        'weight': 0.22,
        'description': 'ALU reg,reg',
        'source': 'WE 32000 Users Manual'
    },
    'alu_mem': {
        'cycles': 10,
        'weight': 0.1,
        'description': 'ALU mem,reg',
        'source': 'WE 32000 Users Manual'
    },
    'branch': {
        'cycles': 6,
        'weight': 0.1,
        'description': 'Branch',
        'source': 'WE 32000 Users Manual'
    },
    'call_ret': {
        'cycles': 12,
        'weight': 0.06,
        'description': 'JSB, RSB',
        'source': 'WE 32000 Users Manual'
    },
    'multiply': {
        'cycles': 15,
        'weight': 0.05,
        'description': 'MULW',
        'source': 'WE 32000 Users Manual'
    },
    'divide': {
        'cycles': 30,
        'weight': 0.02,
        'description': 'DIVW',
        'source': 'WE 32000 Users Manual'
    },
    'misc': {
        'cycles': 4,
        'weight': 0.05,
        'description': 'Other',
        'source': 'WE 32000 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 1000000,
    'ips_max': 3000000,
    'cpi_min': 4,
    'cpi_max': 15,
    'expected_bottlenecks': ['decode', 'memory'],
    'source': 'WE 32000 Users Manual'
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
