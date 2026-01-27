#!/usr/bin/env python3
"""
Motorola 6800 CPU Queueing Model (1974)

The first Motorola microprocessor - contemporary and competitor to Intel 8080.
Chuck Peddle worked on this before leaving to create the 6502.

Key characteristics:
- Dual accumulators (A and B) - innovative for the time
- Clean, orthogonal instruction set
- Big-endian (unlike Intel)
- 1 MHz typical clock

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

class Motorola6800QueueModel:
    """Sequential execution model for Motorola 6800."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Compute weighted average service time
        self.service_time = (
            mix['load_store'] * np.mean([timings['load_direct'], timings['store_direct']]) +
            mix['alu_operations'] * np.mean([timings['alu_immediate'], timings['alu_direct']]) +
            mix['branch_jump'] * np.mean([timings['branch_taken'], timings['jmp']]) +
            mix['stack_ops'] * timings['push'] +
            mix['index_ops'] * timings['load_indexed'] +
            mix['other'] * 4.0
        )
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return [QueueMetrics("Execute", arrival_rate, self.service_time, util, float('inf'), float('inf'), float('inf'))]
        queue_len = util / (1 - util)
        wait = self.service_time / (1 - util)
        return [QueueMetrics("Execute", arrival_rate, self.service_time, util, queue_len, wait, wait + self.service_time)]
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        metrics = self.compute_stage_metrics(arrival_rate)
        if metrics[0].utilization >= 1.0:
            return 0.0, metrics
        efficiency = 1.0 / (1.0 + metrics[0].utilization)
        ipc = min(arrival_rate * efficiency, 1.0 / self.service_time)
        return ipc, metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        low, high = 0.01, 0.5
        for _ in range(50):
            mid = (low + high) / 2
            pred_ipc, metrics = self.predict_ipc(mid)
            if pred_ipc == 0: high = mid; continue
            error = abs(pred_ipc - measured_ipc) / measured_ipc * 100
            if error <= tolerance:
                return {'predicted_ipc': pred_ipc, 'error_percent': error, 'converged': True}
            if pred_ipc < measured_ipc: low = mid
            else: high = mid
        return {'predicted_ipc': pred_ipc, 'error_percent': error, 'converged': False}

def main():
    model = Motorola6800QueueModel('motorola_6800_model.json')
    print("Motorola 6800 (1974) - First Motorola Microprocessor")
    print("="*60)
    
    for rate in [0.05, 0.08, 0.10, 0.12]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    result = model.calibrate(0.07)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    print(f"Service Time: {model.service_time:.2f} cycles")
    print(f"Max IPC: {1/model.service_time:.4f}")

if __name__ == "__main__":
    main()
