# Motorola 68040 - Quick Start Guide

## Most Powerful 68k Ever (1990)

On-chip FPU, 6-stage pipeline, 4KB caches. Powered Mac Quadra.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1990 |
| Transistors | **1,200,000** |
| Pipeline | **6 stages** |
| I-Cache | **4KB** |
| D-Cache | **4KB** |
| FPU | **On-chip** |
| IPC | ~0.90 |

---

## vs 68030

| Feature | 68030 | 68040 |
|---------|-------|-------|
| Transistors | 273K | 1.2M |
| Cache | 512B | 8KB |
| Pipeline | 3-stage | 6-stage |
| FPU | External | On-chip |
| Performance | Baseline | **2-3×** |

---

## Famous Systems

- **Mac Quadra 800/840AV**
- **Amiga 4000**
- **NeXTstation Turbo**

---

## Basic Usage

```python
from motorola_68040_model import Motorola68040QueueModel

model = Motorola68040QueueModel('motorola_68040_model.json')
ipc, _ = model.predict_ipc(0.55)
print(f"IPC: {ipc:.4f}")  # Near 0.9!

comp = model.compare_68030()
print(f"vs 68030: {comp['improvements']['performance']}")
```

---

## End of an Era

The 68040 was the last major 68k before PowerPC.

---

**Version:** 1.0
