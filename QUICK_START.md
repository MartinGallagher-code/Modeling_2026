# Quick Start Guide - Simple CPU Queueing Model

**Version:** 1.0  
**Date:** January 22, 2026

---

## Installation and Setup

### Prerequisites
```bash
# Python 3.8+
python3 --version

# Required packages
pip3 install numpy
```

### Files Required
1. `simple_cpu_model.json` - Model configuration
2. `simple_cpu_model.py` - Python implementation
3. `simple_cpu_queueing_model.md` - Full documentation

---

## Quick Start (5 minutes)

### Step 1: Run the Example

```bash
python3 simple_cpu_model.py
```

**Expected Output:**
```
Simple CPU Queueing Model - Example Run

1. BASELINE PERFORMANCE
--------------------------------------------------------------------------------
================================================================================
SIMPLE CPU QUEUEING MODEL - PERFORMANCE REPORT
================================================================================

Overall Performance:
  IPC:        0.7234
  CPI:        1.3824
  Throughput: 1.158 GIPS (billion instructions/sec)
  Bottleneck: Memory Access (MEM) (ρ = 0.800)

Stage-by-Stage Breakdown:
  Stage                Service (cyc)   Utilization     Queue Len       CPI       
  -------------------- --------------- --------------- --------------- ----------
  Instruction Fetch      1.99 cyc       0.115           0.130           0.231
  Decode (ID)            1.00 cyc       0.058           0.061           0.062
  Execute (EX)           1.17 cyc       0.068           0.073           0.073
  Memory Access (MEM)   13.80 cyc       0.800           4.000           1.000
  Write Back (WB)        1.00 cyc       0.058           0.061           0.062
...
```

### Step 2: Understand the Output

**Key Metrics:**
- **IPC (Instructions Per Cycle)**: Higher is better (target: 0.5-1.0 for simple pipeline)
- **Bottleneck**: Stage with highest utilization (ρ closest to 1.0)
- **CPI Contribution**: Which stages add the most latency

**Interpretation:**
- If Memory Access (MEM) is bottleneck → Memory-bound workload
- If Execute (EX) is bottleneck → Compute-bound workload
- High utilization (ρ > 0.9) → Stage is saturated, system instability

---

## Basic Usage Examples

### Example 1: Compute Baseline Performance

```python
from simple_cpu_model import SimpleCPUQueueModel

# Load model
model = SimpleCPUQueueModel('simple_cpu_model.json')

# Compute performance at 80% bottleneck utilization
result = model.compute_pipeline_performance()

print(f"IPC: {result.ipc:.3f}")
print(f"Bottleneck: {result.bottleneck_stage}")
```

### Example 2: Modify Parameters and Re-evaluate

```python
# Reduce cache miss rates (better locality)
model.update_parameters({
    'p_icache_miss': 0.005,  # 0.5% miss rate
    'p_dcache_miss': 0.010   # 1.0% miss rate
})

result = model.compute_pipeline_performance()
print(f"Improved IPC: {result.ipc:.3f}")
```

### Example 3: Analyze Sensitivity

```python
# Which parameters matter most?
sensitivities = model.full_sensitivity_analysis()

for param, sens in sensitivities.items():
    print(f"{param}: Elasticity = {sens['elasticity']:+.4f}")
```

**Interpretation:**
- **Elasticity > 0**: Increasing parameter increases IPC (positive effect)
- **Elasticity < 0**: Increasing parameter decreases IPC (negative effect)
- **|Elasticity| > 1**: Parameter has strong influence on IPC

### Example 4: Calibrate to Real System

```python
# Measured data from real system (perf counters)
measured_data = {
    'icache_miss_rate': 0.015,   # From perf stat
    'dcache_miss_rate': 0.025,   # From perf stat
    'alu_fraction': 0.70,         # From instruction profiling
    'mul_fraction': 0.05,
    'div_fraction': 0.01,
    'mem_fraction': 0.30
}
measured_ipc = 0.78  # From perf stat (instructions / cycles)

# Calibrate model
calibration = model.calibrate(
    measured_ipc=measured_ipc,
    measured_counters=measured_data,
    tolerance_percent=2.0,  # Target 2% error
    verbose=True
)

print(f"Error: {calibration.error_percent:.2f}%")
print(f"Converged: {calibration.converged}")
```

---

## Collecting Real System Data

### Using Linux `perf` (Recommended)

