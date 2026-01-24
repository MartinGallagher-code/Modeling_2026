#!/usr/bin/env python3
"""
Motorola 68020 CPU Queueing Model (1984)

First full 32-bit Motorola processor:
- 32-bit data bus (vs 68000/68010's 16-bit)
- 32-bit address space (4GB vs 16MB)
- 256-byte instruction cache
- Coprocessor interface for 68881/68882 FPU
- New instructions: bit fields, CAS/CAS2

Performance: 2-3× faster than 68010.

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

class Motorola68020QueueModel:
    """Three-stage pipeline model with instruction cache."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        cache = self.config['cache_system']
        self.cache_hit_rate = cache['hit_rate_typical']
        self.cache_hit_cycles = cache['hit_cycles']
        self.cache_miss_cycles = cache['miss_cycles']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Fetch with cache
        self.fetch_service = (self.cache_hit_rate * self.cache_hit_cycles + 
                              (1 - self.cache_hit_rate) * self.cache_miss_cycles)
        
        # Decode (simple stage)
        self.decode_service = 1.0
        
        # Execute - use more reasonable weighted average
        self.execute_service = (
            mix['move_operations'] * timings['move_reg_reg'] * 0.7 +
            mix['alu_operations'] * timings['add_reg'] +
            mix['branch_jump'] * timings['bra'] * 0.4 +
            mix['load_store'] * timings['move_mem_reg'] * 0.5 +
            mix['multiply_divide'] * 20.0 * 0.3 +
            mix['bit_field'] * timings['bit_field'] * 0.3 +
            mix['other'] * 3.0
        )
        
        self.queue_efficiency = 0.92
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        metrics = []
        for name, service in [("Fetch+Cache", self.fetch_service), 
                               ("Decode", self.decode_service),
                               ("Execute", self.execute_service)]:
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
        efficiency = self.queue_efficiency * (1.0 - 0.08)
        ipc = arrival_rate * efficiency
        max_ipc = 1.0 / max(m.service_time for m in metrics)
        return min(ipc, max_ipc), metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        low, high = 0.1, 0.8
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
    
    def compare_predecessors(self) -> Dict:
        ipc_68020, _ = self.predict_ipc(0.45)
        return {
            '68020': {'ipc': ipc_68020, 'clock': self.clock_freq_mhz, 'mips': ipc_68020 * self.clock_freq_mhz},
            '68010': {'ipc': 0.55, 'clock': 10.0, 'mips': 5.5},
            '68000': {'ipc': 0.50, 'clock': 8.0, 'mips': 4.0},
            'speedup_vs_68010': (ipc_68020 * self.clock_freq_mhz) / 5.5,
            'key_advantages': ['32-bit bus', 'I-cache', '32-bit address', 'Faster clock']
        }

def main():
    model = Motorola68020QueueModel('motorola_68020_model.json')
    print("Motorola 68020 (1984) - First Full 32-bit 68k")
    print("="*60)
    
    for rate in [0.30, 0.40, 0.50, 0.60]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.65)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.compare_predecessors()
    print(f"\n68020: {comp['68020']['mips']:.1f} MIPS")
    print(f"68010: {comp['68010']['mips']:.1f} MIPS")
    print(f"Speedup vs 68010: {comp['speedup_vs_68010']:.1f}×")

if __name__ == "__main__":
    main()
