#!/usr/bin/env python3
"""
General Instrument PIC1650 Queueing Model (1977)

THE FIRST PIC MICROCONTROLLER

The PIC1650 was originally designed as a "Peripheral Interface Controller"
to handle I/O for the GI CP1600 CPU. But it turned out to be useful on
its own as a tiny, cheap microcontroller.

General Instrument spun off the PIC line to Microchip Technology in 1989,
and PICs have since shipped BILLIONS of units, becoming one of the most
successful microcontroller families ever.

Key characteristics:
- Harvard architecture (separate program/data memory)
- 33 simple instructions
- Most instructions execute in 1 cycle
- Extremely cheap and easy to use

The PIC architecture (though much enhanced) is still used today.

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

class GIPIC1650QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        # PIC has 2-stage pipeline, most instructions = 1 cycle
        # Only branches take 2 cycles
        branch_fraction = 0.15
        avg_cycles = 1 * (1 - branch_fraction) + 2 * branch_fraction
        
        base_ipc = 1.0 / avg_cycles  # ~0.87
        
        return base_ipc, []
    
    def compare_mcus(self) -> Dict:
        return {
            'PIC1650': {
                'year': 1977,
                'instructions': 33,
                'cycles_per_instr': '1 (2 for branch)',
                'architecture': 'Harvard',
                'strength': 'Simple, cheap'
            },
            '8048': {
                'year': 1976,
                'instructions': 90,
                'cycles_per_instr': '1-2',
                'architecture': 'Von Neumann',
                'strength': 'More capable'
            },
            '8051': {
                'year': 1980,
                'instructions': 111,
                'cycles_per_instr': '1-4',
                'architecture': 'Harvard',
                'strength': 'Feature-rich'
            },
            'verdict': 'PIC won on simplicity and cost'
        }
    
    def pic_evolution(self) -> Dict:
        return {
            '1977': 'PIC1650 - Original',
            '1985': 'PIC16C5x - Enhanced',
            '1998': 'PIC16F84 - Flash (hobbyist favorite)',
            '2000s': 'PIC18 series',
            '2010s': 'PIC32 (32-bit MIPS core)',
            'total_shipped': 'BILLIONS of units'
        }

def main():
    model = GIPIC1650QueueModel('gi_pic1650_model.json')
    
    print("GI PIC1650 (1977) - The First PIC")
    print("=" * 50)
    print("Ancestor of billions of microcontrollers!")
    print()
    
    ipc, _ = model.predict_ipc(0.8)
    print(f"IPC: {ipc:.4f}")
    print(f"At 1 MHz: ~0.25 MIPS (4 clocks/cycle)")
    print()
    
    print("PIC Evolution:")
    for year, desc in model.pic_evolution().items():
        print(f"  {year}: {desc}")

if __name__ == "__main__":
    main()
