#!/usr/bin/env python3
"""
ARM2 CPU Queueing Model (1986)

The first production ARM processor, powering the Acorn Archimedes -
the fastest personal computer of its time.

Improvements over ARM1:
- Hardware multiplier (vs microcode)
- Coprocessor interface (for FPA10 FPU)
- SWP instruction (atomic swap for semaphores)
- Higher clocks (up to 12 MHz)
- Smaller process (2µm vs 3µm)

The Archimedes with ARM2 outperformed the Amiga, Atari ST,
and Mac of the era in raw CPU benchmarks.

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

class ARM2QueueModel:
    """Three-stage RISC pipeline model for ARM2."""
    
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
        
        # Execute - now with hardware multiplier!
        self.execute_service = (
            mix['data_processing'] * timings['data_processing'] +
            mix['load_store'] * np.mean([timings['load_word'], timings['store_word']]) +
            mix['branch'] * timings['branch'] +
            mix['multiply'] * timings['multiply_32'] +  # Hardware multiplier!
            mix['other'] * 2.0
        )
        
        self.queue_efficiency = 0.91
    
    # ============================================================
    # AUTO-GENERATED METHOD STUBS - Implement these!
    # ============================================================

def analyze(self, workload: str = 'typical') -> 'AnalysisResult':
        """
        Analyze processor performance for given workload.
        
        Args:
            workload: Workload profile name ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, bottleneck analysis
        """
        raise NotImplementedError("Implement analyze() method")
    
def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known timing data.
        
        Returns:
            Dictionary with test results and pass/fail status
        """
        raise NotImplementedError("Implement validate() method")
    
def get_instruction_categories(self) -> Dict[str, 'InstructionCategory']:
        """
        Return instruction category definitions.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        raise NotImplementedError("Implement get_instruction_categories() method")
    
def get_workload_profiles(self) -> Dict[str, 'WorkloadProfile']:
        """
        Return workload profile definitions.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        raise NotImplementedError("Implement get_workload_profiles() method")

    # ============================================================
    # AUTO-GENERATED METHOD STUBS - Implement these!
    # ============================================================

def analyze(self, workload: str = 'typical') -> 'AnalysisResult':
        """
        Analyze processor performance for given workload.
        
        Args:
            workload: Workload profile name ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, bottleneck analysis
        """
        raise NotImplementedError("Implement analyze() method")
    
def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known timing data.
        
        Returns:
            Dictionary with test results and pass/fail status
        """
        raise NotImplementedError("Implement validate() method")
    
def get_instruction_categories(self) -> Dict[str, 'InstructionCategory']:
        """
        Return instruction category definitions.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        raise NotImplementedError("Implement get_instruction_categories() method")
    
def get_workload_profiles(self) -> Dict[str, 'WorkloadProfile']:
        """
        Return workload profile definitions.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        raise NotImplementedError("Implement get_workload_profiles() method")

    # ============================================================
    # AUTO-GENERATED METHOD STUBS - Implement these!
    # ============================================================

def analyze(self, workload: str = 'typical') -> 'AnalysisResult':
        """
        Analyze processor performance for given workload.
        
        Args:
            workload: Workload profile name ('typical', 'compute', 'memory', 'control')
            
        Returns:
            AnalysisResult with IPC, CPI, bottleneck analysis
        """
        raise NotImplementedError("Implement analyze() method")
    
def validate(self) -> Dict[str, Any]:
        """
        Run validation tests against known timing data.
        
        Returns:
            Dictionary with test results and pass/fail status
        """
        raise NotImplementedError("Implement validate() method")
    
def get_instruction_categories(self) -> Dict[str, 'InstructionCategory']:
        """
        Return instruction category definitions.
        
        Returns:
            Dictionary mapping category name to InstructionCategory
        """
        raise NotImplementedError("Implement get_instruction_categories() method")
    
def get_workload_profiles(self) -> Dict[str, 'WorkloadProfile']:
        """
        Return workload profile definitions.
        
        Returns:
            Dictionary mapping profile name to WorkloadProfile
        """
        raise NotImplementedError("Implement get_workload_profiles() method")

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
        efficiency = self.queue_efficiency * (1.0 - 0.07)
        ipc = arrival_rate * efficiency
        max_ipc = 1.0 / max(m.service_time for m in metrics)
        return min(ipc, max_ipc), metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        low, high = 0.2, 0.85
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
    
    def compare_arm1(self) -> Dict:
        """Compare ARM2 to ARM1."""
        ipc_arm2, _ = self.predict_ipc(0.50)
        return {
            'ARM2': {
                'year': 1986, 'transistors': self.transistors,
                'ipc': ipc_arm2, 'clock_mhz': self.clock_freq_mhz,
                'mips': ipc_arm2 * self.clock_freq_mhz,
                'multiplier': 'Hardware (8 cycles)',
                'coprocessor': 'Yes'
            },
            'ARM1': {
                'year': 1985, 'transistors': 25000,
                'ipc': 0.65, 'clock_mhz': 8,
                'mips': 0.65 * 8,
                'multiplier': 'Microcode (16 cycles)',
                'coprocessor': 'No'
            },
            'improvements': [
                'Hardware multiplier (2× faster multiply)',
                'Coprocessor interface',
                'SWP instruction',
                'Higher clock speeds',
                'Production-ready'
            ]
        }
    
    def compare_1987_competitors(self) -> Dict:
        """Compare to 1987 competition (Amiga, Atari ST, Mac)."""
        ipc, _ = self.predict_ipc(0.50)
        arm2_mips = ipc * 8
        
        return {
            'Archimedes_ARM2': {
                'cpu': 'ARM2 @ 8 MHz',
                'mips': arm2_mips,
                'notes': 'Fastest personal computer CPU'
            },
            'Amiga_500': {
                'cpu': '68000 @ 7.16 MHz',
                'mips': 0.7,
                'notes': 'Great graphics/sound'
            },
            'Atari_ST': {
                'cpu': '68000 @ 8 MHz',
                'mips': 0.8,
                'notes': 'Popular in Europe'
            },
            'Mac_Plus': {
                'cpu': '68000 @ 8 MHz',
                'mips': 0.8,
                'notes': 'GUI pioneer'
            },
            'conclusion': f'ARM2 was {arm2_mips/0.8:.1f}× faster than 68000!'
        }

def main():
    model = ARM2QueueModel('arm2_model.json')
    print("ARM2 (1986) - First Production ARM")
    print("=" * 60)
    print("Powered the Acorn Archimedes - fastest PC of its time")
    print()
    
    print(f"Transistors: {model.transistors:,}")
    print(f"Clock: {model.clock_freq_mhz:.0f} MHz")
    print()
    
    for rate in [0.40, 0.50, 0.60, 0.70]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.65)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp_arm1 = model.compare_arm1()
    print(f"\nvs ARM1:")
    for improvement in comp_arm1['improvements']:
        print(f"  + {improvement}")
    
    comp_1987 = model.compare_1987_competitors()
    print(f"\n1987 Competition:")
    print(f"  Archimedes (ARM2): {comp_1987['Archimedes_ARM2']['mips']:.1f} MIPS")
    print(f"  Amiga 500 (68000): {comp_1987['Amiga_500']['mips']:.1f} MIPS")
    print(f"  {comp_1987['conclusion']}")

if __name__ == "__main__":
    main()
