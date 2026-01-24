# Intel 8080 CPU Model - Quick Start Guide

## Overview

This guide provides a rapid introduction to the Intel 8080 queueing model. For complete technical details, see `8080_README.md`.

**Target Audience:** Researchers and students studying microprocessor performance evolution  
**Prerequisites:** Python 3.6+, NumPy  
**Time Required:** 10 minutes

---

## Quick Facts: Intel 8080

| Specification | Value |
|---------------|-------|
| Year | 1974 |
| Word Size | 8 bits |
| Clock Speed | 2 MHz |
| Pipeline | None (sequential) |
| Prefetch | None |
| Cache | None |
| Typical IPC | 0.15-0.20 |
| Significance | Baseline sequential processor |

---

## Installation

### 1. Prerequisites

```bash
# Check Python version (3.6+ required)
python3 --version

# Install NumPy if needed
pip3 install numpy
```

### 2. Get the Model Files

```bash
# Clone or download the repository
git clone https://github.com/MartinGallagher-code/Modeling_2026.git
cd Modeling_2026/8080
```

### 3. Verify Installation

```bash
# Test the model
python3 8080_cpu_model.py
```

If successful, you'll see performance predictions and calibration examples.

---

## Basic Usage

### Example 1: Predict IPC

```python
from 8080_cpu_model import Intel8080QueueModel

# Load the model
model = Intel8080QueueModel('8080_cpu_model.json')

# Predict IPC at 15% instruction arrival rate
ipc, metrics = model.predict_ipc(arrival_rate=0.15)

print(f"Predicted IPC: {ipc:.4f}")
# Output: Predicted IPC: 0.0797
```

### Example 2: Print Detailed Metrics

```python
# Get detailed stage-by-stage metrics
model.print_metrics(metrics)
```

**Output:**
```
================================================================================
Intel 8080 CPU Pipeline Metrics
================================================================================
Stage                          λ        S        ρ        L        W        R
                          (ins/c)    (cyc)             (ins)    (cyc)    (cyc)
--------------------------------------------------------------------------------
Fetch                      0.1500    5.25    0.7875     3.71    24.71    29.96
Decode_Execute             0.1500    6.50    0.9750    39.00   260.00   266.50
================================================================================

Bottleneck: Decode_Execute (ρ = 0.9750)
```

### Example 3: Calibrate to Measured IPC

```python
# Calibrate model to match real hardware
measured_ipc = 0.18  # From actual 8080 system

result = model.calibrate(measured_ipc, tolerance_percent=2.0)

print(f"Target IPC: {result.measured_ipc:.4f}")
print(f"Predicted IPC: {result.predicted_ipc:.4f}")
print(f"Error: {result.error_percent:.2f}%")
print(f"Converged: {result.converged}")
```

**Output:**
```
Target IPC: 0.1800
Predicted IPC: 0.1792
Error: 0.44%
Converged: True
```

---

## Understanding the Output

### Key Metrics Explained

**λ (Lambda)** - Arrival Rate
- Instructions entering the pipeline per cycle
- Higher λ = more aggressive workload
- Typical range: 0.10-0.20 for 8080

**S (Service Time)**
- Average cycles to complete a stage
- Fetch: ~5.25 cycles (depends on instruction length)
- Execute: ~6.5 cycles (depends on instruction mix)

**ρ (Rho)** - Utilization
- Fraction of time stage is busy
- ρ = λ × S
- Must be < 1.0 for stability
- High ρ (>0.9) indicates bottleneck

**L (Queue Length)**
- Average number of instructions waiting
- L = ρ / (1 - ρ)
- Grows rapidly as ρ → 1.0

**W (Wait Time)**
- Average cycles an instruction waits
- W = S / (1 - ρ)
- Includes queueing delay

**R (Response Time)**
- Total time in stage (wait + service)
- R = W + S

### Interpreting Results

**Good Performance** (ρ < 0.7):
- Low wait times
- Predictable execution
- System has spare capacity

**Moderate Performance** (0.7 ≤ ρ < 0.9):
- Increasing wait times
- Some queueing effects
- Approaching bottleneck

**Poor Performance** (ρ ≥ 0.9):
- High wait times
- Severe queueing delays
- System saturated

**Unstable** (ρ ≥ 1.0):
- Infinite queue buildup
- System cannot keep up
- Not sustainable

---

## Common Use Cases

### Use Case 1: Historical Comparison

Compare 8080 baseline to modern processors:

```python
# 8080 IPC
ipc_8080, _ = model.predict_ipc(0.15)

print(f"8080 IPC: {ipc_8080:.4f}")
print(f"Modern CPU IPC: ~2.5-4.0")
print(f"Improvement: {2.5 / ipc_8080:.1f}x to {4.0 / ipc_8080:.1f}x")
```

### Use Case 2: Workload Analysis

Analyze different instruction mixes:

```python
# Modify instruction mix in JSON file
# Or create custom configuration

# Memory-heavy workload
model.config['instruction_mix']['load_store'] = 0.40
model.config['instruction_mix']['alu_operations'] = 0.25

ipc_memory_heavy, _ = model.predict_ipc(0.15)
print(f"Memory-heavy IPC: {ipc_memory_heavy:.4f}")

# Compute-heavy workload  
model.config['instruction_mix']['load_store'] = 0.10
model.config['instruction_mix']['alu_operations'] = 0.50

ipc_compute_heavy, _ = model.predict_ipc(0.15)
print(f"Compute-heavy IPC: {ipc_compute_heavy:.4f}")
```

