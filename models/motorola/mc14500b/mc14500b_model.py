#!/usr/bin/env python3
"""
Motorola MC14500B Performance Model

Grey-box queueing model for the MC14500B 1-bit industrial control unit (1976).

Specifications:
- Clock: 1.0 MHz @ 5V (up to 4 MHz @ 15V)
- Data Width: 1-bit
- Transistors: ~500
- All 16 instructions execute in exactly 1 clock cycle

Source: Motorola MC14500B Industrial Control Unit Handbook (1977)
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from common.queueing import QueueingModel
from common.validation import create_standard_suite

# Load model configuration from JSON
_JSON_FILE = Path(__file__).with_name('mc14500b_model.json')
with _JSON_FILE.open() as f:
    _DATA = json.load(f)

CONFIG = {
    'name': _DATA.get('name', 'Motorola MC14500B'),
    'year': _DATA.get('year', 1976),
    'clock_mhz': _DATA.get('clock_mhz', 1.0),
    'bus_width': _DATA.get('bus_width', 1),
    'transistors': _DATA.get('transistors', 500),
}

_timing_src = _DATA.get('source', 'MC14500B Industrial Control Unit Handbook (1977)')
TIMING_CATEGORIES = {}
for cat, meta in _DATA.get('timing_categories', {}).items():
    TIMING_CATEGORIES[cat] = {
        'cycles': meta.get('cycles', 1.0),
        'weight': meta.get('weight', 0.25),
        'description': meta.get('desc', meta.get('description', cat)),
        'source': meta.get('source', _timing_src),
    }

_vt = _DATA.get('validation_targets', {})
_ips = _vt.get('ips_range', [1000000, 1000000])
_cpi = _vt.get('cpi_range', [1.0, 1.0])
_sources = _vt.get('sources', [_timing_src])
VALIDATION_TARGETS = {
    'ips_min': _ips[0],
    'ips_max': _ips[1],
    'cpi_min': _cpi[0],
    'cpi_max': _cpi[1],
    'expected_bottlenecks': _vt.get('expected_bottlenecks', ['logic', 'load_store', 'control']),
    'source': _sources[0] if _sources else _timing_src,
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
    print(f"{CONFIG['name']} Performance Model")
    print("=" * 50)
    print(f"Clock: {CONFIG['clock_mhz']} MHz")
    print(f"Data Width: {CONFIG['bus_width']}-bit")
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
    suite.run()
    print(suite.summary())


if __name__ == '__main__':
    main()
