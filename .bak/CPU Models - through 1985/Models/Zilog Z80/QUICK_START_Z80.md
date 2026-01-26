# Zilog Z80 CPU Model - Quick Start Guide

## Overview

This guide provides a rapid introduction to the Zilog Z80 queueing model.

**Target Audience:** Researchers studying microprocessor evolution  
**Prerequisites:** Python 3.6+, NumPy  
**Time Required:** 10 minutes

---

## Quick Facts: Zilog Z80

| Specification | Value |
|---------------|-------|
| Year | 1976 |
| Word Size | 8 bits |
| Clock Speed | 4 MHz (typical) |
| Pipeline | None (sequential) |
| Registers | Main set + Alternate set + IX, IY |
| Typical IPC | 0.07-0.09 |
| vs 8080 | ~2× faster (clock + optimizations) |

---

## Installation

```bash
# Prerequisites
python3 --version  # 3.6+ required
pip3 install numpy

# Get files
cd Modeling_2026/Z80_model
python3 z80_cpu_model.py  # Test it works
```

---

## Basic Usage

### Predict IPC

```python
from z80_cpu_model import ZilogZ80QueueModel

model = ZilogZ80QueueModel('z80_cpu_model.json')
ipc, metrics = model.predict_ipc(arrival_rate=0.12)

print(f"Predicted IPC: {ipc:.4f}")
# Output: Predicted IPC: 0.0683
```

### Compare with 8080

```python
comparison = model.compare_with_8080()

print(f"Z80 IPC: {comparison['z80_ipc']:.4f}")
print(f"8080 IPC: {comparison['i8080_ipc']:.4f}")
print(f"Speedup: {comparison['ipc_speedup']:.2f}×")
```

### Calibrate Model

```python
measured_ipc = 0.07  # From real hardware
result = model.calibrate(measured_ipc)

print(f"Error: {result.error_percent:.2f}%")
print(f"Converged: {result.converged}")
```

---

## Key Differences from 8080

**Architectural:**
- ✓ Alternate register set (A', BC', DE', HL')
- ✓ Index registers (IX, IY)
- ✓ Enhanced instructions (BIT, LDIR, JR)
- ✓ Built-in DRAM refresh

**Performance:**
- ✓ Faster instruction timings (4 vs 5 cycles)
- ✓ Higher clock speeds (4 MHz vs 2 MHz)
- ✓ Result: ~2× overall speedup

---

## Common Use Cases

### Historical Analysis

```python
# See Z80 improvements over 8080
comparison = model.compare_with_8080()

print(f"Service time improvement: {comparison['service_time_improvement']:.2f}×")
print(f"With clock advantage (2×): ~{comparison['ipc_speedup'] * 2:.1f}× total")
```

### Workload Characterization

```python
# Test different arrival rates
for rate in [0.08, 0.10, 0.12]:
    ipc, _ = model.predict_ipc(rate)
    print(f"λ={rate:.2f} → IPC={ipc:.4f}")
```

---

## Understanding Output

**Service Time:**
- Z80 Fetch: ~5.57 cycles (includes 2% DRAM refresh)
- Z80 Execute: ~7.03 cycles (optimized vs 8080's 7.3)
- Total: ~12.60 cycles

**Maximum IPC:**
- Theoretical: 1/12.60 ≈ 0.079
- Practical: 0.06-0.07 (due to queueing)

---

## Next Steps

- **Full docs**: See `Z80_README.md`
- **Compare models**: Try 8080, 8086, 80286 models
- **Customize**: Edit JSON for different workloads

---

**Version:** 1.0  
**Date:** January 24, 2026
