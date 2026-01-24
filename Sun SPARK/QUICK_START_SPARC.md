# SPARC - Quick Start Guide

## Sun's Open RISC (1987)

Register windows + Open architecture = Unix workstation dominance

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1987 |
| Total Registers | **136** |
| Visible | 32 |
| Pipeline | 4 stages |
| Open | **First open CPU!** |

---

## Register Windows

```
136 registers, 32 visible at once
Procedure call = rotate window
Zero memory access!
```

---

## Basic Usage

```python
from sparc_model import SPARCQueueModel
model = SPARCQueueModel('sparc_model.json')
ipc, _ = model.predict_ipc(0.60)
print(f"IPC: {ipc:.4f}")
```

---

## Legacy

First open processor architecture. Influenced RISC-V.

---

**Version:** 1.0
