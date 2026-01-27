#!/usr/bin/env python3
"""
Intel 8080 CPU Queueing Model

This model represents the baseline 8-bit microprocessor architecture:
- Pure sequential execution (no pipeline)
- No instruction prefetch
- No cache hierarchy  
- 8-bit data bus
- Simple accumulator-based architecture

The 8080 serves as the historical baseline for understanding
architectural evolution to more complex processors.

Author: Grey-Box Performance Modeling Research
Date: January 24, 2026
Target CPU: Intel 8080 (1974-1990)
"""

import json
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class QueueMetrics:
    """Metrics for a single queue/stage"""
    name: str
    arrival_rate: float  # λ (instructions/cycle)
    service_time: float  # S (cycles/instruction)
    utilization: float  # ρ = λ × S
    queue_length: float  # L = ρ / (1 - ρ)
    wait_time: float  # W = S / (1 - ρ)
    response_time: float  # R = W + S


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


class Intel8080QueueModel:
    """
    Queueing network model for Intel 8080 CPU.
    
    Architecture Overview:
    =====================
    The 8080 is the simplest microprocessor in our model collection:
    - NO pipeline (purely sequential)
    - NO prefetch queue
    - NO cache
    - NO branch prediction
    - NO out-of-order execution
    
    Execution Model:
    ===============
    Each instruction proceeds through two sequential stages:
    
    1. Fetch Stage:
       ┌─────────────────────────────────────┐
       │ Fetch instruction bytes from memory │
       │ - 1-3 bytes per instruction         │
       │ - 8-bit bus (1 byte/cycle)          │
       │ - Average: 4 cycles                 │
       └─────────────────┬───────────────────┘
                         │
                         ↓
    2. Decode/Execute Stage:
       ┌─────────────────────────────────────┐
       │ Decode and execute instruction      │
       │ - Register ops: fast (4-5 cycles)   │
       │ - Memory ops: slow (7-13 cycles)    │
       │ - Control flow: variable            │
       └─────────────────────────────────────┘
    
    Queueing Model:
    ==============
    Modeled as TWO M/M/1 queues in series:
    
    λ → [Fetch Queue] → [Decode/Execute Queue] → Completed
    
    The 8080's sequential nature means:
    - No parallelism between stages
    - One instruction completes before next starts
    - Total time = Fetch time + Execute time
    - Very low IPC (typically 0.15-0.25)
    
    Why This Model Matters:
    =====================
    The 8080 establishes the baseline for understanding:
    - Performance gains from pipelining (8086+)
    - Benefits of prefetch queues (8086+)
    - Impact of wider buses (8086: 16-bit)
    - Value of caching (80386+)
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract architecture parameters
        arch = self.config['architecture']
        self.clock_freq_mhz = arch['clock_frequency_mhz']
        self.data_bus_width = arch['data_bus_width_bits']
        
        # Pipeline stages (really just sequential stages)
        stages = self.config['pipeline_stages']
        self.fetch_base_cycles = stages['fetch']['base_cycles']
        self.execute_base_cycles = stages['decode_execute']['base_cycles']
        
        # Instruction mix
        mix = self.config['instruction_mix']
        self.p_mov = mix['mov_register']
        self.p_alu = mix['alu_operations']
        self.p_load_store = mix['load_store']
        self.p_jump_call = mix['jump_call']
        self.p_io = mix['io_operations']
        
        # Instruction timings
        timings = self.config['instruction_timings']
        self.mov_reg_cycles = timings['mov_register_register']['cycles']
        self.mov_mem_cycles = timings['mov_memory']['cycles']
        self.alu_reg_cycles = timings['alu_register']['cycles']
        self.alu_mem_cycles = timings['alu_memory']['cycles']
        self.load_store_avg_cycles = np.mean([
            timings['load_store']['lxi'],
            timings['load_store']['lda'],
            timings['load_store']['sta']
        ])
        self.jump_avg_cycles = np.mean([
            timings['jump']['jmp'],
            timings['jump']['conditional_jump_taken'],
            timings['jump']['conditional_jump_not_taken']
        ])
        self.call_ret_avg_cycles = np.mean([
            timings['call_return']['call'],
            timings['call_return']['ret']
        ])
        self.io_cycles = timings['io']['in']
        
        # Memory system
        mem = self.config['memory_system']
        self.memory_access_cycles = mem['memory_access_cycles']
        
        # Instruction length distribution
        inst_len = self.config['instruction_length_distribution']
        self.avg_instruction_bytes = inst_len['average_bytes']
    
    def compute_fetch_service_time(self) -> float:
        """
        Compute average fetch time for 8080 instructions.
        
        8080 characteristics:
        - Instructions are 1-3 bytes
        - 8-bit bus fetches 1 byte per cycle
        - Average instruction is 1.75 bytes
        - Fetch time = instruction_bytes × bus_cycle_time
        
        Returns:
            Average cycles to fetch an instruction
        """
        # Base fetch time depends on instruction length
        # 8-bit bus means 1 byte per memory cycle
        # Add memory access latency
        fetch_cycles = self.avg_instruction_bytes * self.memory_access_cycles
        return fetch_cycles
    
    def compute_execute_service_time(self) -> float:
        """
        Compute average execution time for 8080 instructions.
        
        Weighted average based on instruction mix:
        - MOV operations (register and memory)
        - ALU operations (register and memory)
        - Load/Store operations
        - Control flow (jumps, calls)
        - I/O operations
        
        Returns:
            Average cycles to execute an instruction
        """
        # MOV instructions (mix of register and memory)
        # Most MOVs are register-to-register (fast)
        mov_avg = 0.85 * self.mov_reg_cycles + 0.15 * self.mov_mem_cycles
        
        # ALU instructions (mostly register operands)
        alu_avg = 0.85 * self.alu_reg_cycles + 0.15 * self.alu_mem_cycles
        
        # For jump/call, most are simple jumps not calls
        jump_call_avg = 0.80 * self.jump_avg_cycles + 0.20 * self.call_ret_avg_cycles
        
        # Weighted average across all instruction types
        weighted_cycles = (
            self.p_mov * mov_avg +
            self.p_alu * alu_avg +
            self.p_load_store * self.load_store_avg_cycles +
            self.p_jump_call * jump_call_avg +
            self.p_io * self.io_cycles
        )
        
        return weighted_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for both stages (fetch and execute).
        
        For the 8080, these stages are truly sequential:
        - Fetch completes first
        - Then execute completes
        - No overlap (no pipeline)
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/cycle)
        
        Returns:
            List of QueueMetrics for each stage
        """
        metrics = []
        
        # Stage 1: Fetch
        fetch_service_time = self.compute_fetch_service_time()
        fetch_util = arrival_rate * fetch_service_time
        
        if fetch_util >= 1.0:
            fetch_queue_length = float('inf')
            fetch_wait_time = float('inf')
        else:
            fetch_queue_length = fetch_util / (1 - fetch_util)
            fetch_wait_time = fetch_service_time / (1 - fetch_util)
        
        fetch_response_time = fetch_wait_time + fetch_service_time
        
        metrics.append(QueueMetrics(
            name="Fetch",
            arrival_rate=arrival_rate,
            service_time=fetch_service_time,
            utilization=fetch_util,
            queue_length=fetch_queue_length,
            wait_time=fetch_wait_time,
            response_time=fetch_response_time
        ))
        
        # Stage 2: Decode/Execute
        execute_service_time = self.compute_execute_service_time()
        execute_util = arrival_rate * execute_service_time
        
        if execute_util >= 1.0:
            execute_queue_length = float('inf')
            execute_wait_time = float('inf')
        else:
            execute_queue_length = execute_util / (1 - execute_util)
            execute_wait_time = execute_service_time / (1 - execute_util)
        
        execute_response_time = execute_wait_time + execute_service_time
        
        metrics.append(QueueMetrics(
            name="Decode_Execute",
            arrival_rate=arrival_rate,
            service_time=execute_service_time,
            utilization=execute_util,
            queue_length=execute_queue_length,
            wait_time=execute_wait_time,
            response_time=execute_response_time
        ))
        
        return metrics
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given arrival rate.
        
        For the 8080, IPC is low because:
        - Sequential execution (no pipeline overlap)
        - Multi-cycle instructions
        - No prefetch or speculation
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        # Check for instability
        max_util = max(m.utilization for m in metrics)
        if max_util >= 1.0:
            return 0.0, metrics
        
        # For sequential execution, total time is sum of stage times
        # IPC = 1 / total_time
        total_response_time = sum(m.response_time for m in metrics)
        
        # IPC is throughput relative to clock
        # With sequential stages, IPC = arrival_rate if stable
        # But constrained by bottleneck
        predicted_ipc = arrival_rate if max_util < 1.0 else 0.0
        
        # More accurately, for series queues:
        # IPC ≈ 1 / total_service_time (at low utilization)
        # IPC ≈ arrival_rate (at moderate utilization, if stable)
        # We'll use a model that interpolates based on utilization
        
        avg_utilization = np.mean([m.utilization for m in metrics])
        efficiency = 1.0 / (1.0 + avg_utilization)
        predicted_ipc = arrival_rate * efficiency
        
        # Cap at theoretical maximum (which is very low for 8080)
        # Maximum IPC ≈ 1 / (fetch_time + execute_time)
        total_service_time = sum(m.service_time for m in metrics)
        max_theoretical_ipc = 1.0 / total_service_time if total_service_time > 0 else 0.0
        predicted_ipc = min(predicted_ipc, max_theoretical_ipc)
        
        return predicted_ipc, metrics
    
    def find_bottleneck(self, metrics: List[QueueMetrics]) -> str:
        """Identify bottleneck stage (highest utilization)."""
        bottleneck = max(metrics, key=lambda m: m.utilization)
        return bottleneck.name
    
    def calibrate(self,
                  measured_ipc: float,
                  initial_arrival_rate: float = 0.10,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Uses binary search on arrival rate to find the arrival rate
        that produces the measured IPC.
        
        Args:
            measured_ipc: IPC measured from real 8080 system
            initial_arrival_rate: Starting point for search
            tolerance_percent: Convergence tolerance (%)
            max_iterations: Maximum calibration iterations
        
        Returns:
            CalibrationResult with final parameters and metrics
        """
        # Calculate maximum stable arrival rate
        fetch_service = self.compute_fetch_service_time()
        execute_service = self.compute_execute_service_time()
        max_stable_rate = min(0.95 / fetch_service, 0.95 / execute_service)
        
        low = 0.01
        high = min(0.4, max_stable_rate)  # Don't exceed stable rate
        arrival_rate = min(initial_arrival_rate, high * 0.9)
        
        best_error = float('inf')
        best_rate = arrival_rate
        best_metrics = None
        best_ipc = 0.0
        
        for iteration in range(max_iterations):
            predicted_ipc, metrics = self.predict_ipc(arrival_rate)
            
            if predicted_ipc == 0.0:
                # System is unstable, reduce arrival rate
                high = arrival_rate
                arrival_rate = (low + high) / 2.0
                continue
                
            error_percent = abs(predicted_ipc - measured_ipc) / measured_ipc * 100
            
            if error_percent < best_error:
                best_error = error_percent
                best_rate = arrival_rate
                best_metrics = metrics
                best_ipc = predicted_ipc
            
            if error_percent <= tolerance_percent:
                return CalibrationResult(
                    predicted_ipc=predicted_ipc,
                    measured_ipc=measured_ipc,
                    error_percent=error_percent,
                    iterations=iteration + 1,
                    converged=True,
                    bottleneck_stage=self.find_bottleneck(metrics),
                    stage_metrics=metrics
                )
            
            # Binary search
            if predicted_ipc < measured_ipc:
                low = arrival_rate
            else:
                high = arrival_rate
            
            arrival_rate = (low + high) / 2.0
            
            # Check convergence
            if abs(high - low) < 1e-6:
                break
        
        # Return best result found
        return CalibrationResult(
            predicted_ipc=best_ipc,
            measured_ipc=measured_ipc,
            error_percent=best_error,
            iterations=max_iterations,
            converged=best_error <= tolerance_percent,
            bottleneck_stage=best_metrics and self.find_bottleneck(best_metrics) or "Unknown",
            stage_metrics=best_metrics or []
        )
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Intel 8080 CPU Pipeline Metrics")
        print("="*80)
        print(f"{'Stage':<25} {'λ':>8} {'S':>8} {'ρ':>8} {'L':>8} {'W':>8} {'R':>8}")
        print(f"{'':25} {'(ins/c)':>8} {'(cyc)':>8} {'':>8} {'(ins)':>8} {'(cyc)':>8} {'(cyc)':>8}")
        print("-"*80)
        
        for m in metrics:
            l_str = f"{m.queue_length:.2f}" if m.queue_length != float('inf') else "inf"
            w_str = f"{m.wait_time:.2f}" if m.wait_time != float('inf') else "inf"
            r_str = f"{m.response_time:.2f}" if m.response_time != float('inf') else "inf"
            
            print(f"{m.name:<25} {m.arrival_rate:>8.4f} {m.service_time:>8.2f} "
                  f"{m.utilization:>8.4f} {l_str:>8} {w_str:>8} {r_str:>8}")
        
        print("="*80)
        
        # Print bottleneck
        bottleneck = max(metrics, key=lambda m: m.utilization)
        print(f"\nBottleneck: {bottleneck.name} (ρ = {bottleneck.utilization:.4f})")
        
        # Print total metrics
        avg_utilization = np.mean([m.utilization for m in metrics])
        total_service_time = sum(m.service_time for m in metrics)
        
        print(f"\nTotal Service Time: {total_service_time:.2f} cycles")
        print(f"Average Utilization: {avg_utilization:.4f}")
        print(f"Maximum Theoretical IPC: {1.0/total_service_time:.4f}")
        
        # Get arrival rate from first metric
        arrival_rate = metrics[0].arrival_rate
        efficiency = 1.0 / (1.0 + avg_utilization)
        predicted_ipc = arrival_rate * efficiency
        predicted_ipc = min(predicted_ipc, 1.0/total_service_time)
        
        print(f"Predicted IPC: {predicted_ipc:.4f}")
        print()


def main():
    """Example usage of the 8080 model."""
    print("Intel 8080 CPU Queueing Model")
    print("="*80)
    print("The 8080: The Baseline Sequential Processor")
    print("="*80)
    
    # Load model
    model = Intel8080QueueModel('8080_cpu_model.json')
    
    # Example 1: Predict IPC at different arrival rates
    print("\nExample 1: IPC Prediction at Different Load Levels")
    print("-"*80)
    for arrival_rate in [0.10, 0.15, 0.20, 0.25]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        bottleneck = model.find_bottleneck(metrics)
        print(f"Arrival Rate: {arrival_rate:.2f} → IPC: {ipc:.4f}, "
              f"Bottleneck: {bottleneck}")
    
    # Example 2: Full metrics at moderate load
    print("\nExample 2: Detailed Metrics at Typical Load (λ=0.15)")
    ipc, metrics = model.predict_ipc(0.15)
    model.print_metrics(metrics)
    
    # Example 3: Architecture comparison context
    print("\nExample 3: Understanding 8080 Limitations")
    print("-"*80)
    print("The 8080 is sequential - it has NO:")
    print("  ✗ Pipeline overlap")
    print("  ✗ Instruction prefetch")
    print("  ✗ Cache hierarchy")
    print("  ✗ Branch prediction")
    print("  ✗ Out-of-order execution")
    print("\nThis makes it the perfect baseline to understand")
    print("performance gains in later processors:")
    print("  - 8086: Adds prefetch queue → ~2x speedup")
    print("  - 80286: Adds pipeline → ~3x speedup")
    print("  - 80386: Adds cache → ~5x speedup")
    
    # Example 4: Calibration
    print("\nExample 4: Model Calibration")
    print("-"*80)
    measured_ipc = 0.06  # Conservative 8080 IPC at moderate load
    result = model.calibrate(measured_ipc, tolerance_percent=2.0)
    
    print(f"Target IPC: {result.measured_ipc:.4f}")
    print(f"Predicted IPC: {result.predicted_ipc:.4f}")
    print(f"Error: {result.error_percent:.2f}%")
    print(f"Iterations: {result.iterations}")
    print(f"Converged: {result.converged}")
    print(f"Bottleneck: {result.bottleneck_stage}")
    
    # Example 5: Historical context
    print("\nExample 5: Historical Significance")
    print("-"*80)
    historical = model.config['historical_context']
    print(f"Introduced: {historical['year_introduced']}")
    print(f"Significance: {historical['significance']}")
    print(f"Common Systems: {', '.join(historical['common_systems'])}")
    print(f"Successor: {historical['successor']}")
    
    print("\n" + "="*80)
    print("The 8080 laid the foundation for the x86 architecture family.")
    print("Understanding its limitations helps us appreciate modern CPU design.")
    print("="*80)


if __name__ == "__main__":
    main()
