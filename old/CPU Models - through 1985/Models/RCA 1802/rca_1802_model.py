#!/usr/bin/env python3
"""
RCA CDP1802 COSMAC CPU Queueing Model (1976)

The first CMOS microprocessor - still flying in Voyager spacecraft!

Key characteristics:
- First CMOS microprocessor ever
- Radiation-hardened versions for space
- 16 × 16-bit general registers
- Any register can be program counter
- Extremely low power (can run at DC!)
- Wide voltage range (3V to 15V)

Space missions: Voyager 1 & 2, Galileo, Magellan, Ulysses
Still operating: Voyager 1802s have run for 45+ years in space!

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

class RCA1802QueueModel:
    """Sequential model for the radiation-hardened 1802."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # 1802 uses machine cycles of 8 clock cycles each
        machine_cycle = 8
        
        self.service_time = machine_cycle * (
            mix['register_ops'] * timings['register_ops'] +
            mix['memory_ops'] * np.mean([timings['memory_load'], timings['memory_store']]) +
            mix['branch_jump'] * np.mean([timings['short_branch'], timings['long_branch']]) +
            mix['alu_ops'] * timings['alu_ops'] +
            mix['io_ops'] * timings['io'] +
            mix['other'] * 2.0
        )
    
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
        low, high = 0.001, 0.1
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
    
    def space_mission_stats(self) -> Dict:
        return {
            'voyager_launch': 1977,
            'years_operating': 2026 - 1977,
            'distance_voyager1': '15+ billion miles',
            'still_working': True,
            'power_consumption': '~1W',
            'radiation_exposure': 'Extreme (Jupiter, interstellar)',
            'lesson': 'Reliability > Performance for critical systems'
        }

def main():
    model = RCA1802QueueModel('rca_1802_model.json')
    print("RCA 1802 COSMAC (1976) - First CMOS Microprocessor")
    print("="*60)
    print("Still flying in Voyager spacecraft after 45+ years!")
    print()
    
    for rate in [0.01, 0.02, 0.03, 0.04]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.3f} → IPC={ipc:.5f}")
    
    result = model.calibrate(0.05)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.5f}, Error={result['error_percent']:.2f}%")
    print(f"Service Time: {model.service_time:.1f} clock cycles")
    
    stats = model.space_mission_stats()
    print(f"\nVoyager Stats:")
    print(f"  Years operating: {stats['years_operating']}")
    print(f"  Still working: {stats['still_working']}")
    print(f"  Lesson: {stats['lesson']}")

if __name__ == "__main__":
    main()
