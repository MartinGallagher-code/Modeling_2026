# CDP1805 - Quick Start Guide

## Enhanced Space Processor (1984)

Improved 1802. Flew to Jupiter, Saturn, and Pluto!

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1984 |
| Clock | 4-5 MHz (2× 1802) |
| Timer | **On-chip** |
| Registers | 16 × 16-bit |
| Rad-hard | Yes |

---

## Space Missions

- **Galileo** → Jupiter
- **Cassini** → Saturn  
- **New Horizons** → Pluto (still operating!)

---

## Basic Usage

```python
from cdp1805_model import CDP1805QueueModel
model = CDP1805QueueModel('cdp1805_model.json')
ipc, _ = model.predict_ipc(0.05)
print(f"IPC: {ipc:.4f}")
```

---

**Still working 8 billion km from Earth!**

---

**Version:** 1.0
