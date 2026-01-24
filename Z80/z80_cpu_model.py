#!/usr/bin/env python3
"""
Zilog Z80 CPU Queueing Model

This model represents the enhanced 8-bit microprocessor:
- 8080-compatible but with improvements
- Additional registers (alternate set, IX, IY)
- Better instruction timings
- Enhanced instruction set (bit ops, block ops, relative jumps)
- Still sequential execution (no pipeline)

The Z80 demonstrates how microarchitectural improvements
can boost performance within the same basic architecture.

Author: Grey-Box Performance Modeling Research
Date: January 24, 2026
Target CPU: Zilog Z80 (1976-present)
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


class ZilogZ80QueueModel:
    """
    Queueing network model for Zilog Z80 CPU.
    
    Architecture Overview:
    =====================
    The Z80 is an enhanced 8080 with improvements:
    - Better instruction timings (many 4 cycles vs 8080's 5)
    - Alternate register set (fast context switches)
    - Index registers IX, IY (flexible addressing)
    - Enhanced instruction set (bit ops, block transfers)
    - Still sequential (NO pipeline)
    
    Key Difference from 8080:
    ========================
    While both are sequential, the Z80 executes faster:
    - MOV r,r: 4 cycles (vs 8080's 5 cycles)
    - Better microcode optimization
    - More registers reduce memory traffic
    
    This translates to:
    - 15-30% better IPC on typical code
    - Higher clock speeds (4 MHz vs 2 MHz)
    - Overall ~2-2.5× performance vs 8080
    
    Execution Model:
    ===============
    Two sequential stages (like 8080):
    
    1. Fetch Stage:
       ┌─────────────────────────────────────┐
       │ Fetch instruction bytes from memory │
       │ - 1-4 bytes per instruction         │
       │ - 8-bit bus (1 byte/cycle)          │
       │ - Average: 3-4 cycles               │
       └─────────────────┬───────────────────┘
                         │
                         ↓
    2. Decode/Execute Stage:
       ┌─────────────────────────────────────┐
       │ Decode and execute instruction      │
       │ - Generally faster than 8080        │
       │ - 4 cycles typical (vs 8080's 5)    │
       │ - Optimized microcode               │
       └─────────────────────────────────────┘
    
    Queueing Model:
    ==============
    TWO M/M/1 queues in series:
    
    λ → [Fetch Queue] → [Decode/Execute Queue] → Completed
    
    Performance vs 8080:
    ===================
    - 8080 IPC: 0.06-0.08 (at moderate load)
    - Z80 IPC: 0.09-0.12 (at moderate load)
    - Improvement: ~40-50% better throughput
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract architecture parameters
        arch = self.config['architecture']
        self.clock_freq_mhz = arch['clock_frequency_mhz']
        self.data_bus_width = arch['data_bus_width_bits']
        
        # Pipeline stages
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
        self.p_bit = mix['bit_operations']
        
        # Instruction timings
        timings = self.config['instruction_timings']
        self.mov_reg_cycles = timings['mov_register_register']['cycles']
        self.mov_mem_cycles = timings['mov_memory']['cycles']
        self.mov_indexed_cycles = timings['mov_indexed']['cycles']
        self.alu_reg_cycles = timings['alu_register']['cycles']
        self.alu_mem_cycles = timings['alu_memory']['cycles']
        self.alu_indexed_cycles = timings['alu_indexed']['cycles']
        
        # Load/store operations
        self.load_store_avg_cycles = np.mean([
            timings['load_store']['ld_nn'],
            timings['load_store']['ld_addr'],
            timings['load_store']['st_addr']
        ])
        
        # Jump operations (Z80 has relative jumps)
        self.jump_avg_cycles = np.mean([
            timings['jump']['jp'],
            timings['jump']['jr'],
            timings['jump']['jr_conditional_taken'],
            timings['jump']['jr_conditional_not_taken']
        ])
        
        self.call_ret_avg_cycles = np.mean([
            timings['call_return']['call'],
            timings['call_return']['ret']
        ])
        
        self.io_cycles = timings['io']['in']
        self.bit_op_cycles = timings['bit_operations']['bit']
        
        # Memory system
        mem = self.config['memory_system']
        self.memory_access_cycles = mem['memory_access_cycles']
        self.refresh_overhead = mem['refresh_overhead_percent'] / 100.0
        
        # Instruction length distribution
        inst_len = self.config['instruction_length_distribution']
        self.avg_instruction_bytes = inst_len['average_bytes']
    
    def compute_fetch_service_time(self) -> float:
        """
        Compute average fetch time for Z80 instructions.
        
        Z80 characteristics:
        - Instructions are 1-4 bytes (longer than 8080 due to IX/IY prefixes)
        - 8-bit bus fetches 1 byte per cycle
        - Average instruction is 1.82 bytes
        - Includes DRAM refresh overhead (~2%)
        
        Returns:
            Average cycles to fetch an instruction
        """
        # Base fetch time depends on instruction length
        fetch_cycles = self.avg_instruction_bytes * self.memory_access_cycles
        
        # Add DRAM refresh overhead (Z80 has built-in refresh)
        fetch_cycles *= (1.0 + self.refresh_overhead)
        
        return fetch_cycles
    
    def compute_execute_service_time(self) -> float:
        """
        Compute average execution time for Z80 instructions.
        
        Z80 improvements over 8080:
        - Faster register operations (4 vs 5 cycles)
        - Alternate registers reduce memory access
        - But indexed addressing adds overhead when used
        
        Weighted average based on instruction mix.
        
        Returns:
            Average cycles to execute an instruction
        """
        # MOV instructions
        # Z80 code uses LOTS of register-to-register moves (very fast at 4 cycles)
        # Very few indexed moves (slow at 19 cycles)
        # Assume: 92% register, 6% memory, 2% indexed
        mov_avg = (0.92 * self.mov_reg_cycles + 
                   0.06 * self.mov_mem_cycles +
                   0.02 * self.mov_indexed_cycles)
        
        # ALU instructions
        # Similar: mostly register ops
        # Assume: 92% register, 7% memory, 1% indexed
        alu_avg = (0.92 * self.alu_reg_cycles + 
                   0.07 * self.alu_mem_cycles +
                   0.01 * self.alu_indexed_cycles)
        
        # Jump/call instructions
        # Z80 has relative jumps (JR) which are efficient
        # Calls are less common
        jump_call_avg = 0.80 * self.jump_avg_cycles + 0.20 * self.call_ret_avg_cycles
        
        # Weighted average across all instruction types
        weighted_cycles = (
            self.p_mov * mov_avg +
            self.p_alu * alu_avg +
            self.p_load_store * self.load_store_avg_cycles +
            self.p_jump_call * jump_call_avg +
            self.p_io * self.io_cycles +
            self.p_bit * self.bit_op_cycles
        )
        
        return weighted_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for both stages (fetch and execute).
        
        For the Z80, these stages are sequential like 8080:
        - Fetch completes first
        - Then execute completes
        - No overlap (no pipeline)
        
        But both stages are faster than 8080.
        
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
        
        For the Z80, IPC is better than 8080 because:
        - Faster instruction execution (better microcode)
        - More efficient use of registers
        - But still sequential (no pipeline)
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        # Check for instability
        max_util = max(m.utilization for m in metrics)
        if max_util >= 1.0:
            return 0.0, metrics
        
        # For sequential execution with series queues
        avg_utilization = np.mean([m.utilization for m in metrics])
        efficiency = 1.0 / (1.0 + avg_utilization)
        predicted_ipc = arrival_rate * efficiency
        
        # Cap at theoretical maximum
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
                  initial_arrival_rate: float = 0.18,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Uses binary search on arrival rate to find the arrival rate
        that produces the measured IPC.
        
        Args:
            measured_ipc: IPC measured from real Z80 system
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
        high = min(0.5, max_stable_rate)
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
    
    def compare_with_8080(self) -> Dict:
        """
        Compare Z80 performance with 8080.
        
        Returns:
            Dictionary with performance comparison
        """
        # Typical arrival rate for both processors
        test_arrival_rate = 0.12
        
        # Z80 performance
        z80_ipc, z80_metrics = self.predict_ipc(test_arrival_rate)
        z80_service_time = sum(m.service_time for m in z80_metrics)
        
        # Estimate 8080 performance
        # 8080 has slower timings: ~5.25 fetch, ~7.0 execute
        i8080_fetch_service = 5.25
        i8080_execute_service = 7.0
        i8080_total_service = i8080_fetch_service + i8080_execute_service
        
        # 8080 IPC at same arrival rate
        i8080_fetch_util = test_arrival_rate * i8080_fetch_service
        i8080_execute_util = test_arrival_rate * i8080_execute_service
        i8080_avg_util = (i8080_fetch_util + i8080_execute_util) / 2.0
        
        if i8080_avg_util < 1.0:
            i8080_efficiency = 1.0 / (1.0 + i8080_avg_util)
            i8080_ipc = test_arrival_rate * i8080_efficiency
            i8080_ipc = min(i8080_ipc, 1.0 / i8080_total_service)
        else:
            i8080_ipc = 0.0
        
        return {
            'arrival_rate': test_arrival_rate,
            'z80_ipc': z80_ipc,
            'z80_service_time': z80_service_time,
            'i8080_ipc': i8080_ipc,
            'i8080_service_time': i8080_total_service,
            'ipc_speedup': z80_ipc / i8080_ipc if i8080_ipc > 0 else 0,
            'service_time_improvement': i8080_total_service / z80_service_time if z80_service_time > 0 else 0,
            'z80_bottleneck': self.find_bottleneck(z80_metrics)
        }
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Zilog Z80 CPU Pipeline Metrics")
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
    """Example usage of the Z80 model."""
    print("Zilog Z80 CPU Queueing Model")
    print("="*80)
    print("The Z80: Enhanced 8080 with Better Performance")
    print("="*80)
    
    # Load model
    model = ZilogZ80QueueModel('z80_cpu_model.json')
    
    # Example 1: Predict IPC at different arrival rates
    print("\nExample 1: IPC Prediction at Different Load Levels")
    print("-"*80)
    for arrival_rate in [0.10, 0.15, 0.20, 0.25]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        bottleneck = model.find_bottleneck(metrics)
        print(f"Arrival Rate: {arrival_rate:.2f} → IPC: {ipc:.4f}, "
              f"Bottleneck: {bottleneck}")
    
    # Example 2: Full metrics at moderate load
    print("\nExample 2: Detailed Metrics at Typical Load (λ=0.18)")
    ipc, metrics = model.predict_ipc(0.18)
    model.print_metrics(metrics)
    
    # Example 3: Z80 vs 8080 comparison
    print("\nExample 3: Z80 vs Intel 8080 Performance Comparison")
    print("-"*80)
    comparison = model.compare_with_8080()
    print(f"Test Configuration: λ = {comparison['arrival_rate']:.2f} instructions/cycle")
    print(f"\nZ80 Performance:")
    print(f"  IPC: {comparison['z80_ipc']:.4f}")
    print(f"  Service Time: {comparison['z80_service_time']:.2f} cycles")
    print(f"  Bottleneck: {comparison['z80_bottleneck']}")
    print(f"\n8080 Performance (estimated):")
    print(f"  IPC: {comparison['i8080_ipc']:.4f}")
    print(f"  Service Time: {comparison['i8080_service_time']:.2f} cycles")
    print(f"\nZ80 Advantages:")
    print(f"  IPC Speedup: {comparison['ipc_speedup']:.2f}x")
    print(f"  Service Time Improvement: {comparison['service_time_improvement']:.2f}x faster")
    print(f"  Combined with 2x clock advantage (4 MHz vs 2 MHz):")
    print(f"  Overall speedup: ~{comparison['ipc_speedup'] * 2:.1f}x")
    
    # Example 4: Understanding Z80 enhancements
    print("\nExample 4: Z80 Architectural Enhancements Over 8080")
    print("-"*80)
    enhancements = model.config['enhancements_over_8080']
    for key, value in enhancements.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    # Example 5: Calibration
    print("\nExample 5: Model Calibration")
    print("-"*80)
    measured_ipc = 0.07  # Realistic Z80 IPC at moderate load
    result = model.calibrate(measured_ipc, tolerance_percent=2.0)
    
    print(f"Target IPC: {result.measured_ipc:.4f}")
    print(f"Predicted IPC: {result.predicted_ipc:.4f}")
    print(f"Error: {result.error_percent:.2f}%")
    print(f"Iterations: {result.iterations}")
    print(f"Converged: {result.converged}")
    print(f"Bottleneck: {result.bottleneck_stage}")
    
    # Example 6: Historical significance
    print("\nExample 6: Historical Significance")
    print("-"*80)
    historical = model.config['historical_context']
    print(f"Introduced: {historical['year_introduced']}")
    print(f"Designer: {historical['designer']}")
    print(f"Significance: {historical['significance']}")
    print(f"\nFamous Systems:")
    for system in historical['common_systems']:
        print(f"  • {system}")
    
    print("\n" + "="*80)
    print("The Z80 showed that microarchitectural improvements could")
    print("significantly boost performance while maintaining compatibility.")
    print("It dominated the home computer market throughout the 1980s.")
    print("="*80)


if __name__ == "__main__":
    main()