```bash
# Run your benchmark with perf
perf stat -e cycles,instructions,L1-icache-misses,L1-dcache-misses,branches,branch-misses \
  ./your_benchmark

# Example output:
#   10,000,000,000  instructions
#   15,000,000,000  cycles
#   100,000,000     L1-icache-misses
#   250,000,000     L1-dcache-misses
#
# Calculate:
#   IPC = 10B / 15B = 0.667
#   I-cache miss rate = 100M / 10B = 0.01 (1%)
#   D-cache miss rate = 250M / (0.3 * 10B) = 0.083 (8.3%)
#                       (assuming 30% are memory ops)
```

### Using Intel VTune

```bash
vtune -collect hotspots -result-dir vtune_results -- ./your_benchmark

# View results
vtune -report hw-events -result-dir vtune_results -format csv \
  -report-output vtune_counters.csv

# Extract: IPC, cache miss rates, instruction mix
```

### Using AMD uProf

```bash
AMDuProfCLI collect --event cpu-cycles,retired-instructions,l1-icache-misses \
  -o uprof_results ./your_benchmark

# Analyze results
AMDuProfCLI report -i uprof_results
```

---

## Parameter Guide

### Known Parameters (From CPU Datasheet)

| Parameter | Typical Value | Source |
|-----------|---------------|--------|
| `S_ID` (decode) | 1 cycle | Datasheet |
| `S_WB` (write-back) | 1 cycle | Datasheet |
| `clock_freq_ghz` | 2.0 GHz | Specification |
| `l1_cache_kb` | 32 KB | Datasheet |

### Unknown Parameters (Calibrate from Measurements)

| Parameter | Typical Range | Calibration Source |
|-----------|---------------|--------------------|
| `p_icache_miss` | 0.001 - 0.05 | `perf stat` L1-icache-misses |
| `p_dcache_miss` | 0.01 - 0.10 | `perf stat` L1-dcache-misses |
| `L_miss` | 50-500 cycles | Memory latency benchmark |
| `p_alu` | 0.50 - 0.80 | Instruction profiling |
| `p_mul` | 0.01 - 0.10 | Instruction profiling |
| `p_div` | 0.001 - 0.05 | Instruction profiling |
| `p_mem` | 0.20 - 0.40 | Instruction profiling |

### How to Extract Instruction Mix

**Using `perf record` + `perf annotate`:**
```bash
# Record instruction samples
perf record -e instructions:u ./benchmark

# Analyze instruction types
perf annotate --stdio | grep -E "add|sub|mul|div|load|store"

# Count manually:
# ALU ops: add, sub, and, or, xor, shift
# Multiply: mul, imul
# Divide: div, idiv
# Memory: load, store, mov (memory variants)
```

**Using `objdump` (static analysis):**
```bash
objdump -d ./benchmark | grep -E "add|mul|div|mov" | wc -l
```

---

## Validation Checklist

### ✅ Before Calibration

- [ ] CPU frequency is known (check `/proc/cpuinfo` or `lscpu`)
- [ ] Performance counters are available (`perf list` shows events)
- [ ] Benchmark runs successfully
- [ ] You have root access (for `perf stat`)

### ✅ During Calibration

- [ ] Measured IPC is reasonable (0.3 - 2.0 for typical CPUs)
- [ ] Cache miss rates are < 50% (otherwise extreme memory bound)
- [ ] Instruction mix adds to 100% (p_alu + p_mul + p_div + p_other = 1)
- [ ] Model converges within 10 iterations
- [ ] Final error < 5% (ideally < 2%)

### ✅ After Calibration

- [ ] Calibrated `L_miss` is within bounds (50-500 cycles)
- [ ] Bottleneck stage makes sense for workload:
  - Memory-bound workload → MEM stage bottleneck
  - Compute-bound workload → EX stage bottleneck
- [ ] IPC prediction matches measurement within tolerance
- [ ] Sensitivity analysis shows expected trends:
  - Higher cache miss rates → Lower IPC ✓
  - More divide ops → Lower IPC ✓
  - Longer memory latency → Lower IPC ✓

---

## Troubleshooting

### Issue: Model predicts unstable stage (ρ >= 1.0)

**Cause:** Arrival rate too high or service time too long

**Solution:**
```python
# Reduce arrival rate
result = model.compute_pipeline_performance(arrival_rate=1e9)  # 1 GIPS

# Or reduce service times by improving cache parameters
model.update_parameters({'p_dcache_miss': 0.01})  # Lower miss rate
```

### Issue: Calibration doesn't converge

**Cause:** Model structure doesn't capture real system behavior

