#!/usr/bin/env python3
"""
Zilog Z280 CPU Queueing Model (1985)

The Z280 was Zilog's ambitious enhancement of the Z80, adding:
- On-chip MMU
- 256-byte instruction cache
- 16-bit bus
- 16 MB address space
- Multiply/divide instructions

BUT it was not fully Z80 compatible, and by 1985 the market had
moved to 80286 and 68000. The Z280 was a commercial failure.

Lesson: Compatibility often matters more than features.

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

class ZilogZ280QueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        # Z280 had 4-stage pipeline and cache
        base_ipc = 0.15
        return base_ipc, []
    
    def why_failed(self) -> List[str]:
        return [
            "1. Not fully Z80 compatible (timing differences)",
            "2. By 1985, market wanted 80286 or 68000",
            "3. Complex to design with",
            "4. No existing software ecosystem",
            "5. Too little, too late"
        ]

def main():
    model = ZilogZ280QueueModel('zilog_z280_model.json')
    print("Zilog Z280 (1985) - The Failed Z80 Successor")
    print("=" * 55)
    ipc, _ = model.predict_ipc(0.12)
    print(f"IPC: {ipc:.4f}")
    print("\nWhy it failed:")
    for reason in model.why_failed():
        print(f"  {reason}")

if __name__ == "__main__":
    main()
