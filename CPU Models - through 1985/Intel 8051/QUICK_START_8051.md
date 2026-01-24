# Intel 8051 - Quick Start Guide

## Most Successful MCU Ever (1980)

Billions shipped. 50+ manufacturers. Still produced after 45 years!

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1980 |
| On-chip ROM | **4 KB** |
| On-chip RAM | **128 bytes** |
| I/O Lines | **32** |
| Timers | **2 × 16-bit** |
| Serial | **UART** |
| Speed | 1 MIPS |

---

## Why It Won

1. **Boolean processor** - Bit-addressable memory
2. **Complete** - All peripherals on-chip
3. **Licensed** - 50+ manufacturers
4. **Ecosystem** - Huge tool/code base

---

## Basic Usage

```python
from intel_8051_model import Intel8051QueueModel

model = Intel8051QueueModel('intel_8051_model.json')
ipc, _ = model.predict_ipc(0.07)
print(f"IPC: {ipc:.4f}")

impact = model.show_8051_impact()
print(f"Units: {impact['units_shipped']}")
```

---

## Impact

**Most successful MCU architecture in computing history.**

---

**Version:** 1.0
