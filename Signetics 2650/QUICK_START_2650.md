# Signetics 2650 - Quick Start Guide

## The 32KB Limitation

The 2650 (1975) was a capable processor doomed by one decision: only 15 address bits (32KB max memory).

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1975 |
| Address Bits | **15** (vs 16 standard) |
| Max Memory | **32KB** (vs 64KB competitors) |
| Clock | 1.25 MHz |
| IPC | ~0.06 |

---

## The Fatal Flaw

```
8080, 6502, 6800: 16-bit address = 64KB
2650:             15-bit address = 32KB

Result: Couldn't grow with applications
```

---

## Systems

- Interton VC 4000 console family (Europe)
- Emerson Arcadia 2001
- Various European hobby computers

---

## Basic Usage

```python
from signetics_2650_model import Signetics2650QueueModel

model = Signetics2650QueueModel('signetics_2650_model.json')
ipc, _ = model.predict_ipc(0.05)
print(f"IPC: {ipc:.4f}")

# The fatal flaw
print(f"Max memory: {model.config['memory_system']['max_memory_kb']}KB")
# 32KB - not enough!
```

---

## The Lesson

**Don't artificially limit address space.**

The 2650 saved a few pins but lost the market.

---

**Version:** 1.0
