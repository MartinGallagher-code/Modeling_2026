#!/usr/bin/env python3
"""
Intel 8051 CPU Queueing Model (1980)

THE MOST SUCCESSFUL MICROCONTROLLER ARCHITECTURE EVER.

Billions of 8051s have been produced by 50+ manufacturers.
The architecture is STILL in production after 40+ years!

Key features:
- 4KB ROM, 128 bytes RAM on-chip
- Boolean processor (bit-addressable memory)
- Four register banks
- Full-duplex UART
- Two 16-bit timers
- Hardware multiply/divide

The 8051 defined what a microcontroller should be.

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

class Intel8051QueueModel:
    """Sequential microcontroller model for Intel 8051."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['effective_mhz']
        self.machine_cycle = self.config['performance_characteristics']['machine_cycle_clocks']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        self.service_time = self.machine_cycle * (
            mix['register_ops'] * timings['register_to_register'] +
            mix['memory_ops'] * timings['direct_addressing'] +
            mix['io_ops'] * timings['direct_addressing'] +
            mix['branch_jump'] * timings['jump'] +
            mix['bit_ops'] * timings['bit_operations'] +
            mix['other'] * 2.0
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
    
    def show_8051_impact(self) -> Dict:
        return {
            'years_in_production': 45,
            'manufacturers': '50+',
            'units_shipped': 'Billions',
            'still_produced': True,
            'derivatives': 'Hundreds',
            'applications': ['Automotive', 'Industrial', 'Consumer', 'IoT', 'Medical'],
            'verdict': 'Most successful MCU architecture ever'
        }

def main():
    model = Intel8051QueueModel('intel_8051_model.json')
    print("Intel 8051 (1980) - Most Successful MCU Ever")
    print("=" * 60)
    print("Billions shipped, still in production after 45 years!")
    print()
    
    for rate in [0.04, 0.06, 0.08, 0.10]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    result = model.calibrate(0.08)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    impact = model.show_8051_impact()
    print(f"\n8051 Impact:")
    print(f"  Manufacturers: {impact['manufacturers']}")
    print(f"  Units shipped: {impact['units_shipped']}")
    print(f"  Still produced: {impact['still_produced']}")
    print(f"  Verdict: {impact['verdict']}")

if __name__ == "__main__":
    main()
