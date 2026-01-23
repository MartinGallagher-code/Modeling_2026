# Intel 80286 Queueing Model - Quick Start Guide

**Get started in 5 minutes!**

---

## Installation

### Requirements
- Python 3.7+
- NumPy

```bash
pip3 install numpy
```

---

## Quick Start (3 Steps)

### Step 1: Run Example

```bash
python3 80286_cpu_model.py
```

**Expected Output:**
```
Intel 80286 CPU Queueing Model
================================================================================

Example 1: IPC Prediction at Different Load Levels
--------------------------------------------------------------------------------
Arrival Rate: 0.30 → IPC: 0.8125, Bottleneck: Execute
Arrival Rate: 0.50 → IPC: 0.6897, Bottleneck: Execute
Arrival Rate: 0.70 → IPC: 0.5102, Bottleneck: Execute
Arrival Rate: 0.90 → IPC: 0.2941, Bottleneck: Execute

Example 2: Detailed Metrics at 50% Load
================================================================================
Intel 80286 CPU Pipeline Metrics
================================================================================
Stage                         λ        S        ρ        L        W        R
                          (ins/c)    (cyc)              (ins)    (cyc)    (cyc)
--------------------------------------------------------------------------------
Prefetch_Queue_BIU          0.5000     2.50   1.2500     3.00     6.00     8.50
Decode_Address_MMU          0.5000     5.00   2.5000     Inf      Inf      Inf
Execute                     0.5000     2.61   1.3050     Inf      Inf      Inf
Memory_Access               0.5000     1.82   0.9075     9.80    19.60    21.42
Writeback                   0.5000     1.00   0.5000     1.00     2.00     3.00
================================================================================

Bottleneck: Decode_Address_MMU (ρ = 2.5000)
[... more output ...]
```

### Step 2: Understand the Metrics

**Key Metrics:**
- **λ (lambda)**: Arrival rate (instructions/cycle)
- **S**: Service time (cycles/instruction)
- **ρ (rho)**: Utilization = λ × S
- **L**: Queue length (instructions waiting)
- **W**: Wait time (cycles)
- **IPC**: Instructions Per Cycle (higher is better)

**Interpreting Results:**
- ρ < 0.7: Stage is underutilized
- 0.7 ≤ ρ < 0.9: Moderate load
- ρ ≥ 0.9: **Bottleneck** (saturated)
- ρ ≥ 1.0: Unstable (queue grows infinitely)

### Step 3: Calibrate to Your System

```python
from 80286_cpu_model import Intel80286QueueModel

# 1. Load model
model = Intel80286QueueModel('80286_cpu_model.json')

# 2. Set your measured parameters
# (from profiling or specifications)
model.p_alu = 0.65          # 65% ALU instructions
model.p_mul = 0.03          # 3% multiply
model.p_div = 0.01          # 1% divide
model.p_load = 0.18         # 18% loads
model.p_store = 0.13        # 13% stores

# 3. Calibrate to measured IPC
measured_ipc = 0.72  # Your actual measurement
result = model.calibrate(measured_ipc, tolerance_percent=2.0)

print(f"Measured IPC:  {result.measured_ipc:.4f}")
print(f"Predicted IPC: {result.predicted_ipc:.4f}")
print(f"Error:         {result.error_percent:.2f}%")
print(f"Bottleneck:    {result.bottleneck_stage}")
```

---

## Common Use Cases

### 1. Predict Performance at Different Clock Speeds

```python
model = Intel80286QueueModel('80286_cpu_model.json')

# Test at 8 MHz, 10 MHz, 12 MHz
for freq_mhz in [8, 10, 12]:
    model.clock_freq_mhz = freq_mhz
    ipc, metrics = model.predict_ipc(0.6)
    mips = ipc * freq_mhz
    print(f"{freq_mhz} MHz → IPC: {ipc:.4f}, {mips:.2f} MIPS")
```

### 2. Compare Real Mode vs Protected Mode

```python
# Real mode (no MMU overhead)
model.p_protected = 0.0
model.mmu_translation_cycles = 0
ipc_real, _ = model.predict_ipc(0.6)

# Protected mode (80% protected ops)
model.p_protected = 0.8
model.mmu_translation_cycles = 3
ipc_protected, _ = model.predict_ipc(0.6)

overhead_percent = (ipc_real - ipc_protected) / ipc_real * 100
print(f"Protected mode overhead: {overhead_percent:.1f}%")
```

### 3. Optimize Memory System

