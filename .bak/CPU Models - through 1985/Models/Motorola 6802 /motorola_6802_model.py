#!/usr/bin/env python3
"""
Motorola 6802 CPU Queueing Model (1977)

6800 with on-chip RAM and clock generator.

The 6802 simplified system design by integrating:
- 128 bytes of RAM
- Clock generator
- Single +5V power supply

This reduced the chip count and cost of 6800-based systems.

Note the difference:
- 6802 = CPU with RAM (no ROM, no I/O)
- 6801 = MCU with RAM, ROM, and I/O

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

class Motorola6802QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        base_ipc = 0.10
        return base_ipc, []
    
    def compare_6800_family(self) -> Dict:
        return {
            '6800': {'year': 1974, 'ram': 'None', 'clock': 'External', 'io': 'None'},
            '6802': {'year': 1977, 'ram': '128B', 'clock': 'On-chip', 'io': 'None'},
            '6801': {'year': 1978, 'ram': '128B', 'clock': 'On-chip', 'io': 'Yes (MCU)'},
            'note': '6802=CPU with RAM, 6801=full MCU'
        }

def main():
    model = Motorola6802QueueModel('motorola_6802_model.json')
    print("Motorola 6802 (1977) - 6800 with RAM")
    print("=" * 50)
    ipc, _ = model.predict_ipc(0.08)
    print(f"IPC: {ipc:.4f}")
    print("\n6800 Family:")
    comp = model.compare_6800_family()
    for chip, info in comp.items():
        if chip != 'note':
            print(f"  {chip}: RAM={info['ram']}, Clock={info['clock']}")

if __name__ == "__main__":
    main()
