#!/usr/bin/env python3
"""
Intel 80486 CPU Queueing Model (1989)

The 80486 brought RISC-like efficiency to x86:
- 5-stage pipeline (first x86 pipeline)
- On-chip 8KB unified cache
- On-chip FPU (8-10× faster than 80387)
- 1.2 million transistors
- Many instructions execute in 1 cycle

The 486 also pioneered clock doubling (DX2, DX4), allowing
faster CPUs on slower motherboards.

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

class Intel80486QueueModel:
    """Five-stage pipeline model with on-chip cache and FPU."""
    
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        self.transistors = self.config['architecture']['transistor_count']
        
        cache = self.config['cache_system']
        self.cache_hit_rate = cache['cache_hit_rate']
        self.hit_cycles = cache['hit_cycles']
        self.miss_cycles = cache['miss_cycles']
        
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # 5-stage pipeline service times
        # Prefetch with cache
        self.prefetch_service = (self.cache_hit_rate * self.hit_cycles + 
                                 (1 - self.cache_hit_rate) * self.miss_cycles)
        
        # Decode stages
        self.decode1_service = 1.0
        self.decode2_service = 0.8
        
        # Execute (with FPU for some)
        self.execute_service = (
            mix['move_operations'] * timings['mov_reg_reg'] +
            mix['alu_operations'] * timings['add_reg'] +
            mix['branch_jump'] * np.mean([timings['jcc_taken'], timings['jcc_not_taken']]) +
            mix['load_store'] * timings['mov_mem_reg'] +
            mix['floating_point'] * timings['fadd'] +
            mix['other'] * 2.0
        )
        
        # Writeback
        self.writeback_service = 0.5
        
        self.queue_efficiency = 0.93
    
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
            ("Prefetch", self.prefetch_service),
            ("Decode1", self.decode1_service),
            ("Decode2", self.decode2_service),
            ("Execute", self.execute_service),
            ("Writeback", self.writeback_service)
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
        efficiency = self.queue_efficiency * (1.0 - 0.05)
        ipc = arrival_rate * efficiency
        max_ipc = 1.0 / max(m.service_time for m in metrics)
        return min(ipc, max_ipc), metrics
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        low, high = 0.3, 0.95
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
    
    def compare_80386(self) -> Dict:
        """Compare to 80386."""
        ipc_486, _ = self.predict_ipc(0.55)
        return {
            '80486': {
                'year': 1989, 'transistors': self.transistors,
                'ipc': ipc_486, 'clock': self.clock_freq_mhz,
                'mips': ipc_486 * self.clock_freq_mhz,
                'pipeline': 5, 'cache': '8KB unified', 'fpu': 'On-chip'
            },
            '80386': {
                'year': 1985, 'transistors': 275000,
                'ipc': 0.40, 'clock': 25,
                'mips': 0.40 * 25,
                'pipeline': 'None', 'cache': 'None', 'fpu': 'External 80387'
            },
            'improvements': {
                'transistors': '4× more',
                'ipc': '2× better',
                'cache': '8KB on-chip',
                'fpu': '8-10× faster than 80387',
                'pipeline': '5 stages (first x86!)'
            }
        }
    
    def clock_variants(self) -> Dict:
        """Show clock-doubled variants."""
        ipc, _ = self.predict_ipc(0.55)
        return {
            '486DX-25': {'clock': 25, 'bus': 25, 'multiplier': 1, 'mips': ipc * 25},
            '486DX-33': {'clock': 33, 'bus': 33, 'multiplier': 1, 'mips': ipc * 33},
            '486DX2-50': {'clock': 50, 'bus': 25, 'multiplier': 2, 'mips': ipc * 50},
            '486DX2-66': {'clock': 66, 'bus': 33, 'multiplier': 2, 'mips': ipc * 66},
            '486DX4-100': {'clock': 100, 'bus': 33, 'multiplier': 3, 'mips': ipc * 100}
        }

def main():
    model = Intel80486QueueModel('intel_80486_model.json')
    print("Intel 80486 (1989) - RISC-like x86")
    print("=" * 60)
    print("First x86 with pipeline, on-chip cache, and FPU")
    print()
    
    print(f"Transistors: {model.transistors:,}")
    print(f"Clock: {model.clock_freq_mhz:.0f} MHz")
    print()
    
    for rate in [0.50, 0.60, 0.70, 0.80]:
        ipc, metrics = model.predict_ipc(rate)
        bn = max(metrics, key=lambda m: m.utilization).name
        print(f"λ={rate:.2f} → IPC={ipc:.4f}, Bottleneck: {bn}")
    
    result = model.calibrate(0.80)
    print(f"\nCalibration: IPC={result['predicted_ipc']:.4f}, Error={result['error_percent']:.2f}%")
    
    comp = model.compare_80386()
    print(f"\n486 vs 386:")
    for key, val in comp['improvements'].items():
        print(f"  {key}: {val}")
    
    print(f"\nClock Variants:")
    variants = model.clock_variants()
    for name, specs in variants.items():
        print(f"  {name}: {specs['clock']} MHz internal, {specs['mips']:.1f} MIPS")

if __name__ == "__main__":
    main()
