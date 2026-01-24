# Motorola 6800 - Quick Start Guide

## The First Motorola Microprocessor

The 6800 (1974) was Motorola's answer to Intel's 8080. Cleaner design, but lost the market war.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1974 |
| Bits | 8 |
| Clock | 1 MHz |
| Accumulators | 2 (A, B) |
| IPC | ~0.07 |
| Endian | Big |

---

## Basic Usage

```python
from motorola_6800_model import Motorola6800QueueModel

model = Motorola6800QueueModel('motorola_6800_model.json')
ipc, metrics = model.predict_ipc(0.08)
print(f"IPC: {ipc:.4f}")

result = model.calibrate(0.07)
print(f"Error: {result['error_percent']:.2f}%")
```

---

## Key Insight

**6800 vs 8080:**
- 6800: Cleaner architecture, dual accumulators
- 8080: Faster clock, better ecosystem
- Winner: 8080 (market reality)

**Legacy:** Chuck Peddle left Motorola → Created 6502 → Changed computing

---

**Version:** 1.0