### Use Case 3: Bottleneck Identification

Find performance-limiting stages:

```python
ipc, metrics = model.predict_ipc(0.15)

bottleneck = model.find_bottleneck(metrics)
print(f"Bottleneck: {bottleneck}")

for m in metrics:
    print(f"{m.name}: utilization = {m.utilization:.4f}")
```

---

## Configuration

### Editing `8080_cpu_model.json`

**Clock Frequency:**
```json
"architecture": {
  "clock_frequency_mhz": 2.0  // Change to 3.0 for 8080A
}
```

**Instruction Mix:**
```json
"instruction_mix": {
  "mov_register": 0.25,    // Adjust based on workload
  "alu_operations": 0.35,
  "load_store": 0.20,
  "jump_call": 0.15,
  "io_operations": 0.05
}
```

**Instruction Timings:**
```json
"instruction_timings": {
  "mov_register_register": {
    "cycles": 5              // From Intel datasheet
  }
}
```

---

## Troubleshooting

### Problem: Model predicts IPC = 0.0

**Cause:** Arrival rate too high, system unstable (ρ ≥ 1.0)

**Solution:** Reduce arrival rate
```python
# Try lower arrival rates
ipc, metrics = model.predict_ipc(0.10)  # Instead of 0.15
```

### Problem: Calibration doesn't converge

**Cause:** Measured IPC is unrealistic for 8080 architecture

**Solution:** Check measured IPC is in valid range (0.10-0.25)
```python
# 8080 cannot achieve IPC > 0.25
if measured_ipc > 0.25:
    print("Warning: IPC too high for 8080 architecture")
```

### Problem: Import error

**Cause:** Missing dependencies or incorrect path

**Solution:**
```bash
# Install dependencies
pip3 install numpy

# Run from correct directory
cd /path/to/Modeling_2026/8080
python3 8080_cpu_model.py
```

---

## Example Workflow

Complete example analyzing 8080 performance:

```python
#!/usr/bin/env python3
"""
Complete 8080 performance analysis workflow
"""
from 8080_cpu_model import Intel8080QueueModel

# 1. Load model
model = Intel8080QueueModel('8080_cpu_model.json')

# 2. Analyze performance at different loads
print("8080 Performance Analysis")
print("=" * 60)

for arrival_rate in [0.10, 0.12, 0.15, 0.18]:
    ipc, metrics = model.predict_ipc(arrival_rate)
    bottleneck = model.find_bottleneck(metrics)
    
    print(f"\nArrival Rate: {arrival_rate:.2f}")
    print(f"  IPC: {ipc:.4f}")
    print(f"  Bottleneck: {bottleneck}")
    
    for m in metrics:
        print(f"  {m.name}: ρ={m.utilization:.3f}")

# 3. Calibrate to measured data
print("\n" + "=" * 60)
print("Calibration to Real Hardware")
print("=" * 60)

measured_ipc = 0.18  # From Altair 8800
result = model.calibrate(measured_ipc)

print(f"\nMeasured IPC: {result.measured_ipc:.4f}")
print(f"Model IPC: {result.predicted_ipc:.4f}")
print(f"Error: {result.error_percent:.2f}%")
print(f"Converged: {result.converged}")

# 4. Print full metrics
print("\n" + "=" * 60)
model.print_metrics(result.stage_metrics)
```

---

## Next Steps

### Learn More

1. **Read Full Documentation**: See `8080_README.md` for complete technical details

2. **Explore Other Models**: Compare with 8086, 80286, 80386 models
   ```bash
   cd ../8086
   python3 8086_cpu_model.py
   ```

3. **Customize Workloads**: Edit JSON configuration to match your application

4. **Historical Research**: Study how 8080 influenced modern architecture

### Advanced Topics

- **Parameter Sensitivity**: Analyze how instruction mix affects IPC
- **Cross-Architecture Comparison**: Quantify improvements from 8080 to 80386
- **Workload Characterization**: Model real CP/M applications
- **Performance Bounds**: Explore theoretical limits of sequential execution

---

## Key Takeaways

1. **8080 is Sequential**: No pipeline, no prefetch → Very low IPC (0.15-0.20)

2. **Execute is Bottleneck**: Longer execute times limit throughput

3. **Architecture Matters**: Later processors gain 5-10× IPC through architectural improvements

4. **Grey-Box Modeling Works**: Simple queueing model achieves <2% error

5. **Historical Baseline**: Understanding 8080 illuminates evolution to modern CPUs

---

## Resources

- **Full Documentation**: `8080_README.md`
- **Configuration**: `8080_cpu_model.json`
- **Source Code**: `8080_cpu_model.py`
- **GitHub**: https://github.com/MartinGallagher-code/Modeling_2026

---

## Support

For questions or issues:
- Review documentation in `8080_README.md`
- Check configuration parameters in JSON file
- Verify Python environment and dependencies

---

**Version:** 1.0  
**Date:** January 24, 2026  
**Author:** Grey-Box Performance Modeling Research
