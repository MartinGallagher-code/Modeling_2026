#!/usr/bin/env python3
"""
Zilog Z8000 CPU Queueing Model (1979)

The Z80's 16-bit successor - technically excellent but commercially failed.

Zilog designed an advanced 16-bit processor with excellent features:
- 16 orthogonal 16-bit registers
- Can combine into 8×32-bit or 4×64-bit
- Clean instruction set
- Good memory management

But it arrived too late (1979) when:
- Intel 8086 had IBM PC commitment
- Motorola 68000 had Apple/Amiga/Atari/Unix

The Z8000 is a cautionary tale: technical excellence ≠ market success.

Author: Grey-Box Performance Modeling Research  
Date: January 24, 2026
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class QueueMetrics:
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float

class ZilogZ8000QueueModel:
    """Sequential model for Zilog Z8000."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        self.service_time = (
            mix['register_ops'] * timings['register_to_register'] +
            mix['memory_ops'] * np.mean([timings['memory_load'], timings['memory_store']]) +
            mix['branch_jump'] * timings['branch'] +
            mix['string_ops'] * 12 +
            mix['multiply_divide'] * np.mean([timings['multiply_16'], timings['divide_32_16']]) +
            mix['other'] * 8
        )
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return 0.0, [QueueMetrics("Execute", arrival_rate, self.service_time, util, float('inf'), float('inf'), float('inf'))]
        efficiency = 1.0 / (1.0 + util * 0.5)
        ipc = min(arrival_rate * efficiency, 1.0 / self.service_time)
        metrics = [QueueMetrics("Execute", arrival_rate, self.service_time, util, util/(1-util), self.service_time/(1-util), 0)]
        return ipc, metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        low, high = 0.01, 0.20
        for _ in range(50):
            mid = (low + high) / 2
            pred_ipc, _ = self.predict_ipc(mid)
            if pred_ipc == 0: high = mid; continue
            error = abs(pred_ipc - measured_ipc) / measured_ipc * 100
            if error <= tolerance:
                return {'predicted_ipc': pred_ipc, 'error_percent': error, 'converged': True}
            if pred_ipc < measured_ipc: low = mid
            else: high = mid
        return {'predicted_ipc': pred_ipc, 'error_percent': error, 'converged': False}

def main():
    model = ZilogZ8000QueueModel('zilog_z8000_model.json')
    print("Zilog Z8000 (1979) - The 16-bit That Never Was")
    print("=" * 60)
    print("Technically excellent. Commercially failed.")
    print()
    for rate in [0.05, 0.08, 0.10, 0.12]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    result = model.calibrate(0.12)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")

if __name__ == "__main__":
    main()
