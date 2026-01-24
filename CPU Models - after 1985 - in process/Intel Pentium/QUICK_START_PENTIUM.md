# Intel Pentium - Quick Start Guide

## First Superscalar x86 (1993)

Dual pipelines, IPC > 1.0, "Intel Inside" era begins.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1993 |
| Transistors | **3,100,000** |
| Pipelines | **2 (U and V)** |
| IPC | **>1.0** |
| Clock | 60-200 MHz |
| Data Bus | **64-bit** |

---

## Dual Pipeline
```
U-Pipe: All instructions
V-Pipe: Simple instructions only
~40% can pair → IPC ~1.2-1.4
```

---

## Basic Usage

```python
from intel_pentium_model import IntelPentiumQueueModel

model = IntelPentiumQueueModel('intel_pentium_model.json')
ipc, _ = model.predict_ipc(1.0)
print(f"IPC: {ipc:.4f}")  # > 1.0!
```

---

## The FDIV Bug

$475 million recall. Lesson: Verification matters!

---

**The processor that defined 1990s PC computing.**

---

**Version:** 1.0
