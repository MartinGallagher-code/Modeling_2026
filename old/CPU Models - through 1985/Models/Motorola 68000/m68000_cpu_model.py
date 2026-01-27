#!/usr/bin/env python3
"""
Motorola 68000 CPU Queueing Model
===================================

Grey-box queueing model for the Motorola 68000 microprocessor.

The 68000 uses a sophisticated architecture with:
- 2-word prefetch queue
- Variable-length instructions (2-10 bytes)
- Complex addressing modes
- 16-bit external bus, 32-bit internal
- Microcoded execution

This model captures the pipeline behavior using a series queueing network
with explicit prefetch queue modeling.

Key 68000 Features Modeled:
- Prefetch queue (2 words, overlapped operation)
- Effective address calculation (0-20 cycles overhead)
- Register-to-register operations (fast)
- Memory operations (4+ cycle bus access)
- Orthogonal addressing modes
- Variable instruction timing

Author: Grey-Box Performance Modeling Research
Date: January 23, 2026
Version: 1.0
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class PipelineStage(Enum):
    """68000 pipeline stages"""
    PF = "Prefetch"                # Prefetch queue filling
    ID = "Instruction_Decode"      # Decode instruction
    EA = "Effective_Address"       # Calculate effective address
    OF = "Operand_Fetch"          # Fetch operands
    EX = "Execute"                # Execute operation
    WB = "Write_Back"             # Write result


@dataclass
class QueueMetrics:
    """Metrics for a single queue (pipeline stage)"""
    stage: PipelineStage
    service_time: float         # Average service time (cycles)
    arrival_rate: float         # Lambda (instructions/second)
    utilization: float          # Rho = lambda * service_time
    queue_length: float         # Average number in queue (L)
    wait_time: float            # Average time in system (W)
    throughput: float           # Effective throughput


@dataclass
class SystemMetrics:
    """Overall CPU metrics"""
    total_cpi: float            # Cycles per instruction
    ipc: float                  # Instructions per cycle
    throughput: float           # Instructions per second
    bottleneck_stage: PipelineStage
    max_utilization: float
    stage_metrics: Dict[PipelineStage, QueueMetrics]


@dataclass
class CalibrationResult:
    """Result of model calibration"""
    converged: bool
    iterations: int
    final_error_percent: float
    calibrated_wait_states: float
    calibrated_prefetch_effectiveness: float
    predicted_ipc: float
    measured_ipc: float


class M68000QueueModel:
    """
    Queueing model for Motorola 68000 CPU.
    
    Models the 68000's prefetch queue and complex addressing modes
    as a series queueing network with conditional stages.
    """
    
    def __init__(self, config_path: str = 'm68000_cpu_model.json'):
        """Load 68000 configuration and initialize model"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq = self.config['timing']['clock_frequency_hz']
        self.clock_period_ns = self.config['timing']['clock_period_ns']
        
        # Extract instruction mix and timing
        self.instr_timing = self.config['instruction_timing']['categories']
        self._compute_weighted_execution_time()
        
        # Pipeline stage service times
        self.service_times = self._initialize_service_times()
        
        # Queueing parameters
        qp = self.config['queueing_parameters']
        self.lambda_instr = qp['arrival_rate']['lambda_instructions_per_second']
        
        # Prefetch queue parameters
        self.prefetch_effectiveness = self.config['prefetch_queue']['effectiveness']['sequential_code']
        
    def _compute_weighted_execution_time(self):
        """Compute weighted average execution time from instruction mix"""
        total_cycles = 0.0
        total_fraction = 0.0
        
        for category, data in self.instr_timing.items():
            fraction = data.get('fraction', 0.0)
            
            # Handle different timing specifications
            if category == 'register_to_register':
                # Mix of byte/word and longword
                cycles = 0.6 * data['cycles']['byte_word'] + 0.4 * data['cycles']['longword']
            elif category == 'immediate_to_register':
                cycles = 0.6 * data['cycles']['byte_word'] + 0.4 * data['cycles']['longword']
            elif category == 'memory_to_register':
                cycles = 0.6 * data['cycles']['byte_word'] + 0.4 * data['cycles']['longword']
                # Add average EA overhead
                avg_ea = 6  # Average across addressing modes
                cycles += avg_ea
            elif category == 'register_to_memory':
                cycles = 0.6 * data['cycles']['byte_word'] + 0.4 * data['cycles']['longword']
                cycles += 6  # EA overhead
            elif category == 'memory_to_memory':
                cycles = 0.6 * data['cycles']['byte_word'] + 0.4 * data['cycles']['longword']
                cycles += 12  # EA overhead for both operands
            elif category == 'arithmetic_logic':
                # Mix of register, immediate, and memory operations
                cycles = (0.5 * data['cycles']['register'] + 
                         0.3 * data['cycles']['immediate'] +
                         0.2 * data['cycles']['memory'])
            elif category == 'shift_rotate':
                # Average shift count of 4
                cycles = 0.7 * (6 + 2*4) + 0.3 * data['cycles_memory']
            elif category == 'multiply':
                cycles = data['cycles']['mulu']
            elif category == 'divide':
                cycles = data['cycles']['divu']
            elif category == 'branch':
                # Branch prediction
                p_taken = data.get('branch_taken_probability', 0.5)
                cycles = p_taken * data['cycles']['taken'] + (1 - p_taken) * data['cycles']['not_taken']
            elif category == 'jump_subroutine':
                # Mix of JSR and RTS
                cycles = 0.5 * data['cycles']['jsr'] + 0.5 * data['cycles']['rts']
            elif category == 'stack':
                # Average 4 registers saved/restored
                cycles = 8 + 4*4
            elif category == 'special':
                cycles = data['cycles']['lea']
            else:
                cycles = 8.0  # Default
            
            total_cycles += fraction * cycles
            total_fraction += fraction
        
        # Normalize if fractions don't sum to 1.0
        if total_fraction > 0:
            self.avg_execution_cycles = total_cycles / total_fraction
        else:
            self.avg_execution_cycles = 8.5  # Default from config
            
    def _initialize_service_times(self) -> Dict[PipelineStage, float]:
        """Initialize service times for each pipeline stage (in cycles)"""
        st = self.config['queueing_parameters']['service_times']
        
        return {
            PipelineStage.PF: st['PF']['effective_service'],
            PipelineStage.ID: st['ID']['base_cycles'],
            PipelineStage.EA: st['EA']['base_cycles'],
            PipelineStage.OF: st['OF']['base_cycles'],
            PipelineStage.EX: self.avg_execution_cycles,
            PipelineStage.WB: st['WB']['base_cycles']
        }
    
    def compute_stage_metrics(self, 
                             stage: PipelineStage,
                             arrival_rate: float,
                             service_time: float,
                             probability: float = 1.0) -> QueueMetrics:
        """
        Compute queueing metrics for a single stage.
        
        Uses M/M/1 queueing formulas with conditional execution probability.
        
        Args:
            stage: Pipeline stage
            arrival_rate: Lambda (instructions/second)
            service_time: Average service time (cycles)
            probability: Probability that this stage is visited
            
        Returns:
            QueueMetrics for this stage
        """
        # Convert service time to seconds
        service_time_sec = service_time / self.clock_freq
        
        # Effective arrival rate (accounting for conditional execution)
        lambda_eff = arrival_rate * probability
        
        # Utilization: rho = lambda * service_time
        rho = lambda_eff * service_time_sec
        
        # Check stability
        if rho >= 1.0:
            raise ValueError(
                f"Stage {stage.name} is unstable: rho = {rho:.3f} >= 1.0\n"
                f"Reduce arrival rate or service time."
            )
        
        # M/M/1 formulas
        queue_length = rho / (1 - rho)  # L = rho / (1 - rho)
        wait_time_sec = service_time_sec / (1 - rho)  # W = S / (1 - rho)
        throughput = lambda_eff  # For stable queue, throughput = arrival rate
        
        return QueueMetrics(
            stage=stage,
            service_time=service_time,
            arrival_rate=lambda_eff,
            utilization=rho,
            queue_length=queue_length,
            wait_time=wait_time_sec,
            throughput=throughput
        )
    
    def analyze_system(self, 
                      lambda_instr: Optional[float] = None,
                      wait_states: float = 0.0,
                      prefetch_effectiveness: Optional[float] = None) -> SystemMetrics:
        """
        Analyze complete 68000 queueing network.
        
        Args:
            lambda_instr: Instruction arrival rate (instructions/second)
                         If None, uses default from config
            wait_states: Additional wait states for memory accesses (0-2 typical)
            prefetch_effectiveness: How effective prefetch is (0.0-1.0)
                                   If None, uses default from config
            
        Returns:
            SystemMetrics with complete system analysis
        """
        if lambda_instr is None:
            lambda_instr = self.lambda_instr
        
        if prefetch_effectiveness is None:
            prefetch_effectiveness = self.prefetch_effectiveness
        
        # Adjust service times for wait states
        service_times = self.service_times.copy()
        
        # Wait states affect bus cycles (PF, OF, WB)
        wait_cycles = wait_states * 2  # Each wait state adds 2 clocks
        service_times[PipelineStage.PF] += wait_cycles * prefetch_effectiveness
        service_times[PipelineStage.OF] += wait_cycles
        service_times[PipelineStage.WB] += wait_cycles
        
        # Compute metrics for each stage
        stage_metrics = {}
        
        # Stage 1: Prefetch (always active, but overlapped)
        # Prefetch effectiveness reduces the apparent service time
        stage_metrics[PipelineStage.PF] = self.compute_stage_metrics(
            PipelineStage.PF,
            lambda_instr,
            service_times[PipelineStage.PF],
            probability=1.0
        )
        
        # Stage 2: Instruction Decode (always executed)
        stage_metrics[PipelineStage.ID] = self.compute_stage_metrics(
            PipelineStage.ID,
            lambda_instr,
            service_times[PipelineStage.ID],
            probability=1.0
        )
        
        # Stage 3: Effective Address calculation (conditional)
        p_ea = self.config['queueing_parameters']['service_times']['EA']['probability_needed']
        stage_metrics[PipelineStage.EA] = self.compute_stage_metrics(
            PipelineStage.EA,
            lambda_instr,
            service_times[PipelineStage.EA],
            probability=p_ea
        )
        
        # Stage 4: Operand Fetch (conditional)
        p_of = self.config['queueing_parameters']['service_times']['OF']['probability_needed']
        stage_metrics[PipelineStage.OF] = self.compute_stage_metrics(
            PipelineStage.OF,
            lambda_instr,
            service_times[PipelineStage.OF],
            probability=p_of
        )
        
        # Stage 5: Execute (always executed)
        stage_metrics[PipelineStage.EX] = self.compute_stage_metrics(
            PipelineStage.EX,
            lambda_instr,
            service_times[PipelineStage.EX],
            probability=1.0
        )
        
        # Stage 6: Write Back (conditional)
        p_wb = self.config['queueing_parameters']['service_times']['WB']['probability_needed']
        stage_metrics[PipelineStage.WB] = self.compute_stage_metrics(
            PipelineStage.WB,
            lambda_instr,
            service_times[PipelineStage.WB],
            probability=p_wb
        )
        
        # Compute overall metrics
        # Total CPI = sum of all stage wait times (in cycles)
        total_cpi = sum(
            metrics.wait_time * self.clock_freq 
            for metrics in stage_metrics.values()
        )
        
        ipc = 1.0 / total_cpi if total_cpi > 0 else 0.0
        
        # Find bottleneck (stage with highest utilization)
        bottleneck = max(stage_metrics.items(), 
                        key=lambda x: x[1].utilization)
        
        return SystemMetrics(
            total_cpi=total_cpi,
            ipc=ipc,
            throughput=lambda_instr,
            bottleneck_stage=bottleneck[0],
            max_utilization=bottleneck[1].utilization,
            stage_metrics=stage_metrics
        )
    
    def calibrate(self,
                 measured_ipc: float,
                 measured_counters: Dict[str, float],
                 tolerance_percent: float = 2.0,
                 max_iterations: int = 50) -> CalibrationResult:
        """
        Calibrate model to match measured IPC.
        
        Adjusts wait_states and prefetch_effectiveness to match measured performance.
        
        Args:
            measured_ipc: Measured IPC from real 68000 system
            measured_counters: Dictionary with measured parameters:
                - 'instruction_mix': Dict of instruction type fractions
                - 'memory_access_fraction': Fraction of memory accesses
                - 'addressing_mode_distribution': Distribution of addressing modes
            tolerance_percent: Target error percentage
            max_iterations: Maximum calibration iterations
            
        Returns:
            CalibrationResult with calibration outcome
        """
        # Update model with measured parameters
        if 'instruction_mix' in measured_counters:
            # Update instruction timing fractions
            for cat, fraction in measured_counters['instruction_mix'].items():
                if cat in self.instr_timing:
                    self.instr_timing[cat]['fraction'] = fraction
            self._compute_weighted_execution_time()
        
        if 'memory_access_fraction' in measured_counters:
            st = self.config['queueing_parameters']['service_times']
            st['OF']['probability_needed'] = measured_counters['memory_access_fraction']
        
        # Two-parameter calibration: wait_states and prefetch_effectiveness
        # Use nested optimization
        
        best_result = None
        best_error = float('inf')
        
        # Grid search over parameter space
        for pf_eff in [0.60, 0.70, 0.80, 0.90, 0.95]:
            # Binary search on wait_states for this prefetch effectiveness
            ws_low = 0.0
            ws_high = 4.0
            
            for iteration in range(max_iterations):
                ws_mid = (ws_low + ws_high) / 2.0
                
                try:
                    metrics = self.analyze_system(
                        wait_states=ws_mid,
                        prefetch_effectiveness=pf_eff
                    )
                    predicted_ipc = metrics.ipc
                    
                    error_percent = abs(predicted_ipc - measured_ipc) / measured_ipc * 100
                    
                    if error_percent < best_error:
                        best_error = error_percent
                        best_result = CalibrationResult(
                            converged=(error_percent < tolerance_percent),
                            iterations=iteration + 1,
                            final_error_percent=error_percent,
                            calibrated_wait_states=ws_mid,
                            calibrated_prefetch_effectiveness=pf_eff,
                            predicted_ipc=predicted_ipc,
                            measured_ipc=measured_ipc
                        )
                    
                    # Check convergence
                    if error_percent < tolerance_percent:
                        return best_result
                    
                    # Adjust search range
                    if predicted_ipc > measured_ipc:
                        # Model too fast, increase wait states
                        ws_low = ws_mid
                    else:
                        # Model too slow, decrease wait states
                        ws_high = ws_mid
                        
                except ValueError:
                    # Unstable, reduce wait states
                    ws_high = ws_mid
        
        return best_result
    
    def sensitivity_analysis(self, 
                           parameter: str,
                           values: List[float]) -> List[Tuple[float, float]]:
        """
        Analyze sensitivity of IPC to a parameter.
        
        Args:
            parameter: Parameter name ('wait_states', 'prefetch_effectiveness', etc.)
            values: List of parameter values to test
            
        Returns:
            List of (parameter_value, ipc) tuples
        """
        results = []
        
        for value in values:
            try:
                if parameter == 'wait_states':
                    metrics = self.analyze_system(wait_states=value)
                elif parameter == 'prefetch_effectiveness':
                    metrics = self.analyze_system(prefetch_effectiveness=value)
                elif parameter == 'clock_freq':
                    original_freq = self.clock_freq
                    self.clock_freq = value
                    metrics = self.analyze_system()
                    self.clock_freq = original_freq
                elif parameter == 'arrival_rate':
                    metrics = self.analyze_system(lambda_instr=value)
                else:
                    raise ValueError(f"Unknown parameter: {parameter}")
                
                results.append((value, metrics.ipc))
            except ValueError as e:
                # Skip unstable configurations
                print(f"  Warning: {parameter}={value} unstable, skipping")
                continue
        
        return results
    
    def print_analysis(self, metrics: SystemMetrics):
        """Print detailed analysis of system metrics"""
        print("=" * 80)
        print("MOTOROLA 68000 CPU QUEUEING MODEL ANALYSIS")
        print("=" * 80)
        print(f"Clock Frequency: {self.clock_freq/1e6:.2f} MHz")
        print(f"Clock Period: {self.clock_period_ns:.1f} ns")
        print(f"Arrival Rate: {metrics.throughput/1e6:.2f} MIPS")
        print()
        
        print("OVERALL METRICS:")
        print(f"  Total CPI: {metrics.total_cpi:.3f}")
        print(f"  IPC: {metrics.ipc:.3f}")
        print(f"  Bottleneck: {metrics.bottleneck_stage.name} "
              f"(ρ = {metrics.max_utilization:.3f})")
        print()
        
        print("STAGE-BY-STAGE METRICS:")
        print(f"{'Stage':<20} {'Service(cyc)':<12} {'Util(ρ)':<10} "
              f"{'Queue(L)':<10} {'Wait(cyc)':<10}")
        print("-" * 80)
        
        for stage in PipelineStage:
            m = metrics.stage_metrics[stage]
            wait_cycles = m.wait_time * self.clock_freq
            print(f"{stage.name:<20} {m.service_time:<12.2f} {m.utilization:<10.3f} "
                  f"{m.queue_length:<10.2f} {wait_cycles:<10.2f}")
        
        print("=" * 80)
        print()
        
        # 68000-specific insights
        print("68000-SPECIFIC INSIGHTS:")
        print(f"  Bus Cycle Time: {self.config['timing']['bus_cycle_clocks']} clocks")
        print(f"  Prefetch Queue Depth: {self.config['prefetch_queue']['queue_depth']} words")
        print(f"  Avg Instruction Time: {metrics.total_cpi:.1f} clocks")
        print(f"  Instructions/Second: {metrics.throughput/1e6:.2f} million")
        print()
        
        # Performance tips
        if metrics.bottleneck_stage == PipelineStage.EX:
            print("  ⚠ BOTTLENECK: Execution stage")
            print("  → Optimize instruction mix (use register operations)")
            print("  → Avoid multiply/divide operations (70-158 cycles!)")
            print("  → Use word operations instead of longword when possible")
        elif metrics.bottleneck_stage == PipelineStage.EA:
            print("  ⚠ BOTTLENECK: Effective address calculation")
            print("  → Use simpler addressing modes (register direct, indirect)")
            print("  → Avoid complex modes (indexed, absolute long)")
            print("  → Precompute addresses when possible")
        elif metrics.bottleneck_stage == PipelineStage.OF:
            print("  ⚠ BOTTLENECK: Operand fetch")
            print("  → Reduce memory operations (use registers)")
            print("  → Use faster memory (reduce wait states)")
            print("  → Keep frequently-used data in registers")
        elif metrics.bottleneck_stage == PipelineStage.PF:
            print("  ⚠ BOTTLENECK: Prefetch")
            print("  → Memory too slow (add wait states parameter)")
            print("  → Code execution very branch-heavy")
        
        print("=" * 80)


