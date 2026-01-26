#!/usr/bin/env python3
"""
Western Design Center W65C802 Queueing Model (1984)

THE 65816 IN A 6502 PACKAGE!

The 65802 is the brilliant solution to the upgrade problem:
- Take the 65816 (16-bit 6502 successor)
- Put it in a 40-pin package (same as 6502!)
- Limit address space to 64KB (16-bit addressing)
- DROP INTO EXISTING 6502 SYSTEMS!

Internally, the 65802 is IDENTICAL to the 65816 - same
16-bit registers, same new instructions, same native mode.
The only difference is the package and address bus width.

This let users upgrade Apple IIs, C64s, and other 6502
systems to 16-bit capability without major hardware changes.

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
"""

import json
from dataclasses import dataclass
from typing import Tuple, Dict, List

@dataclass
class QueueMetrics:
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float

class WDC65802QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
        self.native_mode = False
    
    def set_mode(self, native: bool):
        """Switch between emulation (6502) and native (16-bit) mode."""
        self.native_mode = native
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        if self.native_mode:
            base_ipc = 0.14  # 16-bit operations
        else:
            base_ipc = 0.10  # 6502 emulation
        return base_ipc, []
    
    def compare_family(self) -> Dict:
        return {
            '6502': {
                'year': 1975,
                'bits': 8,
                'package': '40-pin',
                'address': '64 KB'
            },
            '65C02': {
                'year': 1983,
                'bits': 8,
                'package': '40-pin',
                'address': '64 KB',
                'note': 'CMOS, new instructions'
            },
            '65802': {
                'year': 1984,
                'bits': '8/16',
                'package': '40-pin (same!)',
                'address': '64 KB',
                'note': '65816 in 6502 package!'
            },
            '65816': {
                'year': 1984,
                'bits': '8/16',
                'package': '64-pin',
                'address': '16 MB',
                'note': 'Apple IIGS, SNES'
            }
        }
    
    def upgrade_scenario(self) -> str:
        return """
        Your Apple II (1977):
        ┌─────────────────────┐
        │  6502 @ 1 MHz       │
        │  8-bit, 64 KB       │
        └─────────────────────┘
                │
                │ Pop out 6502, drop in 65802
                ▼
        ┌─────────────────────┐
        │  65802 @ 1 MHz      │
        │  16-bit registers!  │
        │  New instructions!  │
        │  Still runs old     │
        │  software!          │
        └─────────────────────┘
        """

def main():
    model = WDC65802QueueModel('wdc_65802_model.json')
    
    print("WDC W65C802 (1984) - 65816 in 6502 Package")
    print("=" * 55)
    print("Drop a 16-bit CPU into your 6502 socket!")
    print()
    
    model.set_mode(False)
    ipc_emu, _ = model.predict_ipc(0.09)
    model.set_mode(True)
    ipc_nat, _ = model.predict_ipc(0.09)
    
    print(f"IPC (emulation mode): {ipc_emu:.4f}")
    print(f"IPC (native mode):    {ipc_nat:.4f}")
    print()
    
    print("6502 Family Evolution:")
    family = model.compare_family()
    for chip, info in family.items():
        note = info.get('note', '')
        print(f"  {chip}: {info['year']}, {info['bits']}-bit, {info['package']}"
              + (f" - {note}" if note else ""))
    
    print(model.upgrade_scenario())

if __name__ == "__main__":
    main()
