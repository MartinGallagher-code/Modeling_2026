# Fairchild F8 - Quick Start Guide

## First Microcontroller Architecture

The F8 (1974) pioneered on-chip RAM and powered the first cartridge game console.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1974 |
| On-Chip RAM | **64 bytes** (first!) |
| Design | Multi-chip (2+ chips) |
| Clock | 2 MHz |
| IPC | ~0.06 |
| Famous For | Channel F console |

---

## Key Innovation

**On-Chip Scratchpad RAM:**
- 64 bytes on CPU die
- 2× faster than external memory
- Precursor to modern MCU architecture

---

## Channel F Console

- First ROM cartridge system (1976)
- Two F8 chips
- 26 game cartridges released
- Lost to Atari 2600 (better marketing)

---

## Basic Usage

```python
from fairchild_f8_model import FairchildF8QueueModel

model = FairchildF8QueueModel('fairchild_f8_model.json')
ipc, _ = model.predict_ipc(0.05)
print(f"IPC: {ipc:.4f}")
```

---

## The Lesson

Good idea (on-chip RAM) + bad execution (multi-chip) = limited success

The concept lived on in every modern microcontroller.

---

**Version:** 1.0
