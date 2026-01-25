# Motorola 68010 - Quick Start Guide

## Virtual Memory + Loop Mode

The 68010 (1982) added virtual memory support to the 68000, enabling Unix workstations.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | 1982 |
| Word Size | 32-bit internal |
| Data Bus | 16-bit |
| Clock | 8-12.5 MHz |
| vs 68000 | 5-10% faster |
| Key Feature | Virtual memory |

---

## Key Improvements

**1. Virtual Memory**
- Bus error recovery (68000 crashed)
- Enables demand paging
- Required for Unix

**2. Loop Mode**
- DBcc loops: 2 cycles vs 10
- 5× speedup for tight loops

**3. New Registers**
- VBR: Relocatable interrupt vectors
- SFC/DFC: MMU support

---

## Basic Usage

```python
from motorola_68010_model import Motorola68010QueueModel

model = Motorola68010QueueModel('motorola_68010_model.json')
ipc, _ = model.predict_ipc(0.35)
print(f"IPC: {ipc:.4f}")

comp = model.compare_68000()
print(f"vs 68000: {comp['speedup']:.2f}× faster")
```

---

## Systems
- Sun-2 workstations
- Apollo workstations  
- HP 9000/200

---

**Version:** 1.0