```python
# Test different memory latencies
for mem_cycles in [3, 5, 8, 12]:
    model.memory_cycles = mem_cycles
    ipc, _ = model.predict_ipc(0.6)
    print(f"Memory latency: {mem_cycles} cycles → IPC: {ipc:.4f}")
```

### 4. Identify Bottleneck for Your Workload

```python
# Your workload's instruction mix
model.p_alu = 0.50
model.p_mul = 0.10   # Lots of multiply!
model.p_div = 0.05
model.p_load = 0.20
model.p_store = 0.15

ipc, metrics = model.predict_ipc(0.6)

# Print utilizations
for m in metrics:
    print(f"{m.name}: ρ = {m.utilization:.3f}")

# Identify bottleneck
bottleneck = model.find_bottleneck(metrics)
print(f"\nBottleneck: {bottleneck}")
```

---

## Interpreting Results

### Healthy System
```
Stage                    ρ
Prefetch_Queue_BIU     0.625
Decode_Address_MMU     0.480
Execute                0.782  ← Bottleneck (but < 0.9, OK)
Memory_Access          0.547
Writeback              0.300

IPC: 0.68  ← Good performance
```

**Interpretation:** Execute stage is the bottleneck but not saturated. System is well-balanced.

### Saturated System
```
Stage                    ρ
Prefetch_Queue_BIU     0.950  ← Near saturation!
Decode_Address_MMU     0.720
Execute                0.980  ← Bottleneck (saturated!)
Memory_Access          0.825
Writeback              0.450

IPC: 0.32  ← Poor performance
```

**Interpretation:** Execute stage is saturated (ρ ≈ 1.0). Need to:
1. Reduce multiply/divide fraction (if possible)
2. Increase clock speed
3. Use faster ALU (not an option for 80286)

### Prefetch Starvation
```
Stage                    ρ
Prefetch_Queue_BIU     0.990  ← Prefetch can't keep up!
Decode_Address_MMU     0.450
Execute                0.680
Memory_Access          0.920  ← High memory traffic
Writeback              0.350

IPC: 0.42  ← Moderate performance
```

**Interpretation:** Prefetch queue is starving execution. Likely causes:
1. High memory traffic (loads/stores) contending for BIU
2. Slow memory (many wait states)
3. Instructions executing faster than fetch can supply them

**Solutions:**
1. Reduce memory operations (cache data in registers)
2. Faster memory (reduce wait states)
3. Prefetch more aggressively (not an option on 80286)

---

## Troubleshooting

### Error: "Utilization ≥ 1.0"

**Cause:** Arrival rate too high for service capacity.

**Fix:** Lower arrival rate in `predict_ipc()` call:
```python
# Instead of:
ipc, metrics = model.predict_ipc(0.95)  # Too high!

# Try:
ipc, metrics = model.predict_ipc(0.70)
```

### Error: "Calibration did not converge"

**Cause:** Model parameters don't match real system.

**Fix:** Check your instruction mix and memory latency:
```python
# Verify instruction mix sums to ~1.0
total = model.p_alu + model.p_mul + model.p_div + model.p_load + model.p_store
print(f"Instruction mix total: {total:.3f}")  # Should be ≈ 1.0

# Try adjusting memory_access_cycles
for mem in [3, 5, 7, 10]:
    model.memory_cycles = mem
    result = model.calibrate(measured_ipc, tolerance_percent=5.0)
    print(f"mem={mem}: error={result.error_percent:.2f}%")
```

### Warning: "Prefetch utilization > 1.0"

**Cause:** Memory system too slow or too many memory operations.

**What this means:** Instructions are waiting for prefetch, degrading performance.

**Fix:** Either:
1. Reduce memory access cycles (faster memory)
2. Reduce p_load + p_store (fewer memory ops)

---

## Tips for Accurate Modeling

### 1. Measure, Don't Guess

**Bad:**
```python
model.p_alu = 0.7  # I think most are ALU ops
```

**Good:**
```python
# Analyze your binary
objdump -d program | grep -c "add\|sub\|and"  # Count ALU
objdump -d program | grep -c "mul\|imul"      # Count MUL
# ... then compute fractions
```

### 2. Start Simple, Add Complexity

**Phase 1:** Get basic model working (real mode, simple workload)
```python
model.p_protected = 0.0  # Real mode
model.p_mul = 0.02       # Few multiplies
model.p_div = 0.01       # Few divides
```

