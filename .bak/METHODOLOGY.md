# Grey-Box CPU Performance Modeling Methodology

## A Rigorous Framework for Microprocessor Analysis

**Version:** 2.0  
**Date:** January 24, 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Theoretical Foundation](#2-theoretical-foundation)
3. [Model Architecture](#3-model-architecture)
4. [Parameter Classification](#4-parameter-classification)
5. [Calibration Framework](#5-calibration-framework)
6. [Validation Protocol](#6-validation-protocol)
7. [Implementation Guide](#7-implementation-guide)
8. [Limitations and Extensions](#8-limitations-and-extensions)

---

## 1. Introduction

### 1.1 What is Grey-Box Modeling?

Grey-box modeling combines the interpretability of white-box (physics-based) models with the flexibility of black-box (data-driven) models:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  WHITE-BOX                 GREY-BOX                 BLACK-BOX   │
│  ─────────                 ────────                 ─────────   │
│                                                                 │
│  Known physics      =   Known structure      +    Unknown       │
│  All parameters         Some parameters          parameters    │
│  known                  known, some              learned from  │
│                         calibrated               data alone    │
│                                                                 │
│  Example:               Example:                 Example:       │
│  Pipeline stages        Pipeline + tuned         Neural network │
│  from datasheet         memory latency           IPC predictor  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Why Grey-Box for CPUs?

| Approach | Pros | Cons |
|----------|------|------|
| **White-box** (cycle-accurate sim) | Highest accuracy | Slow, complex, requires full details |
| **Black-box** (ML) | Fast, flexible | No interpretability, needs lots of data |
| **Grey-box** (this project) | Interpretable, efficient | Requires architectural knowledge |

Grey-box provides the sweet spot: **interpretable results** with **reasonable accuracy** and **low computational cost**.

### 1.3 Target Accuracy

| Metric | Target | Acceptable |
|--------|--------|------------|
| IPC prediction error | < 3% | < 5% |
| Bottleneck identification | Correct stage | ±1 stage |
| Relative comparisons | Correct ranking | Correct direction |

---

## 2. Theoretical Foundation

### 2.1 Queueing Theory Basics

A processor pipeline can be modeled as a **queueing network** where:
- **Customers** = Instructions
- **Servers** = Pipeline stages
- **Service time** = Cycles to process an instruction at each stage

#### M/M/1 Queue

The basic building block is the M/M/1 queue:
- **M**: Markovian (exponential) arrivals
- **M**: Markovian (exponential) service
- **1**: Single server

**Key formulas:**

```
Arrival rate:        λ (instructions per cycle)
Service rate:        μ = 1/S (where S = service time in cycles)
Utilization:         ρ = λ/μ = λ × S
Queue length:        L = ρ/(1-ρ)
Wait time:           W = S/(1-ρ)
Response time:       R = W (for M/M/1)
```

**Stability condition:** ρ < 1 (arrival rate must be less than service rate)

### 2.2 Jackson Networks

For a series of queues (pipeline stages), **Jackson's theorem** allows us to analyze each queue independently:

```
λ → [Stage 1] → [Stage 2] → [Stage 3] → ... → [Stage N] → output
        ↓           ↓           ↓                 ↓
       W₁          W₂          W₃               Wₙ

Total response time: R = W₁ + W₂ + W₃ + ... + Wₙ
CPI = R (cycles per instruction)
IPC = 1/CPI
```

**Burke's theorem:** The departure process from an M/M/1 queue is also Poisson with rate λ, allowing the series decomposition.

### 2.3 Bottleneck Analysis

The **bottleneck** is the stage with highest utilization:

```
Bottleneck stage = argmax(ρᵢ) = argmax(λ × Sᵢ)

At the bottleneck:
- Queue length grows fastest
- Small increases in λ cause large delays
- Overall throughput is limited
```

**Optimization principle:** Reduce service time of bottleneck stage for maximum impact.

---

## 3. Model Architecture

### 3.1 Basic Pipeline Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    CPU PIPELINE QUEUEING MODEL                   │
│                                                                  │
│    λ (arrival rate)                                              │
│         ↓                                                        │
│    ┌─────────┐                                                   │
│    │  FETCH  │  S_fetch = (1-p_miss)×1 + p_miss×L_miss          │
│    └────┬────┘                                                   │
│         ↓                                                        │
│    ┌─────────┐                                                   │
│    │ DECODE  │  S_decode = 1 (typically)                         │
│    └────┬────┘                                                   │
│         ↓                                                        │
│    ┌─────────┐                                                   │
│    │ EXECUTE │  S_execute = Σ(pᵢ × cyclesᵢ) for each instr type │
│    └────┬────┘                                                   │
│         ↓                                                        │
│    ┌─────────┐                                                   │
│    │ MEMORY  │  S_memory = p_mem × [(1-p_miss)×1 + p_miss×L]    │
│    └────┬────┘                                                   │
│         ↓                                                        │
│    ┌─────────┐                                                   │
│    │WRITEBACK│  S_writeback = 1 (typically)                      │
│    └────┬────┘                                                   │
│         ↓                                                        │
│    Completed instructions                                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Extended Models

#### Prefetch Queue Model (8086, 80286)

```
         ┌─────────────────────┐
         │    BUS INTERFACE    │
         │    UNIT (BIU)       │
         │  ┌───────────────┐  │
Memory → │  │ Prefetch Queue│  │ → Instructions
         │  │  (6 bytes)    │  │
         │  └───────────────┘  │
         └─────────┬───────────┘
                   ↓
         ┌─────────────────────┐
         │   EXECUTION UNIT    │
         │       (EU)          │
         └─────────────────────┘

Model: M/M/1/K queue (bounded buffer)
K = prefetch queue size
```

#### Superscalar Model (Pentium, 68060)

```
                    ┌─────────────┐
         ┌────────→ │  U-Pipe     │ ────────┐
         │          └─────────────┘         │
Fetch → Decode                              → Writeback
         │          ┌─────────────┐         │
         └────────→ │  V-Pipe     │ ────────┘
                    └─────────────┘

Model: Fork-join queueing network
- Instructions split probabilistically
- Must synchronize at writeback
- IPC can exceed 1.0
```

#### Cache Hierarchy Model (68020, 80486)

```
CPU → [L1 Cache] → [L2 Cache] → [Memory]
         ↓              ↓           ↓
       1 cycle      10 cycles   100 cycles

Effective latency = Σ(pᵢ × Lᵢ)
where pᵢ = probability of access at level i
```

---

## 4. Parameter Classification

### 4.1 Three Parameter Types

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  WHITE-BOX PARAMETERS (Known from architecture)                 │
│  ─────────────────────────────────────────────                 │
│  • Pipeline depth (number of stages)                           │
│  • Cache sizes (L1, L2)                                        │
│  • Register count                                              │
│  • Clock frequency                                             │
│  • Word size                                                   │
│  • Bus width                                                   │
│                                                                 │
│  Source: Datasheets, technical manuals                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GREY-BOX PARAMETERS (Measured from system)                    │
│  ──────────────────────────────────────────                    │
│  • Instruction mix (% ALU, % MUL, % branch, etc.)             │
│  • Cache miss rates (I-cache, D-cache)                        │
│  • Branch prediction accuracy                                  │
│  • Memory access patterns                                      │
│                                                                 │
│  Source: Performance counters, profiling                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  BLACK-BOX PARAMETERS (Calibrated iteratively)                 │
│  ─────────────────────────────────────────────                 │
│  • Effective memory latency                                    │
│  • Pipeline stall factors                                      │
│  • Contention coefficients                                     │
│  • Unmodeled overhead                                          │
│                                                                 │
│  Source: Calibration against measured IPC                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Typical Parameter Values

#### Instruction Mix (varies by workload)

| Instruction Type | Integer | FP-heavy | Mixed |
|------------------|---------|----------|-------|
| ALU | 40% | 20% | 35% |
| Load | 20% | 25% | 22% |
| Store | 10% | 15% | 12% |
| Branch | 15% | 10% | 15% |
| Multiply | 3% | 10% | 5% |
| Divide | 1% | 5% | 2% |
| FP | 1% | 15% | 5% |
| Other | 10% | 0% | 4% |

#### Cache Parameters

| Era | L1 Size | L1 Hit Rate | L2 Size | L2 Hit Rate |
|-----|---------|-------------|---------|-------------|
| Pre-cache | N/A | N/A | N/A | N/A |
| Early cache (68020) | 256B | 85% | N/A | N/A |
| 1990s (486) | 8KB | 95% | 256KB | 98% |
| Modern | 32KB+ | 98% | 256KB+ | 99% |

---

## 5. Calibration Framework

### 5.1 Calibration Process

```
┌──────────────────────────────────────────────────────────────┐
│                    CALIBRATION WORKFLOW                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INITIALIZE                                               │
│     • Set white-box parameters from datasheet               │
│     • Set grey-box parameters from typical workload         │
│     • Set black-box parameters to initial guesses           │
│                                                              │
│  2. PREDICT                                                  │
│     • Run queueing model                                     │
│     • Calculate predicted IPC                                │
│                                                              │
│  3. COMPARE                                                  │
│     • Calculate error vs measured/published IPC             │
│     • error = |IPC_predicted - IPC_measured| / IPC_measured │
│                                                              │
│  4. CHECK CONVERGENCE                                        │
│     • If error < tolerance (e.g., 3%): DONE                 │
│     • Else: continue to step 5                              │
│                                                              │
│  5. ADJUST                                                   │
│     • Modify black-box parameters                           │
│     • Use gradient descent or binary search                 │
│     • Go back to step 2                                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 Calibration Algorithm

```python
def calibrate(model, measured_ipc, tolerance=0.03, max_iterations=50):
    """
    Calibrate model to match measured IPC.
    
    Primary calibration parameter: effective_memory_latency
    """
    
    # Initial bounds for memory latency
    L_min, L_max = 5, 200  # cycles
    
    for iteration in range(max_iterations):
        # Binary search for optimal memory latency
        L_mid = (L_min + L_max) / 2
        model.set_memory_latency(L_mid)
        
        predicted_ipc = model.predict_ipc()
        error = abs(predicted_ipc - measured_ipc) / measured_ipc
        
        if error < tolerance:
            return {
                'converged': True,
                'iterations': iteration,
                'memory_latency': L_mid,
                'error': error
            }
        
        # Adjust search bounds
        if predicted_ipc > measured_ipc:
            L_min = L_mid  # Need more latency (slower)
        else:
            L_max = L_mid  # Need less latency (faster)
    
    return {'converged': False, 'error': error}
```

### 5.3 Multi-Parameter Calibration

For complex models with multiple calibration parameters:

```python
def multi_calibrate(model, measured_ipc, params_to_calibrate):
    """
    Use scipy.optimize for multi-parameter calibration.
    """
    from scipy.optimize import minimize
    
    def objective(param_values):
        for name, value in zip(params_to_calibrate, param_values):
            model.set_parameter(name, value)
        predicted = model.predict_ipc()
        return (predicted - measured_ipc) ** 2
    
    result = minimize(objective, initial_guess, method='Nelder-Mead')
    return result
```

---

## 6. Validation Protocol

### 6.1 Validation Sources

| Source | Reliability | Availability |
|--------|-------------|--------------|
| Manufacturer specs | High | Good for major CPUs |
| Published benchmarks | Medium-High | Varies |
| Academic papers | High | Limited coverage |
| Cycle-accurate emulators | Very High | Limited to popular CPUs |
| Community measurements | Medium | Good for retro CPUs |

### 6.2 Validation Benchmarks

| Benchmark | Type | Best For |
|-----------|------|----------|
| Dhrystone | Integer | Overall integer IPC |
| Whetstone | FP | FP performance |
| SPEC | Mixed | Modern CPUs |
| CoreMark | Embedded | MCUs |
| Custom loops | Specific | Targeted validation |

### 6.3 Validation Criteria

```
Model is VALIDATED if:

1. IPC error < 5% on primary benchmark
2. Correct bottleneck identification (±1 stage)
3. Correct relative ranking vs similar processors
4. Sensible sensitivity analysis results
5. Consistent behavior across workload variations
```

### 6.4 Cross-Validation

For processors in the same family, validate consistency:

```
Example: Intel 8086 family

8086 IPC ≈ 0.12
8088 IPC ≈ 0.10 (8-bit bus penalty)
80186 IPC ≈ 0.12 (same as 8086, integrated)
80286 IPC ≈ 0.15 (pipeline improvements)

Consistency check: 8088 < 8086 ≈ 80186 < 80286 ✓
```

---

## 7. Implementation Guide

### 7.1 Model File Structure

```
ProcessorName/
├── processor_model.py      # Main Python implementation
├── processor_model.json    # Configuration file
├── PROCESSOR_README.md     # Documentation
├── QUICK_START.md          # Quick reference
└── PROJECT_SUMMARY.md      # Executive summary
```

### 7.2 JSON Configuration Template

```json
{
  "model_metadata": {
    "name": "Processor Name",
    "version": "1.0",
    "date": "YYYY-MM-DD",
    "target_cpu": "Processor (Year)"
  },
  "architecture": {
    "word_size_bits": 32,
    "data_bus_width_bits": 32,
    "address_bus_width_bits": 32,
    "clock_frequency_mhz": 10.0,
    "registers": 16,
    "pipeline_stages": 5,
    "transistor_count": 100000
  },
  "instruction_mix": {
    "alu_operations": 0.40,
    "memory_load": 0.20,
    "memory_store": 0.10,
    "branch": 0.15,
    "other": 0.15
  },
  "instruction_timings": {
    "alu_simple": 1,
    "alu_complex": 3,
    "memory_load": 4,
    "memory_store": 4,
    "branch_taken": 3,
    "branch_not_taken": 1
  },
  "memory_system": {
    "cache_size_kb": 8,
    "cache_hit_rate": 0.95,
    "cache_hit_cycles": 1,
    "cache_miss_cycles": 50
  },
  "calibration": {
    "target_ipc": 0.25,
    "tolerance_percent": 3.0
  }
}
```

### 7.3 Python Implementation Template

```python
#!/usr/bin/env python3
"""
Processor Name CPU Queueing Model (Year)

Brief description of the processor and its significance.

Author: Grey-Box Performance Modeling Research
Date: YYYY-MM-DD
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class QueueMetrics:
    """Metrics for a single queueing stage."""
    name: str
    arrival_rate: float
    service_time: float
    utilization: float
    queue_length: float
    wait_time: float
    response_time: float

class ProcessorQueueModel:
    """Grey-box queueing model for Processor."""
    
    def __init__(self, config_file: str):
        """Load configuration from JSON file."""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self._compute_service_times()
    
    def _compute_service_times(self):
        """Calculate service times for each pipeline stage."""
        mix = self.config['instruction_mix']
        timings = self.config['instruction_timings']
        
        # Weighted average execution time
        self.execute_service_time = (
            mix['alu_operations'] * timings['alu_simple'] +
            mix['memory_load'] * timings['memory_load'] +
            # ... etc
        )
    
    def _mm1_metrics(self, name: str, arrival_rate: float, 
                     service_time: float) -> QueueMetrics:
        """Calculate M/M/1 queue metrics."""
        utilization = arrival_rate * service_time
        
        if utilization >= 1.0:
            # Queue is unstable
            return QueueMetrics(
                name=name, arrival_rate=arrival_rate,
                service_time=service_time, utilization=1.0,
                queue_length=float('inf'), wait_time=float('inf'),
                response_time=float('inf')
            )
        
        queue_length = utilization / (1 - utilization)
        wait_time = service_time / (1 - utilization)
        
        return QueueMetrics(
            name=name, arrival_rate=arrival_rate,
            service_time=service_time, utilization=utilization,
            queue_length=queue_length, wait_time=wait_time,
            response_time=wait_time
        )
    
    def predict_ipc(self, arrival_rate: float) -> Tuple[float, List[QueueMetrics]]:
        """
        Predict IPC for given instruction arrival rate.
        
        Returns:
            Tuple of (predicted_ipc, list_of_stage_metrics)
        """
        metrics = []
        
        # Model each pipeline stage
        fetch = self._mm1_metrics('Fetch', arrival_rate, self.fetch_service_time)
        decode = self._mm1_metrics('Decode', arrival_rate, self.decode_service_time)
        execute = self._mm1_metrics('Execute', arrival_rate, self.execute_service_time)
        memory = self._mm1_metrics('Memory', arrival_rate, self.memory_service_time)
        writeback = self._mm1_metrics('Writeback', arrival_rate, self.wb_service_time)
        
        metrics = [fetch, decode, execute, memory, writeback]
        
        # Total CPI is sum of response times
        total_cpi = sum(m.response_time for m in metrics)
        ipc = 1.0 / total_cpi if total_cpi > 0 else 0.0
        
        return ipc, metrics
    
    def find_bottleneck(self, arrival_rate: float) -> str:
        """Identify the bottleneck stage."""
        _, metrics = self.predict_ipc(arrival_rate)
        bottleneck = max(metrics, key=lambda m: m.utilization)
        return bottleneck.name
    
    def calibrate(self, measured_ipc: float, 
                  tolerance: float = 0.03) -> Dict:
        """Calibrate model to match measured IPC."""
        # Implementation of calibration algorithm
        pass

def main():
    """Example usage."""
    model = ProcessorQueueModel('processor_model.json')
    
    arrival_rate = 0.10
    ipc, metrics = model.predict_ipc(arrival_rate)
    
    print(f"Predicted IPC: {ipc:.4f}")
    print(f"Bottleneck: {model.find_bottleneck(arrival_rate)}")
    
    print("\nStage Metrics:")
    for m in metrics:
        print(f"  {m.name}: ρ={m.utilization:.3f}, L={m.queue_length:.2f}")

if __name__ == "__main__":
    main()
```

---

## 8. Limitations and Extensions

### 8.1 Current Limitations

| Limitation | Impact | Workaround |
|------------|--------|------------|
| Exponential service times | May underestimate variance | Use deterministic for known timings |
| No branch prediction detail | ~5% error for branchy code | Add branch predictor model |
| Simplified cache model | Miss rate abstraction | Multi-level cache model |
| No OoO execution | Can't model modern CPUs | Requires major extension |
| Single-threaded | No SMT/multi-core | Separate per-core models |

### 8.2 Planned Extensions

#### Out-of-Order Execution Model

```
                    ┌─────────────────┐
Fetch → Decode →    │ Instruction     │ → Execute → Commit
                    │ Window / ROB    │
                    └─────────────────┘
                    
Model: G/G/m queue with reordering
- Instructions enter in-order
- Execute out-of-order (when ready)
- Commit in-order (ROB)
```

#### Branch Prediction Model

```
Branch outcome:
  - Predicted correctly (p_correct): 1 cycle
  - Mispredicted (1 - p_correct): flush_penalty cycles
  
Effective branch time = p_correct × 1 + (1 - p_correct) × flush_penalty
```

#### Multi-Level Cache Model

```
Access time = Σ (access_probability_i × latency_i)

Where:
  L1 hit:  p_L1 × L1_latency
  L2 hit:  (1-p_L1) × p_L2 × L2_latency  
  Memory:  (1-p_L1) × (1-p_L2) × mem_latency
```

### 8.3 Research Directions

1. **Bayesian calibration** (Kennedy-O'Hagan framework) for uncertainty quantification
2. **Sensitivity analysis** to identify most impactful parameters
3. **Cross-architecture comparison** frameworks
4. **Automated validation** against emulators

---

## References

### Queueing Theory
- Kleinrock, L. (1976). *Queueing Systems, Volume II: Computer Applications*
- Harchol-Balter, M. (2013). *Performance Modeling and Design of Computer Systems*

### Computer Architecture
- Hennessy, J. & Patterson, D. (2017). *Computer Architecture: A Quantitative Approach*
- Shen, J. & Lipasti, M. (2013). *Modern Processor Design*

### Calibration Methods
- Kennedy, M. & O'Hagan, A. (2001). "Bayesian Calibration of Computer Models"

---

**Document Version:** 2.0  
**Last Updated:** January 24, 2026

*This methodology guide is part of the Modeling_2026 project.*
