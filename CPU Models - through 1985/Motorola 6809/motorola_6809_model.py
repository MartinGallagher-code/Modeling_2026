#!/usr/bin/env python3
"""
Motorola 6809 CPU Queueing Model

The 6809 represents the pinnacle of 8-bit processor design:
- Most orthogonal instruction set
- 13 addressing modes
- Hardware multiply
- Dual stack pointers
- Position-independent code support
- Elegant, consistent architecture

Despite technical superiority, it never achieved mainstream success,
proving that "best technology doesn't always win."

Author: Grey-Box Performance Modeling Research
Date: January 24, 2026
Target CPU: Motorola 6809/6809E (1978-1995)
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


class Motorola6809QueueModel:
    """
    Queueing network model for Motorola 6809 CPU.
    
    Architecture Overview:
    =====================
    The 6809 is the most elegant 8-bit processor ever designed:
    
    Key Features:
    - Orthogonal instruction set (any op works with any mode)
    - 13 addressing modes (most of any 8-bit CPU)
    - Hardware multiply (11 cycles vs 100+ in software)
    - Dual stack pointers (S and U)
    - Native 16-bit operations (D = A:B)
    - PC-relative addressing (position-independent code)
    - Two full 16-bit index registers (X, Y)
    
    Design Philosophy:
    ==================
    "Any operation should work with any addressing mode"
    
    This is the opposite of accumulator-centric designs (8080, Z80)
    and more symmetric than the 6502.
    
    Execution Model:
    ===============
    Despite advanced features, still sequential execution:
    
    ┌─────────────────────────────────────┐
    │ Fetch-Decode-Execute                │
    │ - Variable instruction length       │
    │ - 1-5 bytes per instruction         │
    │ - Average: ~4.5 cycles/instruction  │
    │ - Better than 8080/Z80 efficiency   │
    └─────────────────────────────────────┘
    
    Queueing Model:
    ==============
    SINGLE M/M/1 queue (simpler than modeling 8080's two stages):
    
    λ → [Fetch-Decode-Execute] → Completed
    
    The 6809's orthogonality means we can model it as a single
    efficient stage rather than separate fetch/execute.
    
    Performance Characteristics:
    ===========================
    - Cycles/instruction: ~4.5 (better than 8080's ~12)
    - Code density: Excellent (orthogonality reduces instructions)
    - IPC: ~0.08-0.10 (better than 8080/Z80's 0.07)
    - BUT: Slow clock (1 MHz typical vs Z80's 4 MHz)
    - Result: Lower absolute performance despite better efficiency
    
    Why 6809 Matters:
    ================
    The 6809 proves important lessons:
    1. Best technology doesn't always win
    2. Timing and ecosystem matter more than technical excellence
    3. Orthogonal design enables higher efficiency
    4. Late to market = limited success
    """
    
    def __init__(self, config_file: str):
        """Initialize model from JSON configuration file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract architecture parameters
        arch = self.config['architecture']
        self.clock_freq_mhz = arch.get('typical_clock_mhz', 1.0)
        self.data_bus_width = arch['data_bus_width_bits']
        
        # Instruction mix
        mix = self.config['instruction_mix']
        self.p_load_store = mix['load_store']
        self.p_alu = mix['alu_operations']
        self.p_branch = mix['branch_jump']
        self.p_stack = mix['stack_operations']
        self.p_indexed = mix['indexed_operations']
        self.p_multiply = mix['multiply']
        self.p_other = mix['other']
        
        # Instruction timings
        timings = self.config['instruction_timings']
        
        # Load/store average
        ls = timings['load_store']
        self.load_store_avg = np.mean([
            ls['lda_immediate'],
            ls['lda_direct'],
            ls['lda_extended'],
            ls['lda_indexed'],
            ls['sta_direct'],
            ls['lda_indexed']
        ])
        
        # ALU average (8-bit)
        alu = timings['alu_register']
        self.alu_avg = np.mean([
            alu['add_immediate'],
            alu['add_direct'],
            alu['add_extended'],
            alu['add_indexed']
        ])
        
        # ALU 16-bit average
        alu16 = timings['alu_16bit']
        self.alu16_avg = np.mean([
            alu16['addd_immediate'],
            alu16['addd_direct'],
            alu16['addd_extended']
        ])
        
        # Branch/jump average
        branch = timings['branch']
        self.branch_avg = np.mean([
            branch['bra'],
            branch['beq'],
            branch['lbra']
        ])
        
        # Jump/call average
        jc = timings['jump_call']
        self.jump_call_avg = np.mean([
            jc['jsr_direct'],
            jc['jsr_extended'],
            jc['rts'],
            jc['bsr']
        ])
        
        # Stack operations
        stack = timings['stack']
        self.stack_avg = stack['pshs']
        
        # Multiply (hardware!)
        self.multiply_cycles = timings['multiply']['mul']
        
        # Indexed operations
        indexed = timings['indexed']
        self.indexed_avg = indexed['leax']
        
        # Instruction length
        inst_len = self.config['instruction_length_distribution']
        self.avg_instruction_bytes = inst_len['average_bytes']
        
        # Performance characteristics
        perf = self.config['performance_characteristics']
        self.cycles_per_instruction_avg = perf['cycles_per_instruction_avg']
    
    def compute_service_time(self) -> float:
        """
        Compute average service time for 6809 instructions.
        
        The 6809's orthogonal design means most instructions
        execute efficiently with consistent timing across
        addressing modes.
        
        Key advantages:
        - Indexed addressing as fast as direct
        - 16-bit operations built-in
        - Hardware multiply (11 cycles!)
        - Efficient stack operations
        
        Returns:
            Average cycles to execute an instruction
        """
        # Mix of 8-bit and 16-bit ALU (assume 80% 8-bit, 20% 16-bit)
        alu_weighted = 0.80 * self.alu_avg + 0.20 * self.alu16_avg
        
        # Branch mix (80% short branches, 20% long jumps/calls)
        branch_weighted = 0.80 * self.branch_avg + 0.20 * self.jump_call_avg
        
        # Weighted average across instruction types
        weighted_cycles = (
            self.p_load_store * self.load_store_avg +
            self.p_alu * alu_weighted +
            self.p_branch * branch_weighted +
            self.p_stack * self.stack_avg +
            self.p_indexed * self.indexed_avg +
            self.p_multiply * self.multiply_cycles +
            self.p_other * 5.0  # Misc instructions
        )
        
        return weighted_cycles
    
    def compute_stage_metrics(self, arrival_rate: float) -> List[QueueMetrics]:
        """
        Compute metrics for the 6809 execution stage.
        
        Unlike 8080/Z80, we model the 6809 as a single unified
        stage because its orthogonal design makes fetch/execute
        less distinct.
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/cycle)
        
        Returns:
            List with single QueueMetrics for unified execution
        """
        service_time = self.compute_service_time()
        utilization = arrival_rate * service_time
        
        if utilization >= 1.0:
            queue_length = float('inf')
            wait_time = float('inf')
        else:
            queue_length = utilization / (1 - utilization)
            wait_time = service_time / (1 - utilization)
        
        response_time = wait_time + service_time
        
        return [QueueMetrics(
            name="Execution",
            arrival_rate=arrival_rate,
            service_time=service_time,
            utilization=utilization,
            queue_length=queue_length,
            wait_time=wait_time,
            response_time=response_time
        )]
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given arrival rate.
        
        The 6809 should achieve better IPC than 8080/Z80 due to:
        - More efficient instruction set
        - Better code density
        - Faster indexed addressing
        - Hardware multiply
        
        Expected range: 0.08-0.10 vs 8080/Z80's 0.07
        
        Returns:
            (predicted_ipc, stage_metrics)
        """
        metrics = self.compute_stage_metrics(arrival_rate)
        
        # Check for instability
        if metrics[0].utilization >= 1.0:
            return 0.0, metrics
        
        # For single stage, IPC calculation is simpler
        utilization = metrics[0].utilization
        efficiency = 1.0 / (1.0 + utilization)
        predicted_ipc = arrival_rate * efficiency
        
        # Cap at theoretical maximum
        max_theoretical_ipc = 1.0 / metrics[0].service_time
        predicted_ipc = min(predicted_ipc, max_theoretical_ipc)
        
        return predicted_ipc, metrics
    
    def calibrate(self,
                  measured_ipc: float,
                  initial_arrival_rate: float = 0.18,
                  tolerance_percent: float = 2.0,
                  max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Uses binary search on arrival rate.
        
        Args:
            measured_ipc: IPC measured from real 6809 system
            initial_arrival_rate: Starting point for search
            tolerance_percent: Convergence tolerance (%)
            max_iterations: Maximum calibration iterations
        
        Returns:
            CalibrationResult with final parameters and metrics
        """
        service_time = self.compute_service_time()
        max_stable_rate = 0.95 / service_time
        
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
                    bottleneck_stage=metrics[0].name,
                    stage_metrics=metrics
                )
            
            # Binary search
            if predicted_ipc < measured_ipc:
                low = arrival_rate
            else:
                high = arrival_rate
            
            arrival_rate = (low + high) / 2.0
            
            if abs(high - low) < 1e-6:
                break
        
        return CalibrationResult(
            predicted_ipc=best_ipc,
            measured_ipc=measured_ipc,
            error_percent=best_error,
            iterations=max_iterations,
            converged=best_error <= tolerance_percent,
            bottleneck_stage=best_metrics[0].name if best_metrics else "Unknown",
            stage_metrics=best_metrics or []
        )
    
    def compare_with_competitors(self) -> Dict:
        """
        Compare 6809 with Z80, 8080, and 6502.
        
        Returns:
            Dictionary with comparative performance
        """
        test_arrival_rate = 0.15
        
        # 6809 performance
        m6809_ipc, m6809_metrics = self.predict_ipc(test_arrival_rate)
        m6809_service = m6809_metrics[0].service_time
        
        # Competitors (estimated from their models)
        competitors = {
            '8080': {'ipc': 0.069, 'service': 12.25, 'clock': 2.0},
            'Z80': {'ipc': 0.068, 'service': 12.60, 'clock': 4.0},
            '6502': {'ipc': 0.080, 'service': 3.5, 'clock': 1.0}
        }
        
        # Calculate real performance (MIPS)
        m6809_mips = m6809_ipc * self.clock_freq_mhz
        
        comparison = {
            'arrival_rate': test_arrival_rate,
            '6809': {
                'ipc': m6809_ipc,
                'service_time': m6809_service,
                'clock_mhz': self.clock_freq_mhz,
                'mips': m6809_mips
            }
        }
        
        for name, data in competitors.items():
            comp_mips = data['ipc'] * data['clock']
            comparison[name] = {
                'ipc': data['ipc'],
                'service_time': data['service'],
                'clock_mhz': data['clock'],
                'mips': comp_mips,
                'vs_6809_ipc': m6809_ipc / data['ipc'],
                'vs_6809_mips': m6809_mips / comp_mips
            }
        
        return comparison
    
    def analyze_advantages(self) -> Dict:
        """
        Analyze 6809's architectural advantages.
        
        Returns:
            Dictionary quantifying advantages
        """
        service_time = self.compute_service_time()
        
        # Hardware multiply advantage
        software_multiply_cycles = 100  # Typical for 8080/Z80
        multiply_speedup = software_multiply_cycles / self.multiply_cycles
        
        # Indexed addressing advantage
        # 6809: indexed same cost as direct (~4 cycles)
        # 8080/Z80: indexed much more expensive (~10-15 cycles)
        indexed_speedup = 12.0 / 4.0  # Rough estimate
        
        # Code density (bytes per instruction)
        # 6809: ~2.1 bytes/instruction
        # 8080/Z80: ~1.8 bytes/instruction  
        # But 6809 needs fewer instructions due to orthogonality
        instructions_ratio = 0.85  # 6809 needs ~15% fewer instructions
        
        return {
            'service_time_cycles': service_time,
            'hardware_multiply': {
                'cycles_6809': self.multiply_cycles,
                'cycles_software': software_multiply_cycles,
                'speedup': multiply_speedup
            },
            'indexed_addressing': {
                'cycles_6809': 4.0,
                'cycles_8080_z80': 12.0,
                'speedup': indexed_speedup
            },
            'code_efficiency': {
                'bytes_per_instruction': self.avg_instruction_bytes,
                'instructions_ratio_vs_8080': instructions_ratio,
                'net_code_size': self.avg_instruction_bytes * instructions_ratio
            },
            'orthogonality_benefit': 'Consistent, predictable performance',
            'dual_stacks_benefit': 'Better for multitasking and recursion',
            'position_independent_code': 'PC-relative addressing enables relocatable code'
        }
    
    def print_metrics(self, metrics: List[QueueMetrics]):
        """Pretty print stage metrics."""
        print("\n" + "="*80)
        print("Motorola 6809 CPU Performance Metrics")
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
        
        # Print key metrics
        total_service_time = sum(m.service_time for m in metrics)
        print(f"\nService Time: {total_service_time:.2f} cycles/instruction")
        print(f"Maximum Theoretical IPC: {1.0/total_service_time:.4f}")
        print(f"Better than 8080 ({1.0/12.25:.4f}) and Z80 ({1.0/12.60:.4f})")
        
        arrival_rate = metrics[0].arrival_rate
        predicted_ipc, _ = self.predict_ipc(arrival_rate)
        print(f"Predicted IPC at λ={arrival_rate:.3f}: {predicted_ipc:.4f}")
        print()


def main():
    """Example usage of the 6809 model."""
    print("Motorola 6809 CPU Queueing Model")
    print("="*80)
    print("The Most Elegant 8-Bit Processor That Never Achieved Dominance")
    print("="*80)
    
    # Load model
    model = Motorola6809QueueModel('motorola_6809_model.json')
    
    # Example 1: Basic prediction
    print("\nExample 1: IPC Prediction at Different Load Levels")
    print("-"*80)
    for arrival_rate in [0.10, 0.15, 0.20, 0.25]:
        ipc, metrics = model.predict_ipc(arrival_rate)
        print(f"Arrival Rate: {arrival_rate:.2f} → IPC: {ipc:.4f}")
    
    # Example 2: Detailed metrics
    print("\nExample 2: Detailed Metrics at Typical Load (λ=0.18)")
    ipc, metrics = model.predict_ipc(0.18)
    model.print_metrics(metrics)
    
    # Example 3: Comparison with competitors
    print("\nExample 3: 6809 vs Competitors (8080, Z80, 6502)")
    print("-"*80)
    comparison = model.compare_with_competitors()
    
    print(f"Test Configuration: λ = {comparison['arrival_rate']:.2f} instructions/cycle\n")
    
    for cpu in ['6809', '8080', 'Z80', '6502']:
        data = comparison[cpu]
        print(f"{cpu:>6s}: IPC={data['ipc']:.4f}, Clock={data['clock_mhz']:.1f}MHz, "
              f"MIPS={data['mips']:.3f}")
        if cpu != '6809':
            print(f"        vs 6809: IPC {data['vs_6809_ipc']:.2f}×, "
                  f"Real performance {data['vs_6809_mips']:.2f}×")
    
    print("\nKey Insight: 6809 has best per-cycle efficiency but slowest clock!")
    
    # Example 4: Architectural advantages
    print("\nExample 4: 6809 Architectural Advantages")
    print("-"*80)
    advantages = model.analyze_advantages()
    
    print(f"Hardware Multiply:")
    print(f"  6809: {advantages['hardware_multiply']['cycles_6809']} cycles")
    print(f"  Software (8080/Z80): {advantages['hardware_multiply']['cycles_software']} cycles")
    print(f"  Speedup: {advantages['hardware_multiply']['speedup']:.1f}×")
    
    print(f"\nIndexed Addressing:")
    print(f"  6809: {advantages['indexed_addressing']['cycles_6809']:.0f} cycles (same as direct!)")
    print(f"  8080/Z80: {advantages['indexed_addressing']['cycles_8080_z80']:.0f} cycles")
    print(f"  Speedup: {advantages['indexed_addressing']['speedup']:.1f}×")
    
    print(f"\nCode Efficiency:")
    print(f"  Bytes/instruction: {advantages['code_efficiency']['bytes_per_instruction']:.2f}")
    print(f"  Fewer instructions needed: {(1-advantages['code_efficiency']['instructions_ratio_vs_8080'])*100:.0f}%")
    print(f"  Net code size vs 8080: {advantages['code_efficiency']['net_code_size']:.2f} bytes/instruction")
    
    # Example 5: Calibration
    print("\nExample 5: Model Calibration")
    print("-"*80)
    measured_ipc = 0.085  # Typical 6809 IPC
    result = model.calibrate(measured_ipc, tolerance_percent=2.0)
    
    print(f"Target IPC: {result.measured_ipc:.4f}")
    print(f"Predicted IPC: {result.predicted_ipc:.4f}")
    print(f"Error: {result.error_percent:.2f}%")
    print(f"Iterations: {result.iterations}")
    print(f"Converged: {result.converged}")
    
    # Example 6: Why 6809 matters
    print("\nExample 6: Why the 6809 Matters")
    print("-"*80)
    why_matters = model.config['why_6809_matters']
    for key, value in why_matters.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "="*80)
    print("The 6809 proves: Best technology doesn't always win.")
    print("Timing, ecosystem, and market positioning matter more than")
    print("technical excellence. But its influence lives on in RISC design.")
    print("="*80)


if __name__ == "__main__":
    main()
