#!/usr/bin/env python3
"""
AMD Am2901 Bit-Slice Queueing Model (1975)

BUILD YOUR OWN CPU!

The Am2901 is a 4-bit ALU "slice" that you cascade to build
custom CPUs of any width:
- 4 slices = 16-bit CPU
- 8 slices = 32-bit CPU
- etc.

You define the instruction set via microcode in external PROMs.

Used in:
- DEC VAX (floating point)
- Cray (I/O processors)
- Symbolics Lisp machines
- Arcade games (Atari, Williams)
- Military systems

This is a different modeling paradigm - the "processor" is the
entire bit-slice system, not just the 2901 chip.

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

class AMD2901QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.slices = 4  # Default 16-bit
    
    def set_width(self, slices: int):
        """Set number of slices (4, 8, 16, etc.)"""
        self.slices = slices
    
    def predict_cycle_time(self) -> float:
        """Predict cycle time based on slice count."""
        # More slices = longer carry propagation
        base_time_ns = 55  # Single slice
        # With carry lookahead, scales sub-linearly
        return base_time_ns * (1 + 0.1 * (self.slices - 1))
    
    def system_components(self) -> Dict:
        """Components needed for a complete bit-slice CPU."""
        return {
            'alu_slices': f'{self.slices} x Am2901',
            'carry_lookahead': f'{self.slices // 4} x Am2902',
            'sequencer': '1-2 x Am2910',
            'microcode_rom': 'Multiple PROMs',
            'shift_control': '1 x Am2904',
            'total_chips': f'{self.slices + 5}+ chips'
        }
    
    def example_systems(self) -> Dict:
        return {
            'DEC VAX-11/780': 'Floating point unit',
            'Symbolics 3600': 'Lisp machine CPU',
            'Xerox Star': 'Desktop workstation',
            'Atari arcade': 'Star Wars, etc.',
            'Williams arcade': 'Defender, Joust'
        }

def main():
    model = AMD2901QueueModel('amd_2901_model.json')
    
    print("AMD Am2901 (1975) - Bit-Slice ALU")
    print("=" * 55)
    print("Build your own CPU by cascading 4-bit slices!")
    print()
    
    for slices in [4, 8, 16]:
        model.set_width(slices)
        cycle = model.predict_cycle_time()
        bits = slices * 4
        print(f"{slices} slices = {bits}-bit CPU, ~{cycle:.0f}ns cycle")
    
    print("\nComponents for 16-bit system:")
    comp = model.system_components()
    for part, desc in comp.items():
        print(f"  {part}: {desc}")
    
    print("\nUsed in:")
    for system, use in model.example_systems().items():
        print(f"  {system}: {use}")

if __name__ == "__main__":
    main()
