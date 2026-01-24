# Intel 8048 - Quick Start Guide

## First Successful Microcontroller (1976)

CPU + ROM + RAM + I/O on one chip. In every IBM PC keyboard!

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1976 |
| On-chip ROM | **1 KB** |
| On-chip RAM | **64 bytes** |
| I/O Lines | **27** |
| Clock | 6 MHz (÷15) |
| Effective | ~400 kHz |

---

## Why It Matters

Before 8048: 5-10 chips for simple computer
After 8048: ONE CHIP

**Every IBM PC keyboard had an 8048!**

---

## Basic Usage

```python
from intel_8048_model import Intel8048QueueModel

model = Intel8048QueueModel('intel_8048_model.json')
ipc, _ = model.predict_ipc(0.06)
print(f"IPC: {ipc:.4f}")
```

---

## Legacy

8048 → 8051 → Most successful MCU architecture ever

---

**Version:** 1.0
