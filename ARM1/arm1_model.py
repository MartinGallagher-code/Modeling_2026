#!/usr/bin/env python3
"""
ARM1 CPU Queueing Model (1985)

The first ARM processor - birth of an architecture that would
eventually power billions of devices.

Designed by Sophie Wilson and Steve Furber at Acorn Computers:
- Only 25,000 transistors (vs 275,000 for 80386)
- 3-stage pipeline
- 16 registers (vs 8 for x86)
- Every instruction conditional
- Barrel shifter on every ALU operation

The ARM1 was development-only; ARM2 was the production version.
But ARM1 established the architecture that dominates mobile today.

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

class ARM1QueueModel:
    """Three-stage RISC pipeline model for ARM1."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        self.transistors = self.config['architecture']['transistor_count']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # 3-stage pipeline: Fetch, Decode, Execute
        self.fetch_service = 1.0
        self.decode_service = 1.0
        
        # Execute - RISC means most are single-cycle!
        self.execute_service = (
            mix['data_processing'] * timings['data_processing'] +
            mix['load_store'] * np.mean([timings['load_word'], timings['store_word']]) +
            mix['branch'] * timings['branch'] +
            mix['multiply'] * timings['multiply'] +
            mix['other'] * 2.0
        )
        
        self.queue_efficiency = 0.90
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        stages = [
            ("Fetch", self.fetch_service),
            ("Decode", self.decode_service),
            ("Execute", self.execute_service)
        ]
        
        metrics = []
        for name, service in stages:
            util = arrival_rate * service
            if util >= 1.0:
                metrics.append(QueueMetrics(name, arrival_rate, service,
                              util, float('inf'), float('inf'), float('inf')))
            else:
                ql = util / (1 - util)
                wt = service / (1 - util)
                metrics.append(QueueMetrics(name, arrival_rate, service,
                              util, ql, wt, wt + service))
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
        low, high = 0.2, 0.8
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
    
    def compare_contemporary(self) -> Dict:
        """Compare ARM1 to 80386 and 68020."""
        ipc_arm1, _ = self.predict_ipc(0.45)
        return {
            'ARM1': {
                'year': 1985, 'transistors': 25000,
                'ipc': ipc_arm1, 'clock_mhz': 8,
                'mips': ipc_arm1 * 8,
                'architecture': 'RISC'
            },
            '80386': {
                'year': 1985, 'transistors': 275000,
                'ipc': 0.40, 'clock_mhz': 16,
                'mips': 0.40 * 16,
                'architecture': 'CISC'
            },
            '68020': {
                'year': 1984, 'transistors': 190000,
                'ipc': 0.70, 'clock_mhz': 16,
                'mips': 0.70 * 16,
                'architecture': 'CISC'
            },
            'arm_advantage': {
                'transistors': '10× fewer than 386!',
                'power': 'Much lower',
                'design_time': 'Tiny team, 18 months',
                'trade_off': 'Lower absolute performance but incredible efficiency'
            }
        }
    
    def show_risc_benefits(self) -> Dict:
        """Show what made ARM special."""
        return {
            'conditional_execution': {
                'what': 'Every instruction can have condition code',
                'benefit': 'Fewer branches, better code density',
                'example': 'ADDEQ R0,R1,R2  ; Add only if Zero flag set'
            },
            'barrel_shifter': {
                'what': 'Free shift on second operand',
                'benefit': 'Common operations in single instruction',
                'example': 'ADD R0,R1,R2,LSL #2  ; R0 = R1 + (R2 << 2)'
            },
            'link_register': {
                'what': 'Return address in R14, not stack',
                'benefit': 'Fast leaf function calls',
                'example': 'BL function  ; Branch and Link (no stack push)'
            },
            'large_register_file': {
                'what': '16 registers vs 8 for x86',
                'benefit': 'Fewer memory accesses',
                'example': 'More variables can stay in registers'
            }
        }

def main():
    model = ARM1QueueModel('arm1_model.json')
    print("ARM1 (1985) - Birth of ARM Architecture")
    print("=" * 60)
    print("Only 25,000 transistors - the beginning of mobile computing")
    print()
    
    print(f"Transistors: {model.transistors:,}")
    print(f"Clock: {model.clock_freq_mhz:.0f} MHz")
    print()
    
    for rate in [0.35, 0.45, 0.55, 0.65]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.60)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.compare_contemporary()
    print(f"\nARM1 vs Competition (1985):")
    print(f"  ARM1:  {comp['ARM1']['transistors']:,} transistors, {comp['ARM1']['mips']:.1f} MIPS")
    print(f"  80386: {comp['80386']['transistors']:,} transistors, {comp['80386']['mips']:.1f} MIPS")
    print(f"  68020: {comp['68020']['transistors']:,} transistors, {comp['68020']['mips']:.1f} MIPS")
    print(f"\n  ARM advantage: {comp['arm_advantage']['transistors']}")

if __name__ == "__main__":
    main()
