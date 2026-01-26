#!/usr/bin/env python3
"""
Motorola 68020 Performance Model

Grey-box queueing model for the Motorola 68020 microprocessor (1984).

Specifications:
- Clock: 16.0 MHz
- Bus Width: 32-bit
- Transistors: 190,000

Source: MC68020 Users Manual
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
    'name': 'Motorola 68020',
    'year': 1984,
    'clock_mhz': 16.0,
    'bus_width': 32,
    'transistors': 190000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'move_reg': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'MOVE Dn,Dn',
        'source': 'MC68020 Users Manual'
    },
    'move_mem': {
        'cycles': 6,
        'weight': 0.18,
        'description': 'MOVE (An),Dn',
        'source': 'MC68020 Users Manual'
    },
    'alu_reg': {
        'cycles': 2,
        'weight': 0.25,
        'description': 'ALU register',
        'source': 'MC68020 Users Manual'
    },
    'alu_mem': {
        'cycles': 6,
        'weight': 0.1,
        'description': 'ALU memory',
        'source': 'MC68020 Users Manual'
    },
    'immediate': {
        'cycles': 3,
        'weight': 0.08,
        'description': 'Immediate',
        'source': 'MC68020 Users Manual'
    },
    'branch': {
        'cycles': 6,
        'weight': 0.06,
        'description': 'Branch',
        'source': 'MC68020 Users Manual'
    },
    'jsr_rts': {
        'cycles': 10,
        'weight': 0.04,
        'description': 'JSR, RTS',
        'source': 'MC68020 Users Manual'
    },
    'multiply': {
        'cycles': 28,
        'weight': 0.02,
        'description': 'Multiply',
        'source': 'MC68020 Users Manual'
    },
    'divide': {
        'cycles': 60,
        'weight': 0.02,
        'description': 'Divide',
        'source': 'MC68020 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 3000000,
    'ips_max': 6000000,
    'cpi_min': 3,
    'cpi_max': 60,
    'expected_bottlenecks': ['cache', 'memory'],
    'source': 'MC68020 Users Manual'
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
