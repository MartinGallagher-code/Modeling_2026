#!/usr/bin/env python3
"""
IBM PC 8086 CPU Queueing Model - Implementation
================================================

Grey-box performance modeling of the Intel 8086 microprocessor
as used in the IBM PC

Key features:
- 2-stage pipeline: BIU (fetch) and EU (execute)
- 6-byte instruction prefetch queue
- Parallel BIU/EU operation when possible
- Variable instruction cycle counts (2-162 cycles)

Author: Grey-Box Performance Modeling Research
Date: January 22, 2026
Version: 1.0 (8086 variant)
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StageMetrics:
    """Performance metrics for a single pipeline stage"""
    stage_name: str
    service_time_cycles: float
    utilization: float
    queue_length: float
    wait_time_seconds: float
    cpi_contribution: float


@dataclass
class PipelinePerformance:
    """Overall pipeline performance metrics"""
    cpi: float
    ipc: float
    throughput_ips: float
    arrival_rate_ips: float
    stage_metrics: List[StageMetrics]
    bottleneck_stage: str
    bottleneck_utilization: float
    queue_efficiency: float  # How often queue has instructions ready


@dataclass
class CalibrationResult:
    """Results from model calibration"""
    measured_cpi: float
    predicted_cpi: float
    discrepancy: float
    error_percent: float
    calibrated_parameters: Dict[str, float]
    pipeline_details: PipelinePerformance
    iterations: int
    converged: bool


class IBMPC8086Model:
    """
    IBM PC 8086 CPU queueing model
    
    Models a 2-stage pipeline with instruction prefetch:
    - BIU (Bus Interface Unit): Fetches instructions into 6-byte queue
    - EU (Execution Unit): Decodes and executes from queue
    
    Unlike 6502 (sequential) but simpler than modern CPUs (20+ stages).
    The 8086 was the first x86 processor with instruction pipelining.
    """
    
    def __init__(self, config_file: str = 'ibm_pc_8086_model.json'):
        """
        Initialize model from JSON configuration
        
        Args:
            config_file: Path to JSON configuration file
        """
        self.config_file = config_file
        self._load_config()
        self._extract_parameters()
    
    def _load_config(self) -> None:
        """Load model configuration from JSON file"""
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        
        # 8086 clock frequency (4.77 MHz for IBM PC)
        self.clock_freq = self.config['system_parameters']['clock_freq_hz']
        self.stages = self.config['pipeline_stages']
        self.calibration_config = self.config.get('calibration_config', {})
        self.queue_size = self.config['system_parameters']['prefetch_queue_size']
    
    def _extract_parameters(self) -> None:
        """Extract all parameters into flat dictionary"""
        self.params = {}
        for stage in self.stages:
            for param_name, param_data in stage.get('parameters', {}).items():
                if param_data['type'] != 'derived':
                    self.params[param_name] = param_data['value']
        
        # Store parameter metadata for bounds checking
        self.param_metadata = {}
        for stage in self.stages:
            for param_name, param_data in stage.get('parameters', {}).items():
                self.param_metadata[param_name] = param_data
    
    def compute_service_time(self, stage: Dict) -> float:
        """
        Compute service time for a stage given current parameters
        
        Args:
            stage: Stage configuration dictionary
        
        Returns:
            Mean service time in cycles
        """
        formula = stage['service_time_formula']
        
        # Build namespace with current parameter values
        namespace = self.params.copy()
        
        # Handle derived parameters
        for param_name, param_data in stage.get('parameters', {}).items():
            if param_data['type'] == 'derived':
                namespace[param_name] = eval(param_data['formula'], namespace)
        
        # Evaluate service time formula
        try:
            service_time = eval(formula, {"__builtins__": {}}, namespace)
        except Exception as e:
            raise ValueError(f"Error evaluating service time for {stage['name']}: {e}")
        
        return service_time
    
    def compute_stage_metrics(self, stage: Dict, arrival_rate: float) -> StageMetrics:
        """
        Compute queueing metrics for a single M/M/1 stage
        
        For 8086: BIU and EU operate in parallel when possible.
        The prefetch queue decouples them.
        
        Args:
            stage: Stage configuration dictionary
            arrival_rate: Arrival rate λ (instructions/second)
        
        Returns:
            StageMetrics object with all performance metrics
        
        Raises:
            ValueError: If stage is unstable (ρ >= 1)
        """
        # Service time in cycles
        S_cycles = self.compute_service_time(stage)
        
        # Service time in seconds
        S_seconds = S_cycles / self.clock_freq
        
        # Utilization ρ = λ × S
        rho = arrival_rate * S_seconds
        
        # Check stability condition
        if rho >= 1.0:
            raise ValueError(
                f"Stage {stage['name']} is unstable: ρ = {rho:.4f} >= 1.0\n"
                f"Reduce arrival rate or decrease service time"
            )
        
        # Queue length L = ρ / (1 - ρ)
        queue_length = rho / (1 - rho)
        
        # Wait time W = S / (1 - ρ)  (includes service + queueing)
        wait_time = S_seconds / (1 - rho)
        
        # CPI contribution (cycles per instruction for this stage)
        cpi_contribution = wait_time * self.clock_freq
        
        return StageMetrics(
            stage_name=stage['name'],
            service_time_cycles=S_cycles,
            utilization=rho,
            queue_length=queue_length,
            wait_time_seconds=wait_time,
            cpi_contribution=cpi_contribution
        )
    
    def compute_queue_efficiency(self) -> float:
        """
        Estimate prefetch queue effectiveness
        
        Queue efficiency = probability queue has instructions ready
        = 1 - p_queue_empty
        
        Returns:
            Queue efficiency (0.0 to 1.0)
        """
        return 1.0 - self.params.get('p_queue_empty', 0.15)
    
    def compute_pipeline_performance(
        self,
        arrival_rate: Optional[float] = None,
        target_utilization: float = 0.8
    ) -> PipelinePerformance:
        """
        Compute overall pipeline performance
        
        For 8086: The pipeline allows BIU and EU to work in parallel,
        but they share the memory bus. When queue is full, BIU stalls.
        When queue is empty, EU stalls.
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/sec)
                         If None, uses target_utilization of bottleneck stage
            target_utilization: Target utilization for bottleneck (default 0.8)
        
        Returns:
            PipelinePerformance object with CPI, IPC, and stage-level metrics
        """
        # If no arrival rate specified, compute sustainable rate
        if arrival_rate is None:
            # Find bottleneck (stage with maximum service time)
            max_service_time = max([self.compute_service_time(s) for s in self.stages])
            # Set arrival rate to achieve target utilization at bottleneck
            max_sustainable_rate = target_utilization * self.clock_freq / max_service_time
            arrival_rate = max_sustainable_rate
        
        # Compute metrics for each stage
        stage_metrics = []
        total_cpi = 0.0
        
        for stage in self.stages:
            metrics = self.compute_stage_metrics(stage, arrival_rate)
            stage_metrics.append(metrics)
            # For pipeline, use max CPI (bottleneck) not sum
            # But account for queue stalls
            total_cpi = max(total_cpi, metrics.cpi_contribution)
        
        # Add queue empty penalty
        # When queue is empty, EU must wait for BIU
        queue_efficiency = self.compute_queue_efficiency()
        queue_penalty = self.params.get('p_queue_empty', 0.15) * \
                       self.params.get('penalty_queue_empty', 2.0) * \
                       self.params.get('cycles_bus_access', 4.0)
        
        total_cpi += queue_penalty
        
        # Overall performance
        ipc = 1.0 / total_cpi
        throughput = arrival_rate
        
        # Identify bottleneck (highest utilization)
        bottleneck = max(stage_metrics, key=lambda x: x.utilization)
        
        return PipelinePerformance(
            cpi=total_cpi,
            ipc=ipc,
            throughput_ips=throughput,
            arrival_rate_ips=arrival_rate,
            stage_metrics=stage_metrics,
            bottleneck_stage=bottleneck.stage_name,
            bottleneck_utilization=bottleneck.utilization,
            queue_efficiency=queue_efficiency
        )
    
    def update_parameters(self, param_updates: Dict[str, float]) -> None:
        """
        Update model parameters with bounds checking
        
        Args:
            param_updates: Dictionary of parameter names and new values
        
        Raises:
            ValueError: If parameter value is out of bounds
        """
        for param_name, new_value in param_updates.items():
            if param_name not in self.params:
                raise ValueError(f"Unknown parameter: {param_name}")
            
            # Check bounds if specified
            metadata = self.param_metadata.get(param_name, {})
            if 'bounds' in metadata:
                lower, upper = metadata['bounds']
                if not (lower <= new_value <= upper):
                    raise ValueError(
                        f"Parameter {param_name} = {new_value} out of bounds [{lower}, {upper}]"
                    )
            
            self.params[param_name] = new_value
    
    def calibrate(
        self,
        measured_cpi: float,
        measured_instruction_mix: Dict[str, float],
        max_iterations: int = 20,
        tolerance_percent: float = 5.0,
        verbose: bool = True
    ) -> CalibrationResult:
        """
        Calibrate model parameters to match measured 8086 performance
        
        For 8086 calibration:
        1. Extract instruction mix from disassembly or profiling
        2. Set instruction type probabilities
        3. Adjust average cycle counts per instruction type
        4. Adjust queue empty probability
        
        Args:
            measured_cpi: Measured CPI from real IBM PC or emulator
            measured_instruction_mix: Dict with instruction type fractions
            max_iterations: Maximum calibration iterations
            tolerance_percent: Target error threshold (%)
            verbose: Print iteration details
        
        Returns:
            CalibrationResult object with final parameters and metrics
        """
        if verbose:
            print(f"=== Calibrating 8086 Model ===")
            print(f"Target CPI: {measured_cpi:.4f}")
            print(f"Tolerance: {tolerance_percent}%")
            print(f"Max iterations: {max_iterations}\n")
        
        iteration = 0
        converged = False
        learning_rate = self.calibration_config.get('learning_rate', 0.12)
        
        # Update parameters from instruction mix
        param_mapping = {
            'mov_fraction': 'p_mov',
            'alu_reg_fraction': 'p_alu_reg',
            'alu_mem_fraction': 'p_alu_mem',
            'mul_fraction': 'p_mul',
            'div_fraction': 'p_div',
            'shift_fraction': 'p_shift',
            'string_fraction': 'p_string',
            'jump_short_fraction': 'p_jump_short',
            'jump_far_fraction': 'p_jump_far',
            'call_ret_fraction': 'p_call_ret',
            'queue_empty_rate': 'p_queue_empty'
        }
        
        updates = {}
        for measured_name, param_name in param_mapping.items():
            if measured_name in measured_instruction_mix:
                updates[param_name] = measured_instruction_mix[measured_name]
        
        if updates:
            self.update_parameters(updates)
            if verbose:
                print("Updated parameters from instruction mix:")
                for k, v in updates.items():
                    print(f"  {k:30s} = {v:.4f}")
                print()
        
        # Iterative refinement loop
        for iteration in range(1, max_iterations + 1):
            # Compute model prediction
            result = self.compute_pipeline_performance()
            predicted_cpi = result.cpi
            
            # Calculate error
            discrepancy = measured_cpi - predicted_cpi
            error_percent = abs(discrepancy / measured_cpi) * 100
            
            if verbose:
                print(f"Iteration {iteration}:")
                print(f"  Predicted CPI: {predicted_cpi:.4f}")
                print(f"  Error: {error_percent:.2f}%")
            
            # Check convergence
            if error_percent < tolerance_percent:
                converged = True
                if verbose:
                    print(f"  ✓ Converged!\n")
                break
            
            # Adjust cycle counts for instruction types to reduce error
            # Strategy: If model under-predicts CPI (predicted < measured),
            # increase cycle counts. If over-predicts, decrease cycle counts.
            adjustment_factor = 1.0 + learning_rate * (discrepancy / measured_cpi)
            
            # Clamp adjustment to reasonable range
            adjustment_factor = np.clip(adjustment_factor, 0.85, 1.15)
            
            # Adjust the most impactful parameters
            for param_name in ['cycles_mov', 'cycles_alu_mem', 'cycles_jump_short', 
                              'cycles_call_ret', 'cycles_mul']:
                if param_name in self.params:
                    new_value = self.params[param_name] * adjustment_factor
                    bounds = self.param_metadata[param_name]['bounds']
                    new_value = np.clip(new_value, bounds[0], bounds[1])
                    
                    if verbose and abs(new_value - self.params[param_name]) > 0.1:
                        print(f"  Adjusting {param_name}: {self.params[param_name]:.2f} → {new_value:.2f} cycles")
                    
                    self.params[param_name] = new_value
            
            if verbose:
                print()
        
        # Final evaluation
        final_result = self.compute_pipeline_performance()
        final_discrepancy = measured_cpi - final_result.cpi
        final_error = abs(final_discrepancy / measured_cpi) * 100
        
        return CalibrationResult(
            measured_cpi=measured_cpi,
            predicted_cpi=final_result.cpi,
            discrepancy=final_discrepancy,
            error_percent=final_error,
            calibrated_parameters=self.params.copy(),
            pipeline_details=final_result,
            iterations=iteration,
            converged=converged
        )
    
    def sensitivity_analysis(
        self,
        param_name: str,
        epsilon: float = 0.01
    ) -> Dict[str, float]:
        """
        Compute sensitivity ∂CPI/∂param using finite differences
        
        Args:
            param_name: Name of parameter to analyze
            epsilon: Perturbation fraction (default 1%)
        
        Returns:
            Dictionary with sensitivity metrics
        """
        # Baseline CPI
        cpi_base = self.compute_pipeline_performance().cpi
        
        # Perturb parameter
        original_value = self.params[param_name]
        perturbed_value = original_value * (1 + epsilon)
        
        # Check bounds
        metadata = self.param_metadata.get(param_name, {})
        if 'bounds' in metadata:
            lower, upper = metadata['bounds']
            perturbed_value = np.clip(perturbed_value, lower, upper)
        
        self.params[param_name] = perturbed_value
        
        # Compute perturbed CPI
        cpi_perturbed = self.compute_pipeline_performance().cpi
        
        # Restore original value
        self.params[param_name] = original_value
        
        # Compute sensitivities
        delta_cpi = cpi_perturbed - cpi_base
        delta_param = perturbed_value - original_value
        
        absolute_sensitivity = delta_cpi / delta_param
        relative_sensitivity = (delta_cpi / cpi_base) / (delta_param / original_value)
        elasticity = (delta_cpi / cpi_base) / epsilon
        
        return {
            'parameter': param_name,
            'baseline_value': original_value,
            'baseline_cpi': cpi_base,
            'absolute_sensitivity': absolute_sensitivity,
            'relative_sensitivity': relative_sensitivity,
            'elasticity': elasticity
        }
    
    def full_sensitivity_analysis(self) -> Dict[str, Dict]:
        """
        Compute sensitivity for all unknown parameters
        
        Returns:
            Dictionary mapping parameter names to sensitivity metrics
        """
        results = {}
        for param_name in self.params.keys():
            metadata = self.param_metadata.get(param_name, {})
            if metadata.get('type') == 'unknown':
                results[param_name] = self.sensitivity_analysis(param_name)
        return results
    
    def print_performance_report(self, result: PipelinePerformance) -> None:
        """Print detailed performance report for 8086"""
        print("=" * 80)
        print("IBM PC 8086 CPU QUEUEING MODEL - PERFORMANCE REPORT")
        print("=" * 80)
        print(f"\nOverall Performance:")
        print(f"  CPI:        {result.cpi:.4f} cycles/instruction")
        print(f"  IPC:        {result.ipc:.4f} instructions/cycle")
        print(f"  Clock:      {self.clock_freq/1e6:.3f} MHz")
        print(f"  Throughput: {result.throughput_ips/1e6:.2f} MIPS (million instructions/sec)")
        print(f"  Bottleneck: {result.bottleneck_stage} (ρ = {result.bottleneck_utilization:.3f})")
        print(f"  Queue Eff.: {result.queue_efficiency*100:.1f}% (prefetch queue effectiveness)")
        
        print(f"\nPipeline Stage Breakdown:")
        print(f"  {'Stage':<35s} {'Service (cyc)':<15s} {'Utilization':<15s} {'Queue Len':<15s} {'CPI':<10s}")
        print(f"  {'-'*35} {'-'*15} {'-'*15} {'-'*15} {'-'*10}")
        for stage in result.stage_metrics:
            print(f"  {stage.stage_name:<35s} {stage.service_time_cycles:>6.2f} cyc      "
                  f"{stage.utilization:>6.3f}         {stage.queue_length:>6.3f}         "
                  f"{stage.cpi_contribution:>6.3f}")
        
        print(f"\nInstruction Mix Parameters:")
        print(f"  {'Parameter':<30s} {'Value':>10s} {'Type':>12s}")
        print(f"  {'-'*30} {'-'*10} {'-'*12}")
        for param_name in ['p_mov', 'p_alu_reg', 'p_alu_mem', 'p_mul', 'p_div',
                          'p_shift', 'p_string', 'p_jump_short', 'p_jump_far', 
                          'p_call_ret', 'p_other']:
            if param_name in self.params:
                value = self.params[param_name]
                param_type = self.param_metadata.get(param_name, {}).get('type', 'unknown')
                print(f"  {param_name:<30s} {value:>10.4f} {param_type:>12s}")
        
        print(f"\nCycle Count Parameters:")
        print(f"  {'Parameter':<30s} {'Value':>10s} {'Type':>12s}")
        print(f"  {'-'*30} {'-'*10} {'-'*12}")
        for param_name in ['cycles_mov', 'cycles_alu_reg', 'cycles_alu_mem', 
                          'cycles_mul', 'cycles_div', 'cycles_shift', 'cycles_string',
                          'cycles_jump_short', 'cycles_jump_far', 'cycles_call_ret', 
                          'cycles_other']:
            if param_name in self.params:
                value = self.params[param_name]
                param_type = self.param_metadata.get(param_name, {}).get('type', 'unknown')
                print(f"  {param_name:<30s} {value:>10.2f} {param_type:>12s}")
        
        print(f"\nPrefetch Queue Parameters:")
        print(f"  Queue size:        {self.queue_size} bytes")
        print(f"  Queue empty prob:  {self.params.get('p_queue_empty', 0.15):.3f}")
        print(f"  Bus access cycles: {self.params.get('cycles_bus_access', 4):.0f}")
        
        print("=" * 80)
    
    def export_results(self, filename: str, result: PipelinePerformance) -> None:
        """Export results to JSON file"""
        export_data = {
            'model_metadata': self.config['model_metadata'],
            'performance': {
                'cpi': result.cpi,
                'ipc': result.ipc,
                'throughput_ips': result.throughput_ips,
                'clock_freq_hz': self.clock_freq,
                'bottleneck_stage': result.bottleneck_stage,
                'bottleneck_utilization': result.bottleneck_utilization,
                'queue_efficiency': result.queue_efficiency
            },
            'stage_metrics': [
                {
                    'stage_name': s.stage_name,
                    'service_time_cycles': s.service_time_cycles,
                    'utilization': s.utilization,
                    'queue_length': s.queue_length,
                    'cpi_contribution': s.cpi_contribution
                }
                for s in result.stage_metrics
            ],
            'parameters': self.params
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Results exported to: {filename}")


def main():
    """Example usage with 8086"""
    print("IBM PC 8086 CPU Queueing Model - Example Run\n")
    
    # Create model
    model = IBMPC8086Model('ibm_pc_8086_model.json')
    
    # Compute baseline performance
    print("1. BASELINE PERFORMANCE")
    print("-" * 80)
    result = model.compute_pipeline_performance()
    model.print_performance_report(result)
    
    print("\n\n2. SENSITIVITY ANALYSIS")
    print("-" * 80)
    sensitivities = model.full_sensitivity_analysis()
    print(f"{'Parameter':<30s} {'Baseline':<12s} {'∂CPI/∂param':<15s} {'Elasticity':<15s}")
    print(f"{'-'*30} {'-'*12} {'-'*15} {'-'*15}")
    for param_name, sens in sensitivities.items():
        print(f"{param_name:<30s} {sens['baseline_value']:>8.4f}    "
              f"{sens['absolute_sensitivity']:>+10.6f}     {sens['elasticity']:>+10.4f}")
    
    print("\n\n3. MODEL CALIBRATION")
    print("-" * 80)
    
    # Simulate measured data from IBM PC running typical DOS program
    measured_instruction_mix = {
        'mov_fraction': 0.28,           # MOV is very common
        'alu_reg_fraction': 0.18,       # Register ALU ops
        'alu_mem_fraction': 0.12,       # Memory ALU ops
        'jump_short_fraction': 0.10,    # Conditional jumps
        'call_ret_fraction': 0.08,      # CALL/RET
        'shift_fraction': 0.06,         # Shifts/rotates
        'jump_far_fraction': 0.03,      # JMP, LOOP
        'string_fraction': 0.04,        # String operations
        'mul_fraction': 0.02,           # Multiply
        'div_fraction': 0.01,           # Divide
        'queue_empty_rate': 0.12        # Queue empty ~12% of time
    }
    measured_cpi = 5.2  # Typical for DOS utilities
    
    calibration_result = model.calibrate(
        measured_cpi=measured_cpi,
        measured_instruction_mix=measured_instruction_mix,
        tolerance_percent=5.0,
        verbose=True
    )
    
    print("\nCALIBRATION SUMMARY:")
    print(f"  Measured CPI:    {calibration_result.measured_cpi:.4f}")
    print(f"  Predicted CPI:   {calibration_result.predicted_cpi:.4f}")
    print(f"  Error:           {calibration_result.error_percent:.2f}%")
    print(f"  Iterations:      {calibration_result.iterations}")
    print(f"  Converged:       {calibration_result.converged}")
    
    # Export results
    model.export_results('8086_baseline_results.json', result)
    
    print("\n" + "=" * 80)
    print("IBM PC 8086 model example complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
