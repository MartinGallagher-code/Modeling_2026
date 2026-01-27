# Intel 80486 - Quick Start Guide

## RISC-like x86 (1989)

First x86 with pipeline, on-chip cache, and FPU. 2× faster than 386.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1989 |
| Transistors | **1,200,000** |
| Pipeline | **5 stages** (first x86!) |
| Cache | **8KB unified** (first x86!) |
| FPU | **On-chip** (first x86!) |
| IPC | ~0.85 |
| vs 386 | **2× faster** at same clock |

---

## Key Innovations

1. **First x86 pipeline** - Multiple instructions in flight
2. **On-chip cache** - 93% hit rate
3. **Integrated FPU** - 8-10× faster than 80387
4. **Clock doubling** - DX2/DX4 variants

---

## Variants

| Model | Clock | Notes |
|-------|-------|-------|
| 486DX-33 | 33 MHz | Common |
| 486DX2-66 | 66 MHz | Most popular |
| 486DX4-100 | 100 MHz | Fastest |
| 486SX | Various | No FPU |

---

## Basic Usage

```python
from intel_80486_model import Intel80486QueueModel

model = Intel80486QueueModel('intel_80486_model.json')
ipc, _ = model.predict_ipc(0.55)
print(f"IPC: {ipc:.4f}")

# Clock variants
variants = model.clock_variants()
for name, specs in variants.items():
    print(f"{name}: {specs['mips']:.1f} MIPS")
```

---

**The 486 saved x86 by proving CISC could be fast.**

---

**Version:** 1.0