def example_usage():
    """Example: Analyze standard 68000 system"""
    print("Motorola 68000 CPU Queueing Model - Example Analysis")
    print()
    
    # Load model
    model = M68000QueueModel('m68000_cpu_model.json')
    
    # Analyze with default parameters
    # At 8 MHz with avg execution of ~8.5 cycles:
    # Max rate = 8e6 / 8.5 = ~940K instructions/sec
    # Use 70% of max for stability
    print("SCENARIO 1: Standard 68000 at 8 MHz with fast memory (0 wait states)")
    print("-" * 80)
    metrics = model.analyze_system(lambda_instr=600000, wait_states=0.0)
    model.print_analysis(metrics)
    
    # Analyze with slow memory (typical for early systems)
    print("\nSCENARIO 2: Standard 68000 at 8 MHz with slow memory (1 wait state)")
    print("-" * 80)
    metrics_slow = model.analyze_system(lambda_instr=600000, wait_states=1.0)
    model.print_analysis(metrics_slow)
    
    # Compare
    print("\nPERFORMANCE COMPARISON:")
    print(f"Fast memory IPC: {metrics.ipc:.3f}")
    print(f"Slow memory IPC: {metrics_slow.ipc:.3f}")
    print(f"Performance loss: {(1 - metrics_slow.ipc/metrics.ipc)*100:.1f}%")
    print()
    
    # Sensitivity analysis - wait states
    print("\nSENSITIVITY ANALYSIS: Wait States vs IPC")
    print("-" * 80)
    wait_states_range = [0.0, 0.5, 1.0, 1.5, 2.0]
    results_ws = []
    
    for ws in wait_states_range:
        try:
            m = model.analyze_system(lambda_instr=400000, wait_states=ws)
            results_ws.append((ws, m.ipc))
        except ValueError:
            print(f"  Warning: ws={ws} unstable, skipping")
            continue
    
    if results_ws:
        print(f"{'Wait States':<15} {'IPC':<10} {'Slowdown':<10}")
        print("-" * 40)
        baseline = results_ws[0][1]
        for ws, ipc in results_ws:
            slowdown = (1 - ipc/baseline) * 100
            print(f"{ws:<15.1f} {ipc:<10.3f} {slowdown:<10.1f}%")
    
    # Sensitivity analysis - prefetch effectiveness
    print("\nSENSITIVITY ANALYSIS: Prefetch Effectiveness vs IPC")
    print("-" * 80)
    prefetch_range = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
    results_pf = []
    
    for pf in prefetch_range:
        try:
            m = model.analyze_system(lambda_instr=400000, prefetch_effectiveness=pf)
            results_pf.append((pf, m.ipc))
        except ValueError:
            continue
    
    if results_pf:
        print(f"{'Prefetch Eff':<15} {'IPC':<10} {'vs. 50%':<10}")
        print("-" * 40)
        baseline = results_pf[0][1]
        for pf, ipc in results_pf:
            improvement = (ipc/baseline - 1) * 100
            print(f"{pf:<15.2f} {ipc:<10.3f} {improvement:+10.1f}%")


if __name__ == '__main__':
    example_usage()
