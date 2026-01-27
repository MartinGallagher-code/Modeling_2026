# Zilog Z8000 - Quick Start Guide

## The 16-bit That Failed (1979)

Technically excellent. Commercially dead.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1979 |
| Registers | **16 × 16-bit** (excellent!) |
| Clock | 4-10 MHz |
| IPC | ~0.12 |
| Market | **Failed** |

---

## Why It Lost

1. Too late (1979)
2. No killer platform (no IBM PC, no Mac)
3. Z80 success made Zilog complacent

---

## Basic Usage

```python
from zilog_z8000_model import ZilogZ8000QueueModel
model = ZilogZ8000QueueModel('zilog_z8000_model.json')
ipc, _ = model.predict_ipc(0.10)
print(f"IPC: {ipc:.4f}")
```

---

## The Lesson

**Best technology ≠ market winner.**

---

**Version:** 1.0
