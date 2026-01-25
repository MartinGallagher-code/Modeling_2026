#!/usr/bin/env python3
"""
NEC V20 CPU Queueing Model (1984)

The chip that proved you could beat Intel at their own game!

The V20 was a drop-in replacement for the 8088 that ran 10-40% faster.
It also included a hardware 8080 emulation mode, letting you run CP/M
on your IBM PC.

This chip sparked the Intel vs NEC lawsuit (1984-1989), which NEC won,
establishing the right to make clean-room x86 clones. This ruling
enabled AMD, Cyrix, and the entire x86 clone industry.

Key improvements over 8088:
- 4-5× faster multiply/divide
- Single-cycle barrel shifter
- Optimized string operations
- Hardware 8080 mode

Author: Grey-Box Performance Modeling Research
Date: January 25, 2026
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

class NECV20QueueModel:
    """Grey-box queueing model for NEC V20."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
        self._compute_service_times()
    
    def _compute_service_times(self):
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        self.avg_execute_time = (
            mix['alu_operations'] * timings['alu_reg_reg'] +
            mix['memory_load'] * timings['alu_reg_mem'] +
            mix['memory_store'] * timings['alu_reg_mem'] +
            mix['branch'] * (timings['branch_taken'] + timings['branch_not_taken']) / 2 +
            mix['string_ops'] * timings['string_move'] +
            mix['multiply_divide'] * (timings['multiply_16'] + timings['divide_16']) / 2 +
            mix['other'] * timings['alu_reg_reg']
        )
        
        self.prefetch_service = 2.0
        self.execute_service = self.avg_execute_time * 0.85  # V20 optimization
    
    def _mm1_metrics(self, name: str, arrival_rate: float, 
                     service_time: float) -> QueueMetrics:
        utilization = arrival_rate * service_time
        if utilization >= 1.0:
            return QueueMetrics(name, arrival_rate, service_time, 1.0,
                              float('inf'), float('inf'), float('inf'))
        queue_length = utilization / (1 - utilization)
        wait_time = service_time / (1 - utilization)
        return QueueMetrics(name, arrival_rate, service_time, utilization,
                          queue_length, wait_time, wait_time)
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        prefetch = self._mm1_metrics('Prefetch', arrival_rate, self.prefetch_service)
        execute = self._mm1_metrics('Execute', arrival_rate, self.execute_service)
        
        if prefetch.utilization >= 1.0 or execute.utilization >= 1.0:
            return 0.0, [prefetch, execute]
        
        total_response = prefetch.response_time + execute.response_time
        ipc = 1.0 / total_response if total_response > 0 else 0.0
        return ipc, [prefetch, execute]
    
    def compare_8088(self) -> Dict:
        """Compare V20 to Intel 8088."""
        return {
            'multiply_16_cycles': {'8088': 118, 'V20': 25, 'speedup': '4.7×'},
            'divide_16_cycles': {'8088': 150, 'V20': 30, 'speedup': '5.0×'},
            'shift_multiple': {'8088': '4+n cycles', 'V20': '1 cycle', 'speedup': 'huge'},
            'string_ops': {'8088': 'standard', 'V20': 'optimized', 'speedup': '20-30%'},
            'overall': '10-40% faster on real code',
            'bonus': 'Hardware 8080 emulation mode!'
        }
    
    def lawsuit_history(self) -> Dict:
        return {
            'filed': 1984,
            'plaintiff': 'Intel',
            'defendant': 'NEC',
            'claim': 'V20/V30 copied 8088/8086 microcode',
            'verdict': 'NEC wins (1989)',
            'reason': 'NEC proved clean-room implementation',
            'impact': 'Enabled AMD, Cyrix, and all x86 clones',
            'irony': 'Intel lawsuit backfired spectacularly'
        }

def main():
    model = NECV20QueueModel('nec_v20_model.json')
    
    print("NEC V20 (1984) - The Faster 8088")
    print("=" * 55)
    print("Drop-in 8088 replacement, 10-40% faster!")
    print()
    
    for rate in [0.08, 0.10, 0.12]:
        ipc, metrics = model.predict_ipc(rate)
        print(f"λ={rate:.2f}: IPC={ipc:.4f}")
    
    print("\nV20 vs 8088:")
    comp = model.compare_8088()
    print(f"  Multiply: {comp['multiply_16_cycles']['speedup']} faster")
    print(f"  Divide: {comp['divide_16_cycles']['speedup']} faster")
    print(f"  Overall: {comp['overall']}")
    
    print("\nLawsuit Result:")
    lawsuit = model.lawsuit_history()
    print(f"  Intel sued NEC, NEC WON ({lawsuit['verdict']})")
    print(f"  Impact: {lawsuit['impact']}")

if __name__ == "__main__":
    main()
