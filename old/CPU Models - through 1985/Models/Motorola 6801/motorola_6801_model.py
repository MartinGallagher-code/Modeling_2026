#!/usr/bin/env python3
"""
Motorola 6801 CPU Queueing Model (1978)

The first single-chip microcontroller with ON-CHIP RAM!

Before the 6801, MCUs had ROM only - you needed external RAM.
The 6801's 128 bytes of on-chip RAM made true single-chip
computers possible for the first time.

This chip is the ancestor of the legendary 68HC11.

Key innovations:
- 128 bytes on-chip RAM (first!)
- Hardware multiply (8x8=16)
- Full-duplex UART
- 16-bit timer
- 6800 instruction superset

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

class Motorola6801QueueModel:
    """Grey-box queueing model for Motorola 6801."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_mhz = self.config['architecture']['clock_frequency_mhz']
        self._compute_service_times()
    
    def _compute_service_times(self):
        """Calculate average service time based on instruction mix."""
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Weighted average
        self.avg_service_time = (
            mix['register_ops'] * timings['inherent'] +
            mix['memory_ops'] * (timings['direct'] + timings['extended']) / 2 +
            mix['io_ops'] * timings['direct'] +
            mix['branch_jump'] * timings['extended'] +
            mix['other'] * timings['indexed']
        )
    
    def _mm1_metrics(self, name: str, arrival_rate: float, 
                     service_time: float) -> QueueMetrics:
        """Calculate M/M/1 queue metrics."""
        utilization = arrival_rate * service_time
        
        if utilization >= 1.0:
            return QueueMetrics(name, arrival_rate, service_time, 1.0,
                              float('inf'), float('inf'), float('inf'))
        
        queue_length = utilization / (1 - utilization)
        wait_time = service_time / (1 - utilization)
        
        return QueueMetrics(name, arrival_rate, service_time, utilization,
                          queue_length, wait_time, wait_time)
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """Predict IPC for given arrival rate."""
        metrics = self._mm1_metrics('Execute', arrival_rate, self.avg_service_time)
        
        if metrics.utilization >= 1.0:
            return 0.0, [metrics]
        
        cpi = metrics.response_time
        ipc = 1.0 / cpi if cpi > 0 else 0.0
        
        return ipc, [metrics]
    
    def calibrate(self, measured_ipc: float, tolerance: float = 3.0) -> Dict:
        """Calibrate model to measured IPC."""
        best_rate = 0.08
        for rate in np.linspace(0.05, 0.12, 50):
            ipc, _ = self.predict_ipc(rate)
            if abs(ipc - measured_ipc) / measured_ipc < tolerance / 100:
                best_rate = rate
                break
        
        final_ipc, _ = self.predict_ipc(best_rate)
        error = abs(final_ipc - measured_ipc) / measured_ipc * 100
        
        return {
            'converged': error < tolerance,
            'arrival_rate': best_rate,
            'predicted_ipc': final_ipc,
            'error_percent': error
        }
    
    def compare_6800(self) -> Dict:
        """Compare to original 6800."""
        return {
            '6800': {
                'year': 1974,
                'on_chip_ram': 'None',
                'on_chip_rom': 'None', 
                'multiply': 'Software (100+ cycles)',
                'uart': 'External ACIA chip',
                'single_chip': False
            },
            '6801': {
                'year': 1978,
                'on_chip_ram': '128 bytes',
                'on_chip_rom': '2KB',
                'multiply': 'Hardware (10 cycles)',
                'uart': 'On-chip SCI',
                'single_chip': True
            },
            'improvement': '6801 = true single-chip computer'
        }

def main():
    model = Motorola6801QueueModel('motorola_6801_model.json')
    
    print("Motorola 6801 (1978) - First MCU with On-Chip RAM!")
    print("=" * 60)
    print("128 bytes RAM + 2KB ROM + UART + Timer = Single-chip computer")
    print()
    
    for rate in [0.05, 0.07, 0.09]:
        ipc, metrics = model.predict_ipc(rate)
        print(f"λ={rate:.2f}: IPC={ipc:.4f}, ρ={metrics[0].utilization:.3f}")
    
    print("\n6801 vs 6800:")
    comp = model.compare_6800()
    print(f"  6800: No on-chip RAM, external UART needed")
    print(f"  6801: {comp['6801']['on_chip_ram']} RAM, on-chip UART")
    print(f"  Result: {comp['improvement']}")

if __name__ == "__main__":
    main()
