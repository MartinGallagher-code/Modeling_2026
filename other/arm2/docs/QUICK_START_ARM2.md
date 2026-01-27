# ARM2 - Quick Start Guide

## First Production ARM (1986)

Powered the Acorn Archimedes - fastest personal computer of its time.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1986 |
| Transistors | **30,000** |
| Clock | 8-12 MHz |
| Pipeline | 3 stages |
| IPC | ~0.70 |
| MIPS | ~4.5 @ 8 MHz |

---

## vs ARM1

| Feature | ARM1 | ARM2 |
|---------|------|------|
| Multiplier | 16 cycles | **8 cycles** |
| Coprocessor | No | **Yes** |
| SWP instruction | No | **Yes** |
| Status | Dev | **Production** |

---

## 1987 Performance

| System | CPU | MIPS |
|--------|-----|------|
| **Archimedes** | **ARM2** | **~4.5** |
| Amiga 500 | 68000 | ~0.7 |
| Atari ST | 68000 | ~0.8 |

**ARM2 was 5-6× faster than 68000!**

---

## Basic Usage

```python
from arm2_model import ARM2QueueModel

model = ARM2QueueModel('arm2_model.json')
ipc, _ = model.predict_ipc(0.50)
print(f"IPC: {ipc:.4f}")

comp = model.compare_1987_competitors()
print(comp['conclusion'])
```

---

**Version:** 1.0
