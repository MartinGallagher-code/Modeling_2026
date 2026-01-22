#!/usr/bin/env python3
"""
Simple CPU Queueing Model - Implementation
==========================================

Grey-box performance modeling of a simple in-order CPU pipeline
using queueing theory (series of M/M/1 queues)

Author: Grey-Box Performance Modeling Research
Date: January 22, 2026
Version: 1.0
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
    ipc: float
    cpi: float
    throughput_ips: float
    arrival_rate_ips: float
    stage_metrics: List[StageMetrics]
    bottleneck_stage: str
    bottleneck_utilization: float


@dataclass
class CalibrationResult:
    """Results from model calibration"""
    measured_ipc: float
    predicted_ipc: float
    discrepancy: float
    error_percent: float
    calibrated_parameters: Dict[str, float]
    pipeline_details: PipelinePerformance
    iterations: int
    converged: bool


class SimpleCPUQueueModel:
    """
    Simple in-order CPU pipeline queueing model
    
    Models a 5-stage RISC pipeline as series of M/M/1 queues:
    - Instruction Fetch (IF)
    - Decode (ID)
    - Execute (EX)
    - Memory Access (MEM)
    - Write Back (WB)
    
    Uses Jackson Network decomposition for analysis.
    """
    
    def __init__(self, config_file: str = 'simple_cpu_model.json'):
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
        
        self.clock_freq = self.config['system_parameters']['clock_freq_ghz'] * 1e9  # Hz
        self.stages = self.config['pipeline_stages']
        self.calibration_config = self.config.get('calibration_config', {})
    
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
        
        Uses standard M/M/1 formulas:
        - ρ = λS (utilization)
        - L = ρ/(1-ρ) (average queue length)
        - W = S/(1-ρ) (average wait time)
        
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
    
    def compute_pipeline_performance(
        self,
        arrival_rate: Optional[float] = None,
        target_utilization: float = 0.8
    ) -> PipelinePerformance:
        """
        Compute overall pipeline performance using Jackson Network decomposition
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/sec)
                         If None, uses target_utilization of bottleneck stage
            target_utilization: Target utilization for bottleneck (default 0.8)
        
        Returns:
            PipelinePerformance object with IPC, CPI, and stage-level metrics
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
            total_cpi += metrics.cpi_contribution
        
        # Overall performance
        ipc = 1.0 / total_cpi
        throughput = arrival_rate
        
        # Identify bottleneck (highest utilization)
        bottleneck = max(stage_metrics, key=lambda x: x.utilization)
        
        return PipelinePerformance(
            ipc=ipc,
            cpi=total_cpi,
            throughput_ips=throughput,
            arrival_rate_ips=arrival_rate,
            stage_metrics=stage_metrics,
            bottleneck_stage=bottleneck.stage_name,
            bottleneck_utilization=bottleneck.utilization
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
        measured_ipc: float,
        measured_counters: Dict[str, float],
        max_iterations: int = 10,
        tolerance_percent: float = 2.0,
        verbose: bool = True
    ) -> CalibrationResult:
        """
        Calibrate model parameters to match measured system performance
        
        Iterative process:
        1. Update known parameters from measurements (cache miss rates, instruction mix)
        2. Compute model prediction
        3. If error > tolerance, adjust unknown latency parameters
        4. Repeat until convergence or max iterations
        
        Args:
            measured_ipc: Measured IPC from real system
            measured_counters: Dict with cache miss rates, instruction mix, etc.
            max_iterations: Maximum calibration iterations
            tolerance_percent: Target error threshold (%)
            verbose: Print iteration details
        
        Returns:
            CalibrationResult object with final parameters and metrics
        """
        if verbose:
            print(f"=== Calibrating Model ===")
            print(f"Target IPC: {measured_ipc:.4f}")
            print(f"Tolerance: {tolerance_percent}%")
            print(f"Max iterations: {max_iterations}\n")
        
        iteration = 0
        converged = False
        learning_rate = self.calibration_config.get('learning_rate', 0.1)
        
        # Update parameters from direct measurements
        param_mapping = {
            'icache_miss_rate': 'p_icache_miss',
            'dcache_miss_rate': 'p_dcache_miss',
            'alu_fraction': 'p_alu',
            'mul_fraction': 'p_mul',
            'div_fraction': 'p_div',
            'mem_fraction': 'p_mem'
        }
        
        updates = {}
        for measured_name, param_name in param_mapping.items():
            if measured_name in measured_counters:
                updates[param_name] = measured_counters[measured_name]
        
        if updates:
            self.update_parameters(updates)
            if verbose:
                print("Updated parameters from measurements:")
                for k, v in updates.items():
                    print(f"  {k:20s} = {v:.4f}")
                print()
        
        # Iterative refinement loop
        for iteration in range(1, max_iterations + 1):
            # Compute model prediction
            result = self.compute_pipeline_performance()
            predicted_ipc = result.ipc
            
            # Calculate error
            discrepancy = measured_ipc - predicted_ipc
            error_percent = abs(discrepancy / measured_ipc) * 100
            
            if verbose:
                print(f"Iteration {iteration}:")
                print(f"  Predicted IPC: {predicted_ipc:.4f}")
                print(f"  Error: {error_percent:.2f}%")
            
            # Check convergence
            if error_percent < tolerance_percent:
                converged = True
                if verbose:
                    print(f"  ✓ Converged!\n")
                break
            
            # Adjust latency parameter to reduce error
            # Strategy: If model under-predicts (predicted < measured),
            # decrease latency. If over-predicts, increase latency.
            adjustment_factor = 1.0 - learning_rate * (discrepancy / measured_ipc)
            
            # Clamp adjustment to reasonable range
            adjustment_factor = np.clip(adjustment_factor, 0.5, 1.5)
            
            new_L_miss = self.params['L_miss'] * adjustment_factor
            
            # Check bounds
            bounds = self.param_metadata['L_miss']['bounds']
            new_L_miss = np.clip(new_L_miss, bounds[0], bounds[1])
            
            if verbose:
                print(f"  Adjusting L_miss: {self.params['L_miss']:.1f} → {new_L_miss:.1f} cycles\n")
            
            self.params['L_miss'] = new_L_miss
        
        # Final evaluation
        final_result = self.compute_pipeline_performance()
        final_discrepancy = measured_ipc - final_result.ipc
        final_error = abs(final_discrepancy / measured_ipc) * 100
        
        return CalibrationResult(
            measured_ipc=measured_ipc,
            predicted_ipc=final_result.ipc,
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
        Compute sensitivity ∂IPC/∂param using finite differences
        
        Args:
            param_name: Name of parameter to analyze
            epsilon: Perturbation fraction (default 1%)
        
        Returns:
            Dictionary with sensitivity metrics:
            - absolute_sensitivity: ∂IPC/∂param
            - relative_sensitivity: (∂IPC/IPC) / (∂param/param)
            - elasticity: % change in IPC per 1% change in param
        """
        # Baseline IPC
        ipc_base = self.compute_pipeline_performance().ipc
        
        # Perturb parameter
        original_value = self.params[param_name]
        perturbed_value = original_value * (1 + epsilon)
        
        # Check bounds
        metadata = self.param_metadata.get(param_name, {})
        if 'bounds' in metadata:
            lower, upper = metadata['bounds']
            perturbed_value = np.clip(perturbed_value, lower, upper)
        
        self.params[param_name] = perturbed_value
        
        # Compute perturbed IPC
        ipc_perturbed = self.compute_pipeline_performance().ipc
        
        # Restore original value
        self.params[param_name] = original_value
        
        # Compute sensitivities
        delta_ipc = ipc_perturbed - ipc_base
        delta_param = perturbed_value - original_value
        
        absolute_sensitivity = delta_ipc / delta_param
        relative_sensitivity = (delta_ipc / ipc_base) / (delta_param / original_value)
        elasticity = (delta_ipc / ipc_base) / epsilon  # % change per 1% change
        
        return {
            'parameter': param_name,
            'baseline_value': original_value,
            'baseline_ipc': ipc_base,
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
        """Print detailed performance report"""
        print("=" * 80)
        print("SIMPLE CPU QUEUEING MODEL - PERFORMANCE REPORT")
        print("=" * 80)
        print(f"\nOverall Performance:")
        print(f"  IPC:        {result.ipc:.4f}")
        print(f"  CPI:        {result.cpi:.4f}")
        print(f"  Throughput: {result.throughput_ips/1e9:.3f} GIPS (billion instructions/sec)")
        print(f"  Bottleneck: {result.bottleneck_stage} (ρ = {result.bottleneck_utilization:.3f})")
        
        print(f"\nStage-by-Stage Breakdown:")
        print(f"  {'Stage':<20s} {'Service (cyc)':<15s} {'Utilization':<15s} {'Queue Len':<15s} {'CPI':<10s}")
        print(f"  {'-'*20} {'-'*15} {'-'*15} {'-'*15} {'-'*10}")
        for stage in result.stage_metrics:
            print(f"  {stage.stage_name:<20s} {stage.service_time_cycles:>6.2f} cyc      "
                  f"{stage.utilization:>6.3f}         {stage.queue_length:>6.3f}         "
                  f"{stage.cpi_contribution:>6.3f}")
        
        print(f"\nModel Parameters:")
        for param_name, value in self.params.items():
            metadata = self.param_metadata.get(param_name, {})
            param_type = metadata.get('type', 'unknown')
            units = metadata.get('units', '')
            print(f"  {param_name:<20s} = {value:>8.4f} {units:>10s}  [{param_type}]")
        print("=" * 80)
    
    def export_results(self, filename: str, result: PipelinePerformance) -> None:
        """Export results to JSON file"""
        export_data = {
            'model_metadata': self.config['model_metadata'],
            'performance': {
                'ipc': result.ipc,
                'cpi': result.cpi,
                'throughput_ips': result.throughput_ips,
                'bottleneck_stage': result.bottleneck_stage,
                'bottleneck_utilization': result.bottleneck_utilization
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
    """Example usage and validation"""
    print("Simple CPU Queueing Model - Example Run\n")
    
    # Create model
    model = SimpleCPUQueueModel('simple_cpu_model.json')
    
    # Compute baseline performance
    print("1. BASELINE PERFORMANCE")
    print("-" * 80)
    result = model.compute_pipeline_performance()
    model.print_performance_report(result)
    
    print("\n\n2. SENSITIVITY ANALYSIS")
    print("-" * 80)
    sensitivities = model.full_sensitivity_analysis()
    print(f"{'Parameter':<20s} {'Baseline':<12s} {'∂IPC/∂param':<15s} {'Elasticity':<15s}")
    print(f"{'-'*20} {'-'*12} {'-'*15} {'-'*15}")
    for param_name, sens in sensitivities.items():
        print(f"{param_name:<20s} {sens['baseline_value']:>8.4f}    "
              f"{sens['absolute_sensitivity']:>+10.6f}     {sens['elasticity']:>+10.4f}")
    
    print("\n\n3. MODEL CALIBRATION")
    print("-" * 80)
    
    # Simulate measured data from a real system
    measured_counters = {
        'icache_miss_rate': 0.015,   # 1.5% I-cache miss rate
        'dcache_miss_rate': 0.025,   # 2.5% D-cache miss rate
        'alu_fraction': 0.68,
        'mul_fraction': 0.07,
        'div_fraction': 0.02,
        'mem_fraction': 0.32
    }
    measured_ipc = 0.78
    
    calibration_result = model.calibrate(
        measured_ipc=measured_ipc,
        measured_counters=measured_counters,
        tolerance_percent=2.0,
        verbose=True
    )
    
    print("\nCALIBRATION SUMMARY:")
    print(f"  Measured IPC:    {calibration_result.measured_ipc:.4f}")
    print(f"  Predicted IPC:   {calibration_result.predicted_ipc:.4f}")
    print(f"  Error:           {calibration_result.error_percent:.2f}%")
    print(f"  Iterations:      {calibration_result.iterations}")
    print(f"  Converged:       {calibration_result.converged}")
    
    # Export results
    model.export_results('baseline_results.json', result)
    
    print("\n" + "=" * 80)
    print("Example run complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
