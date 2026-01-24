#!/usr/bin/env python3
"""
Signetics 2650 CPU Queueing Model (1975)

An innovative but obscure 8-bit processor:
- 15-bit address bus (unusual - only 32KB)
- Memory organized in 8KB pages
- Good relative addressing (position-independent code)
- Used in some European computers and game consoles

Never achieved mainstream success due to limited address
space and unusual architecture.

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

class Signetics2650QueueModel:
    """Sequential model for the Signetics 2650."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        self.service_time = (
            mix['load_store'] * np.mean([timings['load_absolute'], timings['store']]) +
            mix['alu_ops'] * timings['alu_register'] +
            mix['branch_jump'] * timings['branch_relative'] +
            mix['register_ops'] * timings['alu_register'] +
            mix['io_ops'] * 3.0 +
            mix['other'] * timings['subroutine']
        ) * 3  # Clock cycles per machine cycle
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return [QueueMetrics("Execute", arrival_rate, self.service_time, util, float('inf'), float('inf'), float('inf'))]
        ql = util / (1 - util)
        wt = self.service_time / (1 - util)
        return [QueueMetrics("Execute", arrival_rate, self.service_time, util, ql, wt, wt + self.service_time)]
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        metrics = self.compute_stage_metrics(arrival_rate)
        if metrics[0].utilization >= 1.0:
            return 0.0, metrics
        efficiency = 1.0 / (1.0 + metrics[0].utilization)
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
    model = Signetics2650QueueModel('signetics_2650_model.json')
    print("Signetics 2650 (1975) - The Forgotten Alternative")
    print("="*60)
    print("Innovative but limited by 15-bit address space")
    print()
    
    for rate in [0.02, 0.04, 0.06, 0.08]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    result = model.calibrate(0.06)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    print(f"Service Time: {model.service_time:.1f} clock cycles")
    print(f"Max Address Space: {model.config['memory_system']['max_memory_kb']}KB (limited!)")

if __name__ == "__main__":
    main()
