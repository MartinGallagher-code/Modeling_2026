# Motorola 68008 CPU Queueing Model

## 8-Bit Bus 68000 (1982)

The Motorola 68008 is to the 68000 what the Intel 8088 is to the 8086: **same internal architecture, smaller external bus** for lower-cost systems.

---

## Executive Summary

| Spec | 68000 | 68008 |
|------|-------|-------|
| Internal | 32-bit | 32-bit |
| **Data Bus** | 16-bit | **8-bit** |
| Address Space | 16 MB | **1 MB** |
| Pins | 64 | **48** |
| Performance | 1.0× | **~0.4×** |

---

## Why 8-Bit Bus?

```
68000 word read:  ████████████████  (1 bus cycle)
68008 word read:  ████████ ████████  (2 bus cycles)

68000 long read:  ████████████████ ████████████████  (2 bus cycles)
68008 long read:  ████████ ████████ ████████ ████████  (4 bus cycles)
```

The 8-bit bus requires **multiple transfers** for word/long operations, reducing performance but also reducing cost.

---

## Cost Benefits

| Factor | 68000 | 68008 |
|--------|-------|-------|
| Package | 64-pin | 48-pin |
| PCB layers | More | Fewer |
| Memory | 16-bit wide | 8-bit wide |
| Total system cost | Higher | **Lower** |

For low-cost systems, the 68008 made 32-bit computing affordable.

---

## The Sinclair QL

The most famous 68008 system was the **Sinclair QL** (1984):

- Quantum Leap - ambitious name
- 68008 at 7.5 MHz
- 128 KB RAM (expandable)
- Dual Microdrives (unreliable)
- Innovative but troubled launch
- Commercial failure, but cult following

Linus Torvalds learned programming on a QL!

---

## Performance Analysis

### Bus Penalty

| Operation | 68000 | 68008 | Penalty |
|-----------|-------|-------|---------|
| Byte read | 8 cyc | 8 cyc | None |
| Word read | 8 cyc | 16 cyc | **2×** |
| Long read | 16 cyc | 32 cyc | **2×** |

Average penalty: ~60% slower for typical code.

---

## Usage

```python
from motorola_68008_model import Motorola68008QueueModel

model = Motorola68008QueueModel('motorola_68008_model.json')
ipc, _ = model.predict_ipc(0.07)
print(f"IPC: {ipc:.4f}")
```

---

**Version:** 1.0 | **Date:** January 25, 2026

*"68000 power at 8-bit cost."*
