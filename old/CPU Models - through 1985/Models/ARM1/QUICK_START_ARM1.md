# ARM1 - Quick Start Guide

## Birth of ARM Architecture (1985)

25,000 transistors. 8 MHz. Changed the world.

---

## Quick Facts

| Spec | Value |
|------|-------|
| Year | April 26, 1985 |
| Transistors | **25,000** (vs 275,000 for 386!) |
| Clock | 8 MHz |
| Pipeline | 3 stages |
| Registers | 16 |
| Architecture | RISC |
| IPC | ~0.65 |

---

## What Made ARM Special

1. **Conditional execution** - Every instruction can be conditional
2. **Barrel shifter** - Free shift on second operand
3. **16 registers** - Fewer memory accesses
4. **Load/store** - Clean RISC architecture

---

## Designers

- **Sophie Wilson** - Instruction set
- **Steve Furber** - Hardware

Both received CBE honors.

---

## Basic Usage

```python
from arm1_model import ARM1QueueModel

model = ARM1QueueModel('arm1_model.json')
ipc, _ = model.predict_ipc(0.45)
print(f"IPC: {ipc:.4f}")

# Compare to contemporaries
comp = model.compare_contemporary()
print(f"ARM: {comp['ARM1']['transistors']:,} transistors")
print(f"386: {comp['80386']['transistors']:,} transistors")
```

---

## Legacy

ARM1 → ARM2 → ... → iPhone → ~250 billion chips

**The architecture that powers every smartphone.**

---

**Version:** 1.0
