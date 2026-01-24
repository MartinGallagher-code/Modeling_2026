#!/usr/bin/env python3
"""
Intel 4004 CPU Queueing Model (1971)

THE FIRST COMMERCIAL MICROPROCESSOR EVER.

On November 15, 1971, Intel announced the 4004 - a complete CPU on a single chip.
This 4-bit processor, originally designed for a Japanese calculator company (Busicom),
launched the microprocessor revolution that transformed the world.

Key characteristics:
- 4-bit data width (designed for BCD calculator operations)
- 2,300 transistors (vs billions today)
- 740 kHz clock (vs GHz today)
- ~60,000 operations per second

Designers: Federico Faggin, Ted Hoff, Stan Mazor

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

class Intel4004QueueModel:
    """Sequential execution model for the first microprocessor."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        self.transistors = self.config['architecture']['transistor_count']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Weighted average: mix of 1-word (8 cycle) and 2-word (16 cycle) instructions
        self.service_time = (
            mix['register_ops'] * timings['one_word_instruction'] +
            mix['memory_ops'] * timings['memory_read'] +
            mix['arithmetic'] * timings['one_word_instruction'] +
            mix['branch_jump'] * timings['two_word_instruction'] +
            mix['io_ops'] * timings['io']
        )
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return [QueueMetrics("Execute", arrival_rate, self.service_time, 
                                 util, float('inf'), float('inf'), float('inf'))]
        queue_len = util / (1 - util)
        wait = self.service_time / (1 - util)
        return [QueueMetrics("Execute", arrival_rate, self.service_time,
                            util, queue_len, wait, wait + self.service_time)]
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        metrics = self.compute_stage_metrics(arrival_rate)
        if metrics[0].utilization >= 1.0:
            return 0.0, metrics
        efficiency = 1.0 / (1.0 + metrics[0].utilization * 0.5)
        ipc = min(arrival_rate * efficiency, 1.0 / self.service_time)
        return ipc, metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        low, high = 0.01, 0.2
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
    
    def historical_comparison(self) -> Dict:
        """Compare to modern processors."""
        ipc_4004, _ = self.predict_ipc(0.08)
        mips_4004 = ipc_4004 * self.clock_freq_mhz
        
        # Modern comparison (approximate)
        modern_mips = 100000  # ~100,000 MIPS for modern CPU
        
        return {
            '4004': {
                'year': 1971,
                'transistors': 2300,
                'clock_mhz': 0.740,
                'mips': mips_4004,
                'bits': 4
            },
            'modern_cpu': {
                'year': 2026,
                'transistors': 50_000_000_000,
                'clock_mhz': 5000,
                'mips': modern_mips,
                'bits': 64
            },
            'improvement': {
                'transistors': 50_000_000_000 / 2300,
                'clock': 5000 / 0.740,
                'performance': modern_mips / mips_4004 if mips_4004 > 0 else float('inf')
            }
        }

def main():
    model = Intel4004QueueModel('intel_4004_model.json')
    print("Intel 4004 (1971) - THE FIRST MICROPROCESSOR")
    print("=" * 60)
    print("Where the microprocessor revolution began.")
    print()
    
    print(f"Transistors: {model.transistors:,}")
    print(f"Clock: {model.clock_freq_mhz * 1000:.0f} kHz")
    print(f"Data width: 4 bits")
    print()
    
    for rate in [0.04, 0.06, 0.08, 0.10]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    result = model.calibrate(0.09)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.historical_comparison()
    print(f"\n55 Years of Progress (1971-2026):")
    print(f"  Transistors: {comp['improvement']['transistors']:,.0f}× more")
    print(f"  Clock speed: {comp['improvement']['clock']:,.0f}× faster")
    print(f"  Performance: {comp['improvement']['performance']:,.0f}× faster")

if __name__ == "__main__":
    main()
