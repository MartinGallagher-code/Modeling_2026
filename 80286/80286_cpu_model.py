#!/usr/bin/env python3
"""
Intel 80286 CPU Queueing Model

This model extends the simple 5-stage pipeline to include the 80286's
architectural advances:
- 6-byte instruction prefetch queue (parallel with execution)
- Memory Management Unit (MMU) with address translation
- Protection checks (privilege levels)
- Separate Bus Interface Unit (BIU) and Execution Unit (EU)

Author: Grey-Box Performance Modeling Research
Date: January 23, 2026
Target CPU: Intel 80286 (1982)
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ProtectionLevel(Enum):
    """80286 Protection Ring Levels"""
    KERNEL = 0      # Ring 0 - OS kernel
    SYSTEM = 1      # Ring 1 - OS services
    SERVICES = 2    # Ring 2 - System services
    USER = 3        # Ring 3 - User applications


@dataclass
class QueueMetrics:
    """Metrics for a single queue/stage"""
    name: str
    arrival_rate: float      # λ (instructions/cycle)
    service_time: float      # S (cycles/instruction)
    utilization: float       # ρ = λ × S
    queue_length: float      # L = ρ / (1 - ρ)
    wait_time: float         # W = S / (1 - ρ)
    response_time: float     # R = W + S


@dataclass
class CalibrationResult:
    """Results from model calibration"""
    predicted_ipc: float
    measured_ipc: float
    error_percent: float
    iterations: int
    converged: bool
    bottleneck_stage: str
    stage_metrics: List[QueueMetrics]


class Intel80286QueueModel:
    """
    Queueing network model for Intel 80286 CPU.
    
    Architecture:
    ============
    
    BIU (Bus Interface Unit) - Parallel Operation:
    ┌─────────────────────────────────────┐
    │  Prefetch Queue (6 bytes)           │
    │  - Fetches ahead of execution       │
    │  - M/M/1/6 queue (bounded capacity) │
    │  - Parallel with EU                 │
    └─────────────────┬───────────────────┘
                      │ Instructions
                      ↓
    EU (Execution Unit) - Series Pipeline:
    ┌─────────────────────────────────────┐
    │  Stage 1: Decode + Address Calc     │
    │  - Decode instruction               │
    │  - Calculate effective address      │
    │  - MMU address translation          │
    │  - Protection checks                │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 2: Execute                   │
    │  - ALU operations                   │
    │  - Multiply/Divide                  │
    │  - Effective 3-4 clocks faster      │
    │    than 8086 per instruction        │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 3: Memory Access             │
    │  - Load/Store through BIU           │
    │  - Protected memory access          │
    │  - Contention with prefetch         │
    └─────────────────┬───────────────────┘
                      ↓
    ┌─────────────────────────────────────┐
    │  Stage 4: Write Back                │
    │  - Update registers                 │
    │  - Update flags                     │
    └─────────────────────────────────────┘
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract key parameters
        self.clock_freq_mhz = self.config['architecture']['clock_frequency_mhz']
        self.prefetch_queue_size = self.config['architecture']['prefetch_queue_size']
        
        # Pipeline stage base latencies (cycles)
        stages = self.config['pipeline_stages']
        self.decode_cycles = stages['decode_and_address_calc']['base_cycles']
        self.execute_cycles = stages['execute']['base_cycles']
        self.memory_cycles = stages['memory_access']['base_cycles']
        self.writeback_cycles = stages['writeback']['base_cycles']
        
        # Instruction mix
        mix = self.config['instruction_mix']
        self.p_alu = mix['alu']
        self.p_mul = mix['multiply']
        self.p_div = mix['divide']
        self.p_load = mix['load']
        self.p_store = mix['store']
        self.p_branch = mix['branch']
        self.p_protected = mix['protected_mode_ops']
        
        # Memory system
        mem = self.config['memory_system']
        self.mem_access_cycles = mem['memory_access_cycles']
        
        # Protection overhead
        prot = self.config['protection_overhead']
        self.mmu_translation_cycles = prot['mmu_translation_cycles']
        self.privilege_check_cycles = prot['privilege_check_cycles']
        self.p_privilege_check = prot['privilege_check_probability']
        
        # Performance characteristics
        perf = self.config['performance']
        self.effective_speedup_vs_8086 = perf['effective_speedup_vs_8086']
        
    def compute_prefetch_metrics(self, arrival_rate: float) -> QueueMetrics:
        """
        Compute metrics for the prefetch queue (BIU).
        
        This is modeled as an M/M/1/K queue (bounded capacity).
        The prefetch unit runs in parallel with execution.
        """
        # Service time = memory access time to fetch instruction bytes
        # Assume average instruction is 2.5 bytes, prefetch fetches 2 bytes at a time
        service_time = self.mem_access_cycles / 2.0
        
        # For bounded queue M/M/1/K, use modified formulas
        K = self.prefetch_queue_size
        rho = arrival_rate * service_time
        
        if rho >= 1.0:
            # At or over capacity
            utilization = 1.0
            queue_length = K / 2.0
            wait_time = queue_length / arrival_rate
        else:
            # Standard M/M/1/K formulas
            utilization = rho
            if abs(rho - 1.0) < 1e-6:
                queue_length = K / 2.0
            else:
                # L = ρ(1 - (K+1)ρ^K + Kρ^(K+1)) / ((1-ρ)(1-ρ^(K+1)))
                numerator = rho * (1 - (K+1) * (rho**K) + K * (rho**(K+1)))
                denominator = (1 - rho) * (1 - rho**(K+1))
                queue_length = numerator / denominator
            
            wait_time = queue_length / arrival_rate if arrival_rate > 0 else 0
        
        response_time = wait_time + service_time
        
        return QueueMetrics(
            name="Prefetch_Queue_BIU",
            arrival_rate=arrival_rate,
            service_time=service_time,
            utilization=utilization,
            queue_length=queue_length,
            wait_time=wait_time,
            response_time=response_time
        )
    
    def compute_decode_service_time(self) -> float:
        """
        Compute service time for decode + address calculation stage.
        
        80286 improvements:
        - Faster decode than 8086
        - MMU address translation (protected mode)
        - Privilege checks
        """
        base_decode = self.decode_cycles
        
        # Add MMU translation overhead for protected mode operations
        mmu_overhead = self.p_protected * self.mmu_translation_cycles
        
        # Add privilege check overhead
        privilege_overhead = self.p_privilege_check * self.privilege_check_cycles
        
        total = base_decode + mmu_overhead + privilege_overhead
        return total
    
    def compute_execute_service_time(self) -> float:
        """
        Compute service time for execution stage.
        
        Weighted by instruction type.
        80286 is ~3-4x faster per instruction than 8086.
        """
        # Base cycles for different instruction types
        alu_cycles = self.execute_cycles
        mul_cycles = 13  # 80286 multiply (16-bit) - reduced from 21
        div_cycles = 17  # 80286 divide (16-bit) - reduced from 25
        
        # Weighted average
        weighted_cycles = (
            self.p_alu * alu_cycles +
            self.p_mul * mul_cycles +
            self.p_div * div_cycles +
            (1 - self.p_alu - self.p_mul - self.p_div) * alu_cycles
        )
        
        return weighted_cycles
    
    def compute_memory_service_time(self) -> float:
        """
        Compute service time for memory access stage.
        
        Accounts for:
        - Load/store probability
        - Memory access latency
        - BIU contention with prefetch
        """
        p_memory = self.p_load + self.p_store
        
        if p_memory == 0:
            return 0.1  # Minimal passthrough time
        
        # Base memory access
        base_mem = self.memory_cycles
        
        # Add contention penalty (prefetch competes for bus)
        # Model as additional 10% overhead when prefetch is active
        contention_factor = 1.1
        
        # Effective service time
        service_time = p_memory * base_mem * contention_factor
        
        return max(service_time, 0.1)
    
    def compute_writeback_service_time(self) -> float:
        """Compute service time for writeback stage."""
        return self.writeback_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for all pipeline stages.
        
        Uses M/M/1 queueing for each stage (except prefetch which is M/M/1/K).
        """
        metrics = []
        
        # Stage 1: Prefetch Queue (parallel, bounded)
        prefetch = self.compute_prefetch_metrics(arrival_rate)
        metrics.append(prefetch)
        
        # Stages 2-5: Series pipeline (EU)
        stage_configs = [
            ("Decode_Address_MMU", self.compute_decode_service_time()),
            ("Execute", self.compute_execute_service_time()),
            ("Memory_Access", self.compute_memory_service_time()),
            ("Writeback", self.compute_writeback_service_time())
        ]
        
        for name, service_time in stage_configs:
            utilization = arrival_rate * service_time
            
            if utilization >= 1.0:
                # Saturated queue
                queue_length = float('inf')
                wait_time = float('inf')
            else:
                # Standard M/M/1 formulas
                queue_length = utilization / (1 - utilization)
                wait_time = service_time / (1 - utilization)
            
            response_time = wait_time + service_time
            
            metrics.append(QueueMetrics(
                name=name,
                arrival_rate=arrival_rate,
                service_time=service_time,
                utilization=utilization,
                queue_length=queue_length,
                wait_time=wait_time,
                response_time=response_time
            ))
        
        return metrics
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC (Instructions Per Cycle) for given arrival rate.
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        # Find the bottleneck stage
        max_util = max(m.utilization for m in metrics)
        
        # If system is unstable (any stage saturated), IPC = 0
        if max_util >= 1.0:
            return 0.0, metrics
        
        # For in-order pipeline, throughput is limited by slowest stage
        # IPC = min(1/S_i) across all stages, adjusted for utilization
        
        # The actual instruction completion rate is limited by the bottleneck
        bottleneck = max(metrics, key=lambda m: m.utilization)
        
        # Effective IPC = arrival_rate (what goes in = what comes out, in steady state)
        # But arrival rate itself was set by us - need different approach
        
        # Instead: CPI = sum of service times (baseline) + queuing delays
        eu_stages = [m for m in metrics if m.name != "Prefetch_Queue_BIU"]
        
        # Base CPI from service times
        base_cpi = sum(m.service_time for m in eu_stages)
        
        # Add queuing overhead proportional to utilization
        queuing_overhead = sum(m.service_time * m.utilization / (1 - m.utilization) 
                              for m in eu_stages if m.utilization < 1.0)
        
        total_cpi = base_cpi + queuing_overhead
        
        # Check if prefetch is significant bottleneck
        prefetch = metrics[0]
        if prefetch.utilization > 0.95:
            # Prefetch stalling significantly, add penalty
            total_cpi += prefetch.service_time * 0.5
        
        # IPC = 1 / CPI
        if total_cpi == 0 or total_cpi == float('inf'):
            predicted_ipc = 0.0
        else:
            predicted_ipc = 1.0 / total_cpi
        
        return predicted_ipc, metrics
    
    def find_bottleneck(self, metrics: List[QueueMetrics]) -> str:
        """Identify the bottleneck stage (highest utilization)."""
        bottleneck = max(metrics, key=lambda m: m.utilization)
        return bottleneck.name
    
    def calibrate(self, 
                  measured_ipc: float,
                  initial_arrival_rate: float = 0.5,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Uses binary search to find arrival rate that produces target IPC.
        
        Args:
            measured_ipc: Target IPC from real measurements
            initial_arrival_rate: Starting guess (instructions/cycle)
            tolerance_percent: Acceptable error percentage
            max_iterations: Maximum calibration iterations
        
        Returns:
            CalibrationResult with predicted IPC and metrics
        """
        # Binary search bounds
        low = 0.01
        high = 0.95  # Cannot exceed 1.0 (one instruction per cycle max for in-order)
        arrival_rate = initial_arrival_rate
        
        best_error = float('inf')
        best_rate = arrival_rate
        best_metrics = None
        
        for iteration in range(max_iterations):
            predicted_ipc, metrics = self.predict_ipc(arrival_rate)
            
            error_percent = abs(predicted_ipc - measured_ipc) / measured_ipc * 100
            
            if error_percent < best_error:
                best_error = error_percent
                best_rate = arrival_rate
                best_metrics = metrics
            
            if error_percent <= tolerance_percent:
                # Converged
                return CalibrationResult(
                    predicted_ipc=predicted_ipc,
                    measured_ipc=measured_ipc,
                    error_percent=error_percent,
                    iterations=iteration + 1,
                    converged=True,
                    bottleneck_stage=self.find_bottleneck(metrics),
                    stage_metrics=metrics
                )
            
            # Binary search adjustment
            if predicted_ipc < measured_ipc:
                # Need higher arrival rate
                low = arrival_rate
            else:
                # Need lower arrival rate
                high = arrival_rate
            
            arrival_rate = (low + high) / 2.0
            
            # Check for convergence stall
            if abs(high - low) < 1e-6:
                break
        
        # Did not converge within tolerance
        return CalibrationResult(
            predicted_ipc=best_metrics and (1.0 / sum(m.wait_time for m in best_metrics[1:])),
            measured_ipc=measured_ipc,
            error_percent=best_error,
            iterations=max_iterations,
            converged=False,
            bottleneck_stage=best_metrics and self.find_bottleneck(best_metrics),
            stage_metrics=best_metrics or []
        )
    
    def sensitivity_analysis(self, 
                            base_arrival_rate: float,
                            parameter_name: str,
                            delta_percent: float = 10.0) -> Dict[str, float]:
        """
        Perform sensitivity analysis on a parameter.
        
        Args:
            base_arrival_rate: Baseline arrival rate
            parameter_name: Name of parameter to vary
            delta_percent: Percentage change to apply
        
        Returns:
            Dictionary with sensitivity metrics
        """
        # Get baseline IPC
        base_ipc, _ = self.predict_ipc(base_arrival_rate)
        
        # Store original value
        original_value = None
        
        # Modify parameter (simplified - you'd extend this for all parameters)
        if parameter_name == 'memory_cycles':
            original_value = self.memory_cycles
            self.memory_cycles *= (1 + delta_percent / 100.0)
        elif parameter_name == 'mmu_translation_cycles':
            original_value = self.mmu_translation_cycles
            self.mmu_translation_cycles *= (1 + delta_percent / 100.0)
        else:
            return {"error": f"Unknown parameter: {parameter_name}"}
        
        # Get modified IPC
        modified_ipc, _ = self.predict_ipc(base_arrival_rate)
        
        # Restore original value
        if parameter_name == 'memory_cycles':
            self.memory_cycles = original_value
        elif parameter_name == 'mmu_translation_cycles':
            self.mmu_translation_cycles = original_value
        
        # Calculate sensitivity
        ipc_change_percent = (modified_ipc - base_ipc) / base_ipc * 100
        sensitivity = ipc_change_percent / delta_percent
        
        return {
            'parameter': parameter_name,
            'base_value': original_value,
            'modified_value': original_value * (1 + delta_percent / 100.0),
            'base_ipc': base_ipc,
            'modified_ipc': modified_ipc,
            'ipc_change_percent': ipc_change_percent,
            'sensitivity': sensitivity
        }
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Intel 80286 CPU Pipeline Metrics")
        print("="*80)
        print(f"{'Stage':<25} {'λ':>8} {'S':>8} {'ρ':>8} {'L':>8} {'W':>8} {'R':>8}")
        print(f"{'':25} {'(ins/c)':>8} {'(cyc)':>8} {'':>8} {'(ins)':>8} {'(cyc)':>8} {'(cyc)':>8}")
        print("-"*80)
        
        for m in metrics:
            print(f"{m.name:<25} {m.arrival_rate:>8.4f} {m.service_time:>8.2f} "
                  f"{m.utilization:>8.4f} {m.queue_length:>8.2f} "
                  f"{m.wait_time:>8.2f} {m.response_time:>8.2f}")
        
        print("="*80)
        
        # Print bottleneck
        bottleneck = max(metrics, key=lambda m: m.utilization)
        print(f"\nBottleneck: {bottleneck.name} (ρ = {bottleneck.utilization:.4f})")
        
        # Print total CPI and IPC
        eu_stages = [m for m in metrics if m.name != "Prefetch_Queue_BIU"]
        total_cpi = sum(m.wait_time for m in eu_stages)
        ipc = 1.0 / total_cpi if total_cpi > 0 else 0
        print(f"Total CPI: {total_cpi:.4f}")
        print(f"Predicted IPC: {ipc:.4f}")
        print()


