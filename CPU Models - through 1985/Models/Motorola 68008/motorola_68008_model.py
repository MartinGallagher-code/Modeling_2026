#!/usr/bin/env python3
"""
Motorola 68008 CPU Queueing Model (1982)

The 8-bit bus version of the 68000.

Just as Intel made the 8088 (8-bit bus 8086) for lower cost systems,
Motorola made the 68008 (8-bit bus 68000). Same 32-bit internal 
architecture, but external 8-bit data bus.

Trade-off:
- Cheaper (fewer pins, simpler PCB)
- Slower (~60% of 68000 speed for word/long operations)
- Smaller address space (1 MB vs 16 MB)

Most famous use: Sinclair QL (1984)

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

class Motorola68008QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
        self._compute_service_times()
    
    def _compute_service_times(self):
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Account for 8-bit bus penalty on word/long ops
        avg_memory_time = (
            timings['memory_read_byte'] * 0.3 +
            timings['memory_read_word'] * 0.4 +
            timings['memory_read_long'] * 0.3
        )
        
        self.avg_service_time = (
            mix['register_ops'] * timings['register_to_register'] +
            (mix['memory_load'] + mix['memory_store']) * avg_memory_time +
            mix['branch'] * timings['branch_taken'] +
            mix['other'] * timings['register_to_register']
        )
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        util = arrival_rate * self.avg_service_time
        if util >= 1.0:
            return 0.0, []
        ipc = 1.0 / self.avg_service_time * (1 - util)
        return min(ipc, 0.10), []
    
    def compare_68000(self) -> Dict:
        return {
            '68000': {'bus': '16-bit', 'address': '16 MB', 'pins': 64, 'speed': '1.0×'},
            '68008': {'bus': '8-bit', 'address': '1 MB', 'pins': 48, 'speed': '~0.4×'},
            'same': ['32-bit internal', 'Same instructions', 'Same registers'],
            'tradeoff': 'Lower cost for lower speed'
        }

def main():
    model = Motorola68008QueueModel('motorola_68008_model.json')
    print("Motorola 68008 (1982) - 8-bit bus 68000")
    print("=" * 50)
    print("Same 32-bit core, 8-bit external bus")
    
    for rate in [0.05, 0.07, 0.09]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    print("\n68008 vs 68000:")
    comp = model.compare_68000()
    print(f"  68000: {comp['68000']['bus']} bus, {comp['68000']['address']}")
    print(f"  68008: {comp['68008']['bus']} bus, {comp['68008']['address']}")
    print(f"  Speed: {comp['68008']['speed']} of 68000")

if __name__ == "__main__":
    main()