**Solutions:**
1. Check if measurements are correct (re-run `perf stat`)
2. Verify instruction mix adds to 100%
3. Increase max iterations
4. Reduce learning rate:
```python
model.calibration_config['learning_rate'] = 0.05  # Smaller steps
```

### Issue: Predicted IPC much higher than measured

**Possible Causes:**
- Missing pipeline stalls (branch mispredictions, structural hazards)
- Memory bandwidth limits not modeled
- NUMA effects (multi-socket system)
- Thermal throttling

**Diagnosis:**
```bash
# Check actual CPU frequency during benchmark
perf stat -e cpu-cycles,task-clock ./benchmark

# If task-clock < expected, CPU is throttled
# If cycles/second < clock_freq, CPU is not running at full speed
```

### Issue: Predicted IPC much lower than measured

**Possible Causes:**
- Over-estimated cache miss rates
- Over-estimated memory latency
- Out-of-order execution (model assumes in-order)

**Solution:**
```python
# Manually reduce latency parameter
model.params['L_miss'] = 80  # Lower latency
result = model.compute_pipeline_performance()
```

---

## Advanced Usage

### Scenario 1: Compare Different Memory Configurations

```python
# Baseline: Standard memory
model_baseline = SimpleCPUQueueModel('simple_cpu_model.json')
result_baseline = model_baseline.compute_pipeline_performance()

# Configuration 1: Faster memory (lower latency)
model_fast_mem = SimpleCPUQueueModel('simple_cpu_model.json')
model_fast_mem.update_parameters({'L_miss': 50})  # 50 cycles
result_fast_mem = model_fast_mem.compute_pipeline_performance()

# Configuration 2: Better cache (lower miss rate)
model_better_cache = SimpleCPUQueueModel('simple_cpu_model.json')
model_better_cache.update_parameters({
    'p_icache_miss': 0.005,
    'p_dcache_miss': 0.010
})
result_better_cache = model_better_cache.compute_pipeline_performance()

# Compare
print(f"Baseline IPC:      {result_baseline.ipc:.3f}")
print(f"Fast Memory IPC:   {result_fast_mem.ipc:.3f} (+{(result_fast_mem.ipc/result_baseline.ipc-1)*100:.1f}%)")
print(f"Better Cache IPC:  {result_better_cache.ipc:.3f} (+{(result_better_cache.ipc/result_baseline.ipc-1)*100:.1f}%)")
```

### Scenario 2: Workload Characterization

```python
# Compute-bound workload (low memory %)
model.update_parameters({
    'p_mem': 0.10,          # Only 10% memory ops
    'p_alu': 0.75,          # 75% ALU
    'p_mul': 0.10,          # 10% multiply
    'p_dcache_miss': 0.01   # Low miss rate
})
result_compute = model.compute_pipeline_performance()

# Memory-bound workload (high memory %)
model.update_parameters({
    'p_mem': 0.50,          # 50% memory ops
    'p_alu': 0.40,          # 40% ALU
    'p_mul': 0.05,          # 5% multiply
    'p_dcache_miss': 0.10   # High miss rate
})
result_memory = model.compute_pipeline_performance()

print(f"Compute-bound IPC: {result_compute.ipc:.3f}")
print(f"Memory-bound IPC:  {result_memory.ipc:.3f}")
```

### Scenario 3: Export Results for Further Analysis

```python
# Generate results for multiple configurations
configs = {
    'baseline': {'L_miss': 100, 'p_dcache_miss': 0.03},
    'fast_mem': {'L_miss': 50, 'p_dcache_miss': 0.03},
    'better_cache': {'L_miss': 100, 'p_dcache_miss': 0.01}
}

results = {}
for name, params in configs.items():
    model = SimpleCPUQueueModel('simple_cpu_model.json')
    model.update_parameters(params)
    result = model.compute_pipeline_performance()
    results[name] = result.ipc
    
    # Export detailed results
    model.export_results(f'results_{name}.json', result)

# Create summary
import json
with open('comparison_summary.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

## Next Steps

1. **✅ Start simple**: Run the example and understand baseline performance
2. **📊 Collect data**: Use `perf stat` to measure your real system
3. **🎯 Calibrate**: Match model to measurements
4. **🔬 Analyze**: Use sensitivity analysis to identify optimization targets
5. **📈 Extend**: Move to more complex CPU models (see documentation)

---

## References

- Full documentation: `simple_cpu_queueing_model.md`
- Model configuration: `simple_cpu_model.json`
- Implementation: `simple_cpu_model.py`

---

**Version:** 1.0  
**Last Updated:** January 22, 2026  
**Contact:** Grey-Box Performance Modeling Research