def main():
    """Example usage of the 80286 model."""
    print("Intel 80286 CPU Queueing Model")
    print("="*80)
    
    # Load model
    model = Intel80286QueueModel('80286_cpu_model.json')
    
    # Example 1: Predict IPC at different arrival rates
    print("\nExample 1: IPC Prediction at Different Load Levels")
    print("-"*80)
    
    for arrival_rate in [0.3, 0.5, 0.7, 0.9]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        bottleneck = model.find_bottleneck(metrics)
        print(f"Arrival Rate: {arrival_rate:.2f} → IPC: {ipc:.4f}, "
              f"Bottleneck: {bottleneck}")
    
    # Example 2: Full metrics at moderate load
    print("\nExample 2: Detailed Metrics at 50% Load")
    ipc, metrics = model.predict_ipc(0.5)
    model.print_metrics(metrics)
    
    # Example 3: Calibration
    print("\nExample 3: Model Calibration")
    print("-"*80)
    measured_ipc = 0.65  # Example measured IPC
    result = model.calibrate(measured_ipc, tolerance_percent=2.0)
    
    print(f"Target IPC: {result.measured_ipc:.4f}")
    print(f"Predicted IPC: {result.predicted_ipc:.4f}")
    print(f"Error: {result.error_percent:.2f}%")
    print(f"Iterations: {result.iterations}")
    print(f"Converged: {result.converged}")
    print(f"Bottleneck: {result.bottleneck_stage}")
    
    # Example 4: Sensitivity Analysis
    print("\nExample 4: Sensitivity Analysis")
    print("-"*80)
    
    for param in ['memory_cycles', 'mmu_translation_cycles']:
        sensitivity = model.sensitivity_analysis(0.5, param, delta_percent=10.0)
        print(f"\nParameter: {sensitivity['parameter']}")
        print(f"  Base Value: {sensitivity['base_value']:.2f}")
        print(f"  +10% Value: {sensitivity['modified_value']:.2f}")
        print(f"  IPC Change: {sensitivity['ipc_change_percent']:.2f}%")
        print(f"  Sensitivity: {sensitivity['sensitivity']:.3f}")


if __name__ == "__main__":
    main()
