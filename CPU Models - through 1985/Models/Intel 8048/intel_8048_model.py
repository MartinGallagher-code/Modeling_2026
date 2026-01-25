#!/usr/bin/env python3
"""
Intel 8048 CPU Queueing Model (1976)

The first widely successful single-chip microcontroller.
Every IBM PC had one - in the keyboard!

Key features:
- CPU + 1KB ROM + 64 bytes RAM + I/O on single chip
- 27 I/O lines
- Two register banks for fast interrupts
- 8-bit timer

The 8048 started the microcontroller revolution and led
directly to the 8051, the most successful MCU architecture ever.

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

class Intel8048QueueModel:
    """Sequential microcontroller model for Intel 8048."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['effective_mhz']
        self.machine_cycle = self.config['performance_characteristics']['machine_cycle_clocks']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        self.service_time = self.machine_cycle * (
            mix['register_ops'] * timings['register_to_register'] +
            mix['memory_ops'] * timings['memory_indirect'] +
            mix['io_ops'] * timings['io_operation'] +
            mix['branch_jump'] * timings['jump'] +
            mix['other'] * 1.5
        )
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return [QueueMetrics("Execute", arrival_rate, self.service_time,
                                 util, float('inf'), float('inf'), float('inf'))]
        ql = util / (1 - util)
        wt = self.service_time / (1 - util)
        return [QueueMetrics("Execute", arrival_rate, self.service_time,
                            util, ql, wt, wt + self.service_time)]
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        metrics = self.compute_stage_metrics(arrival_rate)
        if metrics[0].utilization >= 1.0:
            return 0.0, metrics
        efficiency = 1.0 / (1.0 + metrics[0].utilization * 0.5)
        ipc = min(arrival_rate * efficiency, 1.0 / self.service_time)
        return ipc, metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        low, high = 0.01, 0.15
        best_error, best_ipc = float('inf'), 0
        for _ in range(50):
            mid = (low + high) / 2
            pred_ipc, _ = self.predict_ipc(mid)
            if pred_ipc == 0: high = mid; continue
            error = abs(pred_ipc - measured_ipc) / measured_ipc * 100
            if error < best_error: best_error, best_ipc = error, pred_ipc
            if error <= tolerance:
                return {'predicted_ipc': pred_ipc, 'error_percent': error, 'converged': True}
            if pred_ipc < measured_ipc: low = mid
            else: high = mid
        return {'predicted_ipc': best_ipc, 'error_percent': best_error, 'converged': False}

def main():
    model = Intel8048QueueModel('intel_8048_model.json')
    print("Intel 8048 (1976) - First Successful Microcontroller")
    print("=" * 60)
    print("In every IBM PC keyboard!")
    print()
    
    for rate in [0.03, 0.05, 0.07, 0.09]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    result = model.calibrate(0.07)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")

if __name__ == "__main__":
    main()
