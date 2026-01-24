#!/usr/bin/env python3
"""
Motorola 68010 CPU Queueing Model (1982)

The 68010 added virtual memory support to the 68000:
- Bus error recovery (critical for VM)
- Loop mode (DBcc in 2 cycles vs 10)
- Vector Base Register (relocatable interrupts)
- MOVE from SR now privileged (security)

Performance: 5-10% faster than 68000, up to 20% for loop-heavy code.

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

class Motorola68010QueueModel:
    """Two-stage pipeline model for 68010 with loop mode optimization."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Compute weighted service times
        self.fetch_service = 3.0  # Average instruction fetch
        
        # Loop mode optimization for DBcc
        loop_cycles = mix['loop_operations'] * timings['dbcc_loop_mode']
        normal_cycles = (
            mix['move_operations'] * timings['move_reg_reg'] * 0.6 +
            mix['alu_operations'] * timings['add_reg'] +
            mix['branch_jump'] * timings['bra'] * 0.5 +
            mix['load_store'] * timings['move_mem_reg'] * 0.4 +
            mix['multiply_divide'] * 30.0 * 0.5 +
            mix['other'] * 4.0
        )
        self.execute_service = loop_cycles + normal_cycles
        self.queue_efficiency = 0.88
    
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
        efficiency = self.queue_efficiency * (1.0 - 0.10)
        ipc = arrival_rate * efficiency
        max_ipc = 1.0 / max(m.service_time for m in metrics)
        return min(ipc, max_ipc), metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        low, high = 0.05, 0.6
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
        ipc_68010, _ = self.predict_ipc(0.35)
        ipc_68000 = ipc_68010 / 1.08  # 68010 is ~8% faster
        return {
            '68010_ipc': ipc_68010,
            '68000_ipc': ipc_68000,
            'speedup': 1.08,
            'loop_mode_benefit': '5× for DBcc loops',
            'vm_support': '68010 only'
        }

def main():
    model = Motorola68010QueueModel('motorola_68010_model.json')
    print("Motorola 68010 (1982) - Virtual Memory + Loop Mode")
    print("="*60)
    
    for rate in [0.20, 0.30, 0.40, 0.50]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.55)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.compare_68000()
    print(f"\nvs 68000: {comp['speedup']:.2f}× faster")
    print(f"Loop mode: {comp['loop_mode_benefit']}")

if __name__ == "__main__":
    main()
