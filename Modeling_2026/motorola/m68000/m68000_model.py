#!/usr/bin/env python3
"""
Motorola 68000 Performance Model

Grey-box queueing model for the Motorola 68000 microprocessor (1979).

Specifications:
- Clock: 8.0 MHz
- Bus Width: 16-bit
- Transistors: 68,000

Source: M68000 Users Manual
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
    'name': 'Motorola 68000',
    'year': 1979,
    'clock_mhz': 8.0,
    'bus_width': 16,
    'transistors': 68000
}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {
    'move_reg': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'MOVE Dn,Dn',
        'source': 'M68000 Users Manual'
    },
    'move_mem': {
        'cycles': 12,
        'weight': 0.15,
        'description': 'MOVE (An),Dn',
        'source': 'M68000 Users Manual'
    },
    'alu_reg': {
        'cycles': 4,
        'weight': 0.2,
        'description': 'ADD, SUB, AND reg',
        'source': 'M68000 Users Manual'
    },
    'alu_mem': {
        'cycles': 12,
        'weight': 0.1,
        'description': 'ALU with memory',
        'source': 'M68000 Users Manual'
    },
    'immediate': {
        'cycles': 8,
        'weight': 0.1,
        'description': 'MOVE #imm',
        'source': 'M68000 Users Manual'
    },
    'branch': {
        'cycles': 10,
        'weight': 0.1,
        'description': 'Bcc',
        'source': 'M68000 Users Manual'
    },
    'jsr_rts': {
        'cycles': 18,
        'weight': 0.05,
        'description': 'JSR, RTS',
        'source': 'M68000 Users Manual'
    },
    'multiply': {
        'cycles': 70,
        'weight': 0.05,
        'description': 'MULS, MULU',
        'source': 'M68000 Users Manual'
    },
    'divide': {
        'cycles': 158,
        'weight': 0.03,
        'description': 'DIVS, DIVU',
        'source': 'M68000 Users Manual'
    },
    'misc': {
        'cycles': 4,
        'weight': 0.02,
        'description': 'NOP, etc.',
        'source': 'M68000 Users Manual'
    },
}

# Validation targets from documentation
VALIDATION_TARGETS = {
    'ips_min': 1000000,
    'ips_max': 2000000,
    'cpi_min': 4,
    'cpi_max': 158,
    'expected_bottlenecks': ['ea_calc', 'decode'],
    'source': 'M68000 Users Manual'
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
