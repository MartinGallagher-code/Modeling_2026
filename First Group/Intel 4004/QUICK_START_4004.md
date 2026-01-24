# Intel 4004 - Quick Start Guide

## THE FIRST MICROPROCESSOR (November 15, 1971)

2,300 transistors. 740 kHz. 4 bits. Changed the world.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1971 |
| Bits | **4** |
| Transistors | **2,300** |
| Clock | 740 kHz |
| IPC | ~0.09 |
| Die Size | 12 mm² |
| Price | $200 |

---

## Why It Matters

**Before 4004:** CPUs filled circuit boards
**After 4004:** Complete CPU on one chip

This enabled:
- Personal computers
- Smartphones
- Everything with a processor

---

## Basic Usage

```python
from intel_4004_model import Intel4004QueueModel

model = Intel4004QueueModel('intel_4004_model.json')
ipc, _ = model.predict_ipc(0.08)
print(f"IPC: {ipc:.4f}")

# See how far we've come
comp = model.historical_comparison()
print(f"Improvement: {comp['improvement']['performance']:,.0f}× faster")
```

---

## The Designers

- **Federico Faggin** - Lead designer
- **Ted Hoff** - Architecture
- **Stan Mazor** - Software
- **Masatoshi Shima** - Logic design

---

**"The 4004 is the most historically significant processor ever made."**

---

**Version:** 1.0
