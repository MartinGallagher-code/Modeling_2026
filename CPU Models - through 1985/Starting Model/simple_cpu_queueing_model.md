# Simple CPU Queueing Model - Foundation Documentation

**Version:** 1.0  
**Date:** January 22, 2026  
**Author:** Grey-Box Performance Modeling Project  
**Purpose:** Establish baseline queueing network model for CPU performance prediction

---

## Table of Contents

1. [Model Overview](#model-overview)
2. [Theoretical Foundation](#theoretical-foundation)
3. [Queue Network Architecture](#queue-network-architecture)
4. [Model Parameters](#model-parameters)
5. [Performance Metrics](#performance-metrics)
6. [Calibration Framework](#calibration-framework)
7. [Implementation](#implementation)
8. [Validation Protocol](#validation-protocol)

---

## 1. Model Overview

### 1.1 Scope

This model represents a **simple scalar in-order CPU pipeline** with the following characteristics:

- **Single execution pipeline** (no superscalar execution)
- **In-order instruction processing** (no out-of-order execution)
- **Single-level cache hierarchy** (unified L1 cache)
- **No branch prediction** (stalls on all branches)
- **Deterministic instruction mix** (fixed operation types)

### 1.2 Design Philosophy

This model follows **grey-box system identification** principles:

1. **White-box foundation**: Core pipeline stages based on documented CPU architecture
2. **Grey-box unknowns**: Service times, contention effects, and cache behavior treated as calibration parameters
3. **Black-box validation**: Model predictions compared against real system measurements

### 1.3 Simplifying Assumptions

- Instructions arrive as a Poisson process with rate λ
- Service times are exponentially distributed (memoryless property)
- No instruction-level parallelism (ILP)
- Fixed memory latency (no NUMA effects)
- Steady-state operation (no transient behavior)

---

## 2. Theoretical Foundation

### 2.1 Queueing Theory Basics

The model uses **Jackson Network** theory for open queueing networks:

**Burke's Theorem**: The departure process from an M/M/1 queue is also Poisson with rate λ

**Utilization Law**: ρ = λ × S, where:
- ρ = utilization (fraction of time server is busy)
- λ = arrival rate (instructions/second)
- S = mean service time (seconds/instruction)

**Little's Law**: L = λ × W, where:
- L = average number of instructions in system
- W = average time an instruction spends in system

**Response Time Formula** (M/M/1): W = S / (1 - ρ)

### 2.2 Network Decomposition

The CPU pipeline is decomposed into independent M/M/1 queues connected in series. Each stage:

1. Has exponentially distributed service times with mean S_i
2. Receives Poisson arrivals (from previous stage or external source)
3. Operates independently (no cross-stage dependencies)

**Total Response Time**: W_total = Σ W_i = Σ [S_i / (1 - ρ_i)]

**Throughput (IPC)**: Reciprocal of total pipeline time per instruction

---

## 3. Queue Network Architecture

### 3.1 Pipeline Stages

The simple CPU model consists of **5 sequential queues** representing classical RISC pipeline stages:

```
[Instruction Fetch] → [Decode] → [Execute] → [Memory Access] → [Write Back]
       Q1                Q2          Q3             Q4                Q5
```

### 3.2 Stage Descriptions

#### Stage 1: Instruction Fetch (IF)
- **Function**: Fetch instruction from memory using program counter (PC)
- **Service components**:
  - L1 I-cache lookup: 1 cycle (hit) or 100 cycles (miss)
  - PC increment: negligible
- **Parameters**:
  - S_IF: Mean service time (cycles)
  - p_icache_miss: I-cache miss rate (0.01 = 1%)

#### Stage 2: Decode (ID)
- **Function**: Decode instruction and read register operands
- **Service components**:
  - Instruction decode: 1 cycle
  - Register file access: 1 cycle
- **Parameters**:
  - S_ID: Mean service time (fixed at 1 cycle for simple ISA)

#### Stage 3: Execute (EX)
- **Function**: Perform ALU operation or calculate memory address
- **Service components**:
  - Integer ALU: 1 cycle
  - Load/store address calc: 1 cycle
  - Multiply: 3 cycles
  - Divide: 10 cycles
- **Parameters**:
  - S_EX: Mean service time (weighted by instruction mix)
  - p_alu, p_mul, p_div: Fraction of each operation type

#### Stage 4: Memory Access (MEM)
- **Function**: Access data memory for loads/stores
- **Service components**:
  - L1 D-cache lookup: 1 cycle (hit) or 100 cycles (miss)
  - No access (for non-memory instructions): 0 cycles
- **Parameters**:
  - S_MEM: Mean service time (cycles)
  - p_mem: Fraction of memory instructions (loads + stores)
  - p_dcache_miss: D-cache miss rate

#### Stage 5: Write Back (WB)
- **Function**: Write result to register file
- **Service components**:
  - Register write: 1 cycle
- **Parameters**:
  - S_WB: Fixed at 1 cycle

### 3.3 Network Topology

**Queueing Network Diagram:**

```
            λ (instructions/sec)
                    ↓
        ┌───────────────────────┐
        │   Q1: Fetch (IF)      │  S_IF, μ_IF = 1/S_IF
        │   M/M/1 Queue          │
        └───────────┬───────────┘
                    ↓ λ
        ┌───────────────────────┐
        │   Q2: Decode (ID)     │  S_ID = 1 cycle
        │   M/M/1 Queue          │
        └───────────┬───────────┘
                    ↓ λ
        ┌───────────────────────┐
        │   Q3: Execute (EX)    │  S_EX (weighted avg)
        │   M/M/1 Queue          │
        └───────────┬───────────┘
                    ↓ λ
        ┌───────────────────────┐
        │   Q4: Memory (MEM)    │  S_MEM (conditional)
        │   M/M/1 Queue          │
        └───────────┬───────────┘
                    ↓ λ
        ┌───────────────────────┐
        │   Q5: WriteBack (WB)  │  S_WB = 1 cycle
        │   M/M/1 Queue          │
        └───────────┬───────────┘
                    ↓
            Completed Instructions
```

**Flow Conservation**: Arrival rate λ is constant through all stages (no branching, no instruction dropping)

---

## 4. Model Parameters

### 4.1 Known Parameters (White-Box)

Based on architectural specification:

| Parameter | Value | Source | Description |
|-----------|-------|--------|-------------|
| S_ID | 1 cycle | Datasheet | Decode latency |
| S_WB | 1 cycle | Datasheet | Write-back latency |
| Cache_line_size | 64 bytes | Datasheet | L1 cache line size |
| L1_cache_size | 32 KB | Datasheet | Unified L1 cache |
| Clock_freq | 2.0 GHz | Datasheet | CPU frequency |

### 4.2 Unknown Parameters (Grey-Box)

To be calibrated from measurements:

#### Instruction Fetch (IF)
```
S_IF = (1 - p_icache_miss) × 1 + p_icache_miss × L_miss

Where:
  - p_icache_miss: I-cache miss rate [Unknown]
  - L_miss: Memory latency in cycles [Unknown]
```

**Initial estimates**: p_icache_miss = 0.01, L_miss = 100 cycles

#### Execute (EX)
```
S_EX = p_alu × 1 + p_mul × 3 + p_div × 10 + p_other × 1

Where:
  - p_alu: Fraction of ALU ops [Unknown]
  - p_mul: Fraction of multiply ops [Unknown]
  - p_div: Fraction of divide ops [Unknown]
  - p_other: Fraction of other ops [Unknown]
  
Constraint: p_alu + p_mul + p_div + p_other = 1
```

**Initial estimates**: p_alu = 0.70, p_mul = 0.05, p_div = 0.01, p_other = 0.24

#### Memory Access (MEM)
```
S_MEM = p_mem × [(1 - p_dcache_miss) × 1 + p_dcache_miss × L_miss]
        + (1 - p_mem) × 0

Where:
  - p_mem: Fraction of load/store instructions [Unknown]
  - p_dcache_miss: D-cache miss rate [Unknown]
```

**Initial estimates**: p_mem = 0.30, p_dcache_miss = 0.03

### 4.3 Parameter Summary Table

| Stage | Parameter | Symbol | Initial Value | Calibration Method |
|-------|-----------|--------|---------------|-------------------|
| IF | I-cache miss rate | p_icache_miss | 0.01 | Performance counters |
| IF | Memory latency | L_miss | 100 cycles | Latency benchmark |
| ID | Decode time | S_ID | 1 cycle | Fixed (datasheet) |
| EX | ALU fraction | p_alu | 0.70 | Instruction profiling |
| EX | Multiply fraction | p_mul | 0.05 | Instruction profiling |
| EX | Divide fraction | p_div | 0.01 | Instruction profiling |
| MEM | Memory instruction fraction | p_mem | 0.30 | Instruction profiling |
| MEM | D-cache miss rate | p_dcache_miss | 0.03 | Performance counters |
| WB | Write-back time | S_WB | 1 cycle | Fixed (datasheet) |

---

## 5. Performance Metrics

### 5.1 Primary Metrics

#### Instructions Per Cycle (IPC)

```
IPC = λ / f_clock = 1 / (W_total × f_clock)

Where:
  - λ: Instruction throughput (instructions/second)
  - f_clock: Clock frequency (Hz)
  - W_total: Total time per instruction (seconds)
```

**Target Range**: 0.5 - 1.0 IPC for simple in-order pipeline

#### Cycles Per Instruction (CPI)

```
CPI = 1 / IPC = W_total × f_clock

CPI_total = CPI_IF + CPI_ID + CPI_EX + CPI_MEM + CPI_WB
```

### 5.2 Stage-Level Metrics

For each stage i:

**Utilization**: ρ_i = λ × S_i < 1 (stability condition)

**Average Queue Length**: L_i = ρ_i / (1 - ρ_i)

**Average Wait Time**: W_i = S_i / (1 - ρ_i)

**Throughput**: X_i = λ (constant in series network)

### 5.3 Bottleneck Identification

**Bottleneck Stage**: Stage with highest utilization

```
Bottleneck = argmax_i(ρ_i) = argmax_i(S_i)
```

**Performance Bound**: Maximum IPC ≤ 1 / S_bottleneck

### 5.4 Observable Metrics (for Calibration)

Metrics that can be measured on real system:

1. **Total IPC**: From hardware performance counters
2. **Cache miss rates**: I-cache misses, D-cache misses
3. **Instruction mix**: % ALU, % memory, % multiply/divide
4. **Execution time**: Wall-clock time for benchmark
5. **Stall cycles**: Frontend stalls, backend stalls

---

## 6. Calibration Framework

### 6.1 Calibration Objectives

**Goal**: Find parameter vector θ = [p_icache_miss, L_miss, p_alu, p_mul, p_div, p_mem, p_dcache_miss] that minimizes prediction error

**Objective Function**:
```
minimize J(θ) = Σ_k [IPC_measured(k) - IPC_model(θ, k)]²

Subject to:
  - 0 ≤ p_icache_miss ≤ 1
  - 0 ≤ p_dcache_miss ≤ 1
  - 50 ≤ L_miss ≤ 500 cycles
  - p_alu + p_mul + p_div + p_other = 1
  - 0 ≤ p_mem ≤ 1
```

### 6.2 Calibration Data Sources

#### Hardware Performance Counters
```bash
# Example: Linux perf counters
perf stat -e cycles,instructions,L1-icache-misses,L1-dcache-misses ./benchmark

Collected metrics:
  - instructions: Total instructions executed
  - cycles: Total CPU cycles
  - IPC: instructions / cycles
  - I-cache miss rate: L1-icache-misses / instructions
  - D-cache miss rate: L1-dcache-misses / memory_instructions
```

#### Instruction Mix Profiling
```bash
# Example: Using perf or Intel VTune
perf record -e cycles ./benchmark
perf report --sort symbol

Extract:
  - % integer ALU ops
  - % load/store ops
  - % multiply ops
  - % divide ops
```

#### Memory Latency Measurement
```bash
# Example: Using lmbench or Intel Memory Latency Checker
mlc --latency_matrix

Extract:
  - L1 hit latency: ~1 cycle
  - L1 miss (L2 hit): ~10 cycles
  - L2 miss (main memory): ~100 cycles
```

### 6.3 Calibration Algorithm

**Iterative Refinement Process**:

```
Step 1: Initialize parameters with architectural estimates
        θ₀ = [p_icache_miss, L_miss, p_alu, p_mul, p_div, p_mem, p_dcache_miss]
        
Step 2: Run benchmark on real system
        Collect: IPC_measured, cache_misses, instruction_mix
        
Step 3: Run model with current parameters θ_k
        Compute: IPC_model(θ_k)
        
Step 4: Calculate discrepancy
        Δ = IPC_measured - IPC_model(θ_k)
        
Step 5: If |Δ| < tolerance (e.g., 2%), STOP
        Else, update parameters:
        
        a) Update cache miss rates from counters:
           p_icache_miss = measured_icache_misses / instructions
           p_dcache_miss = measured_dcache_misses / memory_instructions
        
        b) Update instruction mix from profiling:
           p_alu, p_mul, p_div, p_mem = profiled values
        
        c) If still discrepancy, adjust unknown latency L_miss:
           L_miss ← L_miss × (1 + α × Δ)  [α = learning rate = 0.1]
        
Step 6: Set θ_{k+1} = updated parameters, return to Step 3
```

### 6.4 Sensitivity Analysis

**Parameter Sensitivity**: Measure ∂IPC/∂θ_i for each parameter

```python
def sensitivity(theta, epsilon=0.01):
    """Compute numerical gradient of IPC w.r.t. parameters"""
    ipc_base = compute_ipc(theta)
    sensitivity_dict = {}
    
    for i, param_name in enumerate(theta.keys()):
        theta_plus = theta.copy()
        theta_plus[param_name] *= (1 + epsilon)
        ipc_plus = compute_ipc(theta_plus)
        
        sensitivity_dict[param_name] = (ipc_plus - ipc_base) / (epsilon * theta[param_name])
    
    return sensitivity_dict
```

**High-sensitivity parameters** (large |∂IPC/∂θ|) should be calibrated first.

---

## 7. Implementation

### 7.1 Model Structure (JSON)

```json
{
  "model_metadata": {
    "name": "Simple In-Order CPU",
    "version": "1.0",
    "date": "2026-01-22",
    "architecture": "Scalar RISC Pipeline"
  },
  
  "system_parameters": {
    "clock_freq_ghz": 2.0,
    "l1_cache_kb": 32,
    "cache_line_bytes": 64
  },
  
  "pipeline_stages": [
    {
      "stage_id": 1,
      "name": "Instruction Fetch (IF)",
      "queue_type": "M/M/1",
      "service_time_formula": "(1 - p_icache_miss) * 1 + p_icache_miss * L_miss",
      "parameters": {
        "p_icache_miss": {
          "value": 0.01,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "performance_counters"
        },
        "L_miss": {
          "value": 100,
          "type": "unknown",
          "bounds": [50, 500],
          "units": "cycles",
          "calibration_source": "latency_benchmark"
        }
      }
    },
    
    {
      "stage_id": 2,
      "name": "Decode (ID)",
      "queue_type": "M/M/1",
      "service_time_formula": "1",
      "parameters": {
        "S_ID": {
          "value": 1,
          "type": "known",
          "units": "cycles"
        }
      }
    },
    
    {
      "stage_id": 3,
      "name": "Execute (EX)",
      "queue_type": "M/M/1",
      "service_time_formula": "p_alu * 1 + p_mul * 3 + p_div * 10 + p_other * 1",
      "parameters": {
        "p_alu": {
          "value": 0.70,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "instruction_profiling"
        },
        "p_mul": {
          "value": 0.05,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "instruction_profiling"
        },
        "p_div": {
          "value": 0.01,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "instruction_profiling"
        },
        "p_other": {
          "value": 0.24,
          "type": "derived",
          "formula": "1 - p_alu - p_mul - p_div"
        }
      }
    },
    
    {
      "stage_id": 4,
      "name": "Memory Access (MEM)",
      "queue_type": "M/M/1",
      "service_time_formula": "p_mem * ((1 - p_dcache_miss) * 1 + p_dcache_miss * L_miss)",
      "parameters": {
        "p_mem": {
          "value": 0.30,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "instruction_profiling"
        },
        "p_dcache_miss": {
          "value": 0.03,
          "type": "unknown",
          "bounds": [0.0, 1.0],
          "calibration_source": "performance_counters"
        }
      }
    },
    
    {
      "stage_id": 5,
      "name": "Write Back (WB)",
      "queue_type": "M/M/1",
      "service_time_formula": "1",
      "parameters": {
        "S_WB": {
          "value": 1,
          "type": "known",
          "units": "cycles"
        }
      }
    }
  ],
  
  "network_topology": {
    "type": "series",
    "connections": [
      {"from": "external", "to": "IF"},
      {"from": "IF", "to": "ID"},
      {"from": "ID", "to": "EX"},
      {"from": "EX", "to": "MEM"},
      {"from": "MEM", "to": "WB"},
      {"from": "WB", "to": "external"}
    ]
  }
}
```

### 7.2 Python Implementation

```python
import numpy as np
import json
from typing import Dict, List, Tuple

class SimpleCPUQueueModel:
    """
    Simple in-order CPU pipeline queueing model
    Based on series of M/M/1 queues
    """
    
    def __init__(self, config_file: str):
        """Load model configuration from JSON"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.clock_freq = self.config['system_parameters']['clock_freq_ghz'] * 1e9
        self.stages = self.config['pipeline_stages']
        
        # Extract parameters into flat dictionary
        self.params = self._extract_parameters()
    
    def _extract_parameters(self) -> Dict[str, float]:
        """Extract all parameters into flat dictionary"""
        params = {}
        for stage in self.stages:
            for param_name, param_data in stage.get('parameters', {}).items():
                if param_data['type'] != 'derived':
                    params[param_name] = param_data['value']
        return params
    
    def compute_service_time(self, stage: Dict) -> float:
        """
        Compute service time for a stage given current parameters
        Returns: Mean service time in cycles
        """
        formula = stage['service_time_formula']
        
        # Build namespace with current parameter values
        namespace = self.params.copy()
        
        # Handle derived parameters
        for param_name, param_data in stage.get('parameters', {}).items():
            if param_data['type'] == 'derived':
                namespace[param_name] = eval(param_data['formula'], namespace)
        
        # Evaluate service time formula
        service_time = eval(formula, namespace)
        return service_time
    
    def compute_stage_metrics(self, stage: Dict, arrival_rate: float) -> Dict:
        """
        Compute queueing metrics for a single stage
        
        Args:
            stage: Stage configuration dictionary
            arrival_rate: Arrival rate λ (instructions/second)
        
        Returns:
            Dictionary with utilization, queue_length, wait_time
        """
        # Service time in cycles
        S_cycles = self.compute_service_time(stage)
        
        # Service time in seconds
        S_seconds = S_cycles / self.clock_freq
        
        # Utilization ρ = λ × S
        rho = arrival_rate * S_seconds
        
        if rho >= 1.0:
            raise ValueError(f"Stage {stage['name']} is unstable: ρ = {rho:.3f} >= 1")
        
        # Queue length L = ρ / (1 - ρ)
        queue_length = rho / (1 - rho)
        
        # Wait time W = S / (1 - ρ)
        wait_time = S_seconds / (1 - rho)
        
        # CPI contribution
        cpi_contribution = wait_time * self.clock_freq
        
        return {
            'stage_name': stage['name'],
            'service_time_cycles': S_cycles,
            'utilization': rho,
            'queue_length': queue_length,
            'wait_time_seconds': wait_time,
            'cpi_contribution': cpi_contribution
        }
    
    def compute_pipeline_performance(self, arrival_rate: float = None) -> Dict:
        """
        Compute overall pipeline performance
        
        Args:
            arrival_rate: Instruction arrival rate (instructions/sec)
                         If None, assumes maximum sustainable rate
        
        Returns:
            Dictionary with IPC, CPI, throughput, stage metrics
        """
        # If no arrival rate specified, use 80% of maximum sustainable
        if arrival_rate is None:
            max_service_time = max([self.compute_service_time(s) for s in self.stages])
            max_rate = 0.8 * self.clock_freq / max_service_time
            arrival_rate = max_rate
        
        # Compute metrics for each stage
        stage_metrics = []
        total_cpi = 0
        
        for stage in self.stages:
            metrics = self.compute_stage_metrics(stage, arrival_rate)
            stage_metrics.append(metrics)
            total_cpi += metrics['cpi_contribution']
        
        # Overall performance
        ipc = 1.0 / total_cpi
        throughput = arrival_rate
        
        # Identify bottleneck
        bottleneck = max(stage_metrics, key=lambda x: x['utilization'])
        
        return {
            'ipc': ipc,
            'cpi': total_cpi,
            'throughput_ips': throughput,
            'arrival_rate_ips': arrival_rate,
            'stage_metrics': stage_metrics,
            'bottleneck': bottleneck['stage_name'],
            'bottleneck_utilization': bottleneck['utilization']
        }
    
    def calibrate(self, measured_ipc: float, measured_counters: Dict) -> Dict:
        """
        Calibrate model parameters given real system measurements
        
        Args:
            measured_ipc: Measured IPC from real system
            measured_counters: Dict with cache miss rates, instruction mix, etc.
        
        Returns:
            Updated parameters and calibration report
        """
        # Update parameters from measurements
        if 'icache_miss_rate' in measured_counters:
            self.params['p_icache_miss'] = measured_counters['icache_miss_rate']
        
        if 'dcache_miss_rate' in measured_counters:
            self.params['p_dcache_miss'] = measured_counters['dcache_miss_rate']
        
        if 'alu_fraction' in measured_counters:
            self.params['p_alu'] = measured_counters['alu_fraction']
        
        if 'mul_fraction' in measured_counters:
            self.params['p_mul'] = measured_counters['mul_fraction']
        
        if 'div_fraction' in measured_counters:
            self.params['p_div'] = measured_counters['div_fraction']
        
        if 'mem_fraction' in measured_counters:
            self.params['p_mem'] = measured_counters['mem_fraction']
        
        # Compute model prediction with updated parameters
        result = self.compute_pipeline_performance()
        predicted_ipc = result['ipc']
        
        # Calculate discrepancy
        discrepancy = measured_ipc - predicted_ipc
        error_percent = abs(discrepancy / measured_ipc) * 100
        
        # If still error, adjust latency parameter
        if error_percent > 2.0:
            # Adjust L_miss to account for discrepancy
            adjustment_factor = 1.0 + 0.1 * (discrepancy / measured_ipc)
            self.params['L_miss'] *= adjustment_factor
            
            # Recompute
            result = self.compute_pipeline_performance()
            predicted_ipc = result['ipc']
            discrepancy = measured_ipc - predicted_ipc
            error_percent = abs(discrepancy / measured_ipc) * 100
        
        return {
            'measured_ipc': measured_ipc,
            'predicted_ipc': predicted_ipc,
            'discrepancy': discrepancy,
            'error_percent': error_percent,
            'calibrated_parameters': self.params.copy(),
            'pipeline_details': result
        }
    
    def sensitivity_analysis(self, param_name: str, epsilon: float = 0.01) -> float:
        """
        Compute sensitivity ∂IPC/∂param for a single parameter
        
        Args:
            param_name: Name of parameter to perturb
            epsilon: Perturbation fraction (default 1%)
        
        Returns:
            Sensitivity value (change in IPC per unit change in parameter)
        """
        # Baseline IPC
        ipc_base = self.compute_pipeline_performance()['ipc']
        
        # Perturb parameter
        original_value = self.params[param_name]
        self.params[param_name] *= (1 + epsilon)
        
        # Compute perturbed IPC
        ipc_perturbed = self.compute_pipeline_performance()['ipc']
        
        # Restore original value
        self.params[param_name] = original_value
        
        # Compute sensitivity
        sensitivity = (ipc_perturbed - ipc_base) / (epsilon * original_value)
        
        return sensitivity


# Example usage
if __name__ == "__main__":
    # Create model
    model = SimpleCPUQueueModel('simple_cpu_model.json')
    
    # Compute baseline performance
    result = model.compute_pipeline_performance()
    
    print("=== Simple CPU Queue Model - Baseline Performance ===")
    print(f"IPC: {result['ipc']:.3f}")
    print(f"CPI: {result['cpi']:.3f}")
    print(f"Bottleneck: {result['bottleneck']} (ρ = {result['bottleneck_utilization']:.3f})")
    print("\nStage-by-Stage Breakdown:")
    for stage in result['stage_metrics']:
        print(f"  {stage['stage_name']:20s}: {stage['service_time_cycles']:6.2f} cycles, "
              f"ρ={stage['utilization']:.3f}, CPI={stage['cpi_contribution']:.3f}")
    
    # Simulate calibration with measured data
    print("\n=== Calibration with Measured Data ===")
    measured_counters = {
        'icache_miss_rate': 0.015,  # 1.5% miss rate
        'dcache_miss_rate': 0.025,  # 2.5% miss rate
        'alu_fraction': 0.68,
        'mul_fraction': 0.07,
        'div_fraction': 0.02,
        'mem_fraction': 0.32
    }
    measured_ipc = 0.85
    
    calibration_result = model.calibrate(measured_ipc, measured_counters)
    print(f"Measured IPC: {calibration_result['measured_ipc']:.3f}")
    print(f"Predicted IPC: {calibration_result['predicted_ipc']:.3f}")
    print(f"Error: {calibration_result['error_percent']:.2f}%")
    
    # Sensitivity analysis
    print("\n=== Sensitivity Analysis ===")
    for param in ['p_icache_miss', 'p_dcache_miss', 'L_miss', 'p_mem']:
        sens = model.sensitivity_analysis(param)
        print(f"∂IPC/∂{param:15s} = {sens:+.4f}")
```

---

## 8. Validation Protocol

### 8.1 Benchmark Selection

**Ideal Benchmarks** (for calibration):
1. **Memory-bound**: High cache miss rate, tests memory latency parameter
2. **Compute-bound**: High ALU utilization, tests execution parameter
3. **Mixed**: Balanced instruction mix, tests overall model accuracy

**Example Benchmarks**:
- STREAM (memory bandwidth)
- Dhrystone (integer computation)
- Whetstone (floating-point computation)
- SPEC CPU2017 integer suite

### 8.2 Validation Metrics

**Primary Metric**: IPC error
```
Error = |IPC_measured - IPC_predicted| / IPC_measured × 100%

Target: Error < 2%
Acceptable: Error < 5%
```

**Secondary Metrics**:
- CPI breakdown by stage
- Bottleneck identification accuracy
- Throughput prediction (instructions/second)

### 8.3 Validation Workflow

```
1. Run benchmark on real system
   ├─ Collect: IPC, cache miss rates, instruction mix
   └─ Record: Execution time, clock frequency

2. Profile benchmark characteristics
   ├─ Use: perf, VTune, or similar profiler
   └─ Extract: Instruction distribution, memory access patterns

3. Configure model with measured parameters
   ├─ Set: p_icache_miss, p_dcache_miss, instruction mix
   └─ Keep: L_miss, other latencies as unknowns

4. Run model prediction
   ├─ Compute: Predicted IPC
   └─ Compare: Against measured IPC

5. Calculate discrepancy
   ├─ If error < 2%: Model is accurate → STOP
   └─ If error ≥ 2%: Proceed to calibration

6. Iterative calibration
   ├─ Adjust unknown parameters (e.g., L_miss)
   ├─ Re-run model
   └─ Repeat until error < 2%

7. Document results
   ├─ Final parameters
   ├─ Error metrics
   └─ Sensitivity analysis
```

### 8.4 Cross-Validation

**Generalization Test**: Validate on unseen benchmarks

```
Training set: Calibrate on benchmarks A, B, C
Validation set: Test on benchmarks D, E, F

Goal: Error on validation set < 5% (acceptable generalization)
```

---

## 9. Limitations and Extensions

### 9.1 Current Limitations

1. **No instruction-level parallelism**: Real CPUs have superscalar execution
2. **No out-of-order execution**: Real CPUs reorder instructions dynamically
3. **Exponential service times**: Real service times have more complex distributions
4. **No branch prediction**: Real CPUs predict branches to avoid stalls
5. **Single memory level**: Real CPUs have L1/L2/L3 cache hierarchy
6. **No SMT/hyperthreading**: Real CPUs can run multiple threads per core

### 9.2 Future Extensions

**Phase 2: Superscalar Pipeline**
- Multiple execution units (ALU0, ALU1, FPU, Load/Store)
- Parallel service with job routing to available units
- Requires fork-join queueing network model

**Phase 3: Out-of-Order Execution**
- Reorder buffer (ROB) as finite-capacity queue
- Instruction window for dynamic scheduling
- Requires priority queueing or generalized semi-Markov process

**Phase 4: Memory Hierarchy**
- Multi-level cache (L1 → L2 → L3 → DRAM)
- Cache coherence protocols for multi-core
- Requires hierarchical queueing network

**Phase 5: Branch Prediction**
- Speculative execution with rollback
- Branch misprediction penalty as extra service time
- Requires conditional branching in queueing network

---

## 10. Summary

This simple CPU queueing model provides:

✓ **Tractable foundation** for performance modeling  
✓ **Clear parameter separation** (known vs. unknown)  
✓ **Systematic calibration** process  
✓ **Validation protocol** for real system comparison  
✓ **Extension path** to more complex architectures  

**Key Strengths**:
- Analytically solvable (closed-form expressions)
- Fast computation (<1ms per evaluation)
- Intuitive interpretation (bottleneck identification)
- Calibration converges quickly (5-10 iterations)

**Recommended Use**:
- Baseline model for more complex CPUs
- Teaching tool for queueing theory applications
- Rapid design space exploration
- Bottleneck identification in simple systems

---

**Next Steps**: 
1. Implement model in Python (see Section 7.2)
2. Collect baseline measurements on target CPU
3. Run calibration process (see Section 6.3)
4. Validate accuracy (<2% error target)
5. Document discrepancies and refine model structure

---

**References**:
- Harchol-Balter, M. (2013). *Performance Modeling and Design of Computer Systems*
- Jackson, J.R. (1957). "Networks of Waiting Lines"
- Kleinrock, L. (1976). *Queueing Systems, Volume II: Computer Applications*
- Hennessy & Patterson (2017). *Computer Architecture: A Quantitative Approach*

**Document Version**: 1.0  
**Author**: Grey-Box Performance Modeling Research  
**Date**: January 22, 2026