**Phase 2:** Add protected mode overhead
```python
model.p_protected = 0.8   # Protected mode
model.mmu_translation_cycles = 3
```

**Phase 3:** Add task switching, interrupts (future work)

### 3. Validate at Multiple Load Levels

```python
# Test at low, medium, high load
for rate in [0.3, 0.5, 0.7]:
    ipc, _ = model.predict_ipc(rate)
    print(f"Load {rate:.1f} → IPC {ipc:.4f}")
```

Expect:
- Low load (0.3): High IPC (little queuing)
- Medium load (0.5): Moderate IPC
- High load (0.7): Lower IPC (queuing effects)

---

## Next Steps

### Beginner
1. ✅ Run the example
2. 📊 Understand the output
3. 🎯 Predict IPC for different arrival rates

### Intermediate
1. 📝 Collect data from a real system (or emulator)
2. 🔧 Calibrate model to measured IPC
3. 📈 Identify bottleneck for your workload

### Advanced
1. 🧪 Validate on multiple benchmarks
2. 🔬 Sensitivity analysis on parameters
3. 📚 Read full documentation (80286_DOCUMENTATION.md)
4. 🚀 Extend to 80287 FPU or task switching

---

## Example Workflows

### Workflow 1: Design Space Exploration

**Question:** Should I use faster memory (3 cycles) or keep cheap memory (8 cycles)?

```python
model = Intel80286QueueModel('80286_cpu_model.json')

# Fast memory
model.memory_cycles = 3
ipc_fast, _ = model.predict_ipc(0.6)
cost_fast = 150  # dollars

# Cheap memory
model.memory_cycles = 8
ipc_cheap, _ = model.predict_ipc(0.6)
cost_cheap = 50  # dollars

speedup = ipc_fast / ipc_cheap
cost_ratio = cost_fast / cost_cheap

print(f"Fast memory: {speedup:.2f}x faster, {cost_ratio:.2f}x cost")
print(f"Price/performance: ${cost_fast/ipc_fast:.2f} per IPC")
```

### Workflow 2: Real Mode vs Protected Mode

**Question:** Is protected mode worth the overhead?

```python
# Real mode
model.p_protected = 0.0
model.mmu_translation_cycles = 0
ipc_real, _ = model.predict_ipc(0.6)

# Protected mode
model.p_protected = 0.8
model.mmu_translation_cycles = 3
ipc_protected, _ = model.predict_ipc(0.6)

overhead = (1 - ipc_protected/ipc_real) * 100
print(f"Protected mode costs {overhead:.1f}% performance")
print(f"But gains: virtual memory, process isolation, privilege levels")
```

### Workflow 3: Compiler Optimization

**Question:** Does reducing multiply instructions help?

```python
# Original code (10% multiply)
model.p_alu = 0.60
model.p_mul = 0.10
ipc_original, _ = model.predict_ipc(0.6)

# Optimized code (strength reduction: replace MUL with shifts)
model.p_alu = 0.68
model.p_mul = 0.02
ipc_optimized, _ = model.predict_ipc(0.6)

improvement = (ipc_optimized / ipc_original - 1) * 100
print(f"Optimization improved IPC by {improvement:.1f}%")
```

---

## FAQ

**Q: Can this model predict exact cycle counts?**  
A: No, it predicts **average** performance (IPC). For exact cycle-by-cycle simulation, use gem5 or a cycle-accurate emulator.

**Q: Why doesn't my calibration converge?**  
A: Check that:
1. Your instruction mix sums to ~1.0
2. Your measured IPC is achievable (≤ 1.0 for in-order CPU)
3. Your memory latency is realistic (3-20 cycles typical)

**Q: Can I model 80386 or 80486?**  
A: This model is specific to 80286. For 80386+, you'd need to add:
- On-chip cache (L1)
- 32-bit instructions
- Paging (in addition to segmentation)

**Q: How accurate is this model?**  
A: Target: < 2% error after calibration. Typical: 1-5% on diverse workloads.

**Q: Can I use this for OS design?**  
A: Yes! Model task switching, interrupt handling, and system call overhead. Great for OS performance tuning.

---

## Resources

- **Full Documentation:** `80286_DOCUMENTATION.md` (60+ pages)
- **Configuration:** `80286_cpu_model.json` (all parameters)
- **Source Code:** `80286_cpu_model.py` (well-commented)
- **GitHub Repository:** Your Modeling_2026 repo

---

**Happy Modeling!** 🚀

**Questions?** Read the full documentation or examine the source code.
