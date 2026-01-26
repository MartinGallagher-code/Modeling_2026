#!/usr/bin/env python3
"""
National Semiconductor NS32016 CPU Queueing Model (1982)

The "First 32-bit Microprocessor" - a cautionary tale:
- Technically advanced architecture
- First to market with 32-bit design
- Plagued by silicon bugs
- Much slower than advertised
- Commercial failure

Lesson: Working silicon beats best architecture.

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

class NS32016QueueModel:
    """Two-stage model for the troubled NS32016."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Fetch (16-bit bus)
        self.fetch_service = 2.5 * 4  # Average instruction ~2.5 words, 4 cycles each
        
        # Execute
        self.execute_service = (
            mix['move_operations'] * np.mean([timings['mov_reg_reg'], timings['mov_reg_mem']]) +
            mix['alu_operations'] * timings['add_reg'] +
            mix['branch_jump'] * timings['branch'] +
            mix['load_store'] * timings['mov_mem_reg'] +
            mix['string_ops'] * timings['string_move'] +
            mix['multiply_divide'] * np.mean([timings['mul'], timings['div']]) +
            mix['other'] * 5.0
        )
        
        # Silicon bug penalty (real NS32016 was much slower than spec)
        self.bug_penalty = 1.3  # 30% slower due to workarounds
        self.execute_service *= self.bug_penalty
        
        self.queue_efficiency = 0.82
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        metrics = []
        for name, service in [("Fetch", self.fetch_service), ("Execute", self.execute_service)]:
            util = arrival_rate * service
            if util >= 1.0:
                metrics.append(QueueMetrics(name, arrival_rate, service, util, float('inf'), float('inf'), float('inf')))
            else:
                ql = util / (1 - util)
                wt = service / (1 - util)
                metrics.append(QueueMetrics(name, arrival_rate, service, util, ql, wt, wt + service))
        return metrics
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        metrics = self.compute_stage_metrics(arrival_rate)
        max_util = max(m.utilization for m in metrics)
        if max_util >= 1.0:
            return 0.0, metrics
        efficiency = self.queue_efficiency * (1.0 - 0.15)
        ipc = arrival_rate * efficiency
        max_ipc = 1.0 / max(m.service_time for m in metrics)
        return min(ipc, max_ipc), metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        low, high = 0.05, 0.5
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
    
    def compare_68000(self) -> Dict:
        ipc_ns32016, _ = self.predict_ipc(0.25)
        return {
            'ns32016': {'ipc': ipc_ns32016, 'clock': self.clock_freq_mhz, 
                        'mips': ipc_ns32016 * self.clock_freq_mhz, 'status': 'Failed'},
            '68000': {'ipc': 0.55, 'clock': 8.0, 'mips': 4.4, 'status': 'Success'},
            'lesson': 'Working silicon > Best architecture',
            'ns32016_problems': ['Silicon bugs', 'Slow actual speed', 'Late delivery', 'Poor ecosystem']
        }

def main():
    model = NS32016QueueModel('ns32016_model.json')
    print("NS32016 (1982) - First 32-bit Micro (and First 32-bit Failure)")
    print("="*60)
    
    for rate in [0.08, 0.10, 0.12, 0.15]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.10)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.compare_68000()
    print(f"\nNS32016: {comp['ns32016']['mips']:.1f} MIPS ({comp['ns32016']['status']})")
    print(f"68000:   {comp['68000']['mips']:.1f} MIPS ({comp['68000']['status']})")
    print(f"\nLesson: {comp['lesson']}")

if __name__ == "__main__":
    main()
