# Intel 8085 CPU Model - Quick Start Guide

## Overview

This guide provides a rapid introduction to the Intel 8085 queueing model.

**Target Audience:** Researchers studying microprocessor evolution  
**Prerequisites:** Python 3.6+, NumPy  
**Time Required:** 10 minutes

---

## Quick Facts: Intel 8085

| Specification | Value |
|---------------|-------|
| Year | 1976 |
| Word Size | 8 bits |
| Clock Speed | 3 MHz (typical) |
| Pipeline | None (sequential) |
| Power Supply | Single +5V |
| Typical IPC | 0.07 (same as 8080) |
| vs 8080 | ~1.5× faster (clock only) |

---

## Installation

```bash
# Prerequisites
python3 --version  # 3.6+ required
pip3 install numpy

# Get files
cd Modeling_2026/8085_model
python3 intel_8085_model.py  # Test it works
```

---

## Basic Usage

### Predict IPC

```python
from intel_8085_model import Intel8085QueueModel

model = Intel8085QueueModel('intel_8085_model.json')
ipc, metrics = model.predict_ipc(arrival_rate=0.12)

print(f"Predicted IPC: {ipc:.4f}")
# Output: Predicted IPC: 0.0674
```

### Compare with 8080

```python
comparison = model.compare_with_8080()

print(f"8085 IPC: {comparison['i8085_ipc']:.4f}")
print(f"8080 IPC: {comparison['i8080_ipc']:.4f}")
print(f"Architecture advantage: {comparison['ipc_ratio']:.2f}×")
print(f"Clock advantage: {comparison['clock_advantage']:.2f}×")
print(f"Overall speedup: {comparison['overall_speedup']:.2f}×")

# Shows: Architecture ~1.0× (no improvement)
#        Clock 1.5× (technology improvement)
#        Overall 1.5× (technology only)
```

### Calibrate Model

```python
measured_ipc = 0.070  # From real hardware
result = model.calibrate(measured_ipc)

print(f"Error: {result.error_percent:.2f}%")
print(f"Converged: {result.converged}")
```

---

## Key Differences from 8080

**System Integration:**
- ✓ On-chip clock generator
- ✓ Single +5V supply (vs 8080's 4 voltages)
- ✓ Multiplexed bus (fewer pins)
- ✓ Built-in serial I/O
- ✓ 5 interrupts (vs 8080's 1)

**Performance:**
- ✗ NO improvement in IPC (same 0.07)
- ✓ Higher typical clock (3 MHz vs 2 MHz)
- ✓ Result: 1.5× faster overall

---

## Understanding the Model

**Service Time:**
- 8085 Fetch: ~5.25 cycles (same as 8080)
- 8085 Execute: ~7.05 cycles (same as 8080)
- Total: ~12.30 cycles

**Maximum IPC:**
- Theoretical: 1/12.30 ≈ 0.081
- Practical: 0.06-0.07 (due to queueing)

**Bottleneck:**
- Execute stage (same as 8080)
- Sequential execution limitation

---

## Common Use Cases

### Historical Analysis

```python
# See 8085 advantages over 8080
comparison = model.compare_with_8080()

print("8085 advantages:")
print(f"  Integration: Easier design")
print(f"  Power: Single voltage")
print(f"  Performance: {comparison['overall_speedup']:.2f}× (clock only)")
```

### Workload Characterization

```python
# Test different arrival rates
for rate in [0.08, 0.10, 0.12]:
    ipc, _ = model.predict_ipc(rate)
    print(f"λ={rate:.2f} → IPC={ipc:.4f}")
```

---

## Key Insight

**The 8085 proves that:**
- Market success ≠ Performance improvements
- Integration matters as much as speed
- "Good enough" + easy to use = long-term success
- Still manufactured 50 years later!

---

## Next Steps

- **Full docs**: See `INTEL_8085_README.md`
- **Compare models**: Try 8080, Z80, 8086 models
- **Understand evolution**: See how 8085 fits in timeline

---

**Version:** 1.0  
**Date:** January 24, 2026
