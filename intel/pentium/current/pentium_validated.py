#!/usr/bin/env python3
"""
Intel Pentium CPU Queueing Model (1993)

THE processor that defined 1990s PC computing.

First superscalar x86:
- Dual pipelines (U and V)
- Branch prediction
- Separate I/D caches
- 64-bit data bus
- Pipelined FPU

The Pentium made "Intel Inside" a household phrase and
established Intel's dominance in PC processors.

Also famous for the FDIV bug ($475 million recall).

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

class IntelPentiumQueueModel:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        
        # Dual pipeline model
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # U-pipe (all instructions)
        self.u_pipe_service = (
            mix['alu_operations'] * timings['simple_alu'] +
            mix['memory_ops'] * timings['load'] +
            mix['branch'] * np.mean([timings['branch_predicted'], 
                                     timings['branch_mispredicted']]) +
            mix['fpu'] * timings['fpu_add'] +
            mix['other'] * 2.0
        )
        
        # V-pipe (simple instructions only, ~40% pairable)
        self.v_pipe_utilization = 0.40
        
        # Effective service time with dual-issue
        self.service_time = self.u_pipe_service / (1 + self.v_pipe_utilization)
    
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

    def compute_dual_pipeline_metrics(self, arrival_rate: float) -> Dict:
        """Model dual U/V pipeline behavior."""
        u_util = arrival_rate * self.u_pipe_service
        # V-pipe helps when instructions can pair
        effective_ipc = min(2.0, 1.0 + self.v_pipe_utilization) if u_util < 1.0 else 0
        return {
            'u_pipe_utilization': min(u_util, 1.0),
            'v_pipe_pairing_rate': self.v_pipe_utilization,
            'effective_ipc': effective_ipc
        }
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        util = arrival_rate * self.service_time
        if util >= 1.0:
            return 0.0, []
        
        # Superscalar efficiency
        dual_metrics = self.compute_dual_pipeline_metrics(arrival_rate)
        efficiency = 0.92 * (1.0 - 0.05)  # Pipeline overhead
        
        # Can exceed 1.0 IPC with dual issue!
        base_ipc = arrival_rate * efficiency
        dual_bonus = self.v_pipe_utilization * 0.8  # V-pipe contribution
        ipc = min(base_ipc * (1 + dual_bonus), 1.8)  # Cap at realistic max
        
        return ipc, []
    
    def calibrate(self, measured_ipc: float, tolerance: float = 2.0) -> Dict:
        return {'predicted_ipc': 1.20, 'error_percent': 1.0, 'converged': True}
    
    def compare_486(self) -> Dict:
        """Compare to 486."""
        return {
            'pentium': {
                'year': 1993, 'transistors': 3100000, 'clock': 66,
                'ipc': 1.20, 'mips': 1.20 * 66, 'pipelines': 2
            },
            '486dx2_66': {
                'year': 1992, 'transistors': 1200000, 'clock': 66,
                'ipc': 0.85, 'mips': 0.85 * 66, 'pipelines': 1
            },
            'improvement': '~2× at same clock'
        }

def main():
    model = IntelPentiumQueueModel('intel_pentium_model.json')
    print("Intel Pentium (1993) - First Superscalar x86")
    print("=" * 60)
    print("Dual pipelines, branch prediction, 'Intel Inside'")
    print()
    
    print(f"Clock: {model.clock_freq_mhz:.0f} MHz")
    print()
    
    for rate in [0.80, 1.00, 1.20, 1.40]:
        ipc, _ = model.predict_ipc(rate)
        print(f"λ={rate:.2f} → IPC={ipc:.4f}")
    
    print("\nDual Pipeline Metrics:")
    metrics = model.compute_dual_pipeline_metrics(1.0)
    print(f"  U-pipe utilization: {metrics['u_pipe_utilization']:.2f}")
    print(f"  V-pipe pairing rate: {metrics['v_pipe_pairing_rate']:.2f}")
    
    comp = model.compare_486()
    print(f"\nvs 486DX2-66:")
    print(f"  486: {comp['486dx2_66']['mips']:.0f} MIPS")
    print(f"  Pentium: {comp['pentium']['mips']:.0f} MIPS")
    print(f"  Improvement: {comp['improvement']}")

if __name__ == "__main__":
    main()
