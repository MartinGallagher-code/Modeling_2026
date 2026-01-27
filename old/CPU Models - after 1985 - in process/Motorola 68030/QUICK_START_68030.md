# Motorola 68030 - Quick Start Guide

## The Classic Mac CPU (1987)

On-chip MMU + data cache. Powered Mac SE/30, IIci, NeXT.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1987 |
| Transistors | 273,000 |
| Clock | 16-50 MHz |
| I-Cache | 256 bytes |
| D-Cache | **256 bytes** (new!) |
| MMU | **On-chip** (new!) |
| IPC | ~0.80 |

---

## vs 68020

| Feature | 68020 | 68030 |
|---------|-------|-------|
| D-Cache | None | 256B |
| MMU | External 68851 | On-chip |
| Performance | Baseline | +20-30% |

---

## Famous Systems

- **Mac SE/30** (greatest compact Mac)
- **Mac IIci** (popular workstation)
- **NeXT Computer** (Steve Jobs)
- **Amiga 3000** (multimedia)

---

## Basic Usage

```python
from motorola_68030_model import Motorola68030QueueModel

model = Motorola68030QueueModel('motorola_68030_model.json')
ipc, _ = model.predict_ipc(0.50)
print(f"IPC: {ipc:.4f}")

comp = model.compare_68020()
print(f"Improvements: {comp['improvements']}")
```

---

**Version:** 1.0
