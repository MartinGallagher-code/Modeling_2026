# Intel iAPX 432 CPU Queueing Model

## INTEL'S BIGGEST FAILURE (1981)

The iAPX 432 was Intel's most ambitious project - a "micromainframe" intended to replace mainframe computers. It was a complete disaster that nearly bankrupted the company.

---

## Executive Summary

| Spec | iAPX 432 | 8086 (same era) |
|------|----------|-----------------|
| Year | 1981 | 1978 |
| Chips for CPU | **3** | 1 |
| Clock | 8 MHz | 5 MHz |
| IPC | **0.02** | 0.12 |
| MIPS | **0.16** | 0.60 |
| Result | **FAILED** | IBM PC! |

**The 432 was 4-10× SLOWER than the older, simpler 8086.**

---

## What Intel Tried To Build

```
┌─────────────────────────────────────────────────────────────┐
│                    iAPX 432 "Micromainframe"                │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   43201     │   │   43202     │   │   43203     │       │
│  │   GDP       │◄─►│   IP        │◄─►│   BIU       │       │
│  │ (General    │   │ (Interface  │   │ (Bus        │       │
│  │  Data       │   │  Processor) │   │  Interface) │       │
│  │  Processor) │   │             │   │             │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│         │                                    │              │
│         └───────────────┬────────────────────┘              │
│                         │                                   │
│                    System Bus                               │
│                         │                                   │
│         ┌───────────────┼───────────────┐                  │
│         ▼               ▼               ▼                  │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│    │ Memory  │    │ Memory  │    │  I/O    │             │
│    │Controller│   │Controller│   │Controller│             │
│    └─────────┘    └─────────┘    └─────────┘             │
│                                                             │
│  TOTAL: 6+ chips just to have a working CPU!               │
└─────────────────────────────────────────────────────────────┘
```

Compare to 8086: **1 chip** + simple support logic.

---

## Revolutionary Features (That Didn't Help)

### Capability-Based Architecture
- Hardware-enforced object protection
- Every memory access checked for permissions
- **Cost:** Massive performance overhead

### Object-Oriented Hardware
- Hardware support for OOP concepts
- Garbage collection assist
- **Cost:** Complexity, slow execution

### Variable-Length Instructions
- 6 to 321 bits per instruction
- Bit-aligned (not byte-aligned!)
- **Cost:** Incredibly slow decode

### Ada Optimization
- Designed specifically for Ada language
- **Problem:** Market wanted C and Pascal

---

## Why It Failed

### 1. TOO SLOW

| Processor | Clock | MIPS | Relative |
|-----------|-------|------|----------|
| 68000 | 8 MHz | 1.04 | 1.0× |
| 8086 | 5 MHz | 0.60 | 0.58× |
| **432** | **8 MHz** | **0.16** | **0.15×** |

The 432 was **6× slower than 68000** at the same clock!

### 2. TOO COMPLEX
- 3 chips for CPU (vs 1 for 8086)
- Complex support circuitry
- Difficult to program

### 3. TOO EXPENSIVE
- Multi-chip = high manufacturing cost
- Large board area required
- Power hungry

### 4. WRONG TIMING
- 1981: IBM chooses 8088 for PC
- 1981: 432 finally ships (late)
- 1982: IBM PC explodes in popularity
- 432 had no market

### 5. NO ECOSYSTEM
- No compilers ready at launch
- No operating systems
- No software base

---

## The Aftermath

```
1975: Project starts ("Micromainframe")
1981: Finally ships (6 years late)
1982: IBM PC dominates with 8088
1984: Clear the 432 has failed
1985: Project effectively dead
1986: Officially cancelled

COST: Hundreds of millions of dollars
      Nearly bankrupted Intel
      
SAVED BY: Success of 8086/8088 in IBM PC
```

---

## Lessons Learned

These lessons directly influenced the 80386 design:

| 432 Mistake | 386 Solution |
|-------------|--------------|
| Multi-chip | Single chip |
| Capability overhead | Optional protection |
| Bit-aligned instrs | Byte-aligned |
| Ada optimized | C optimized |
| New architecture | 8086 compatible |
| Slow | Fast |

The 80386 was everything the 432 wasn't - and it succeeded.

---

## Historical Significance

Despite its failure, the 432 was historically important:

1. **Proved capability architectures impractical** for mainstream
2. **Taught Intel** that simple wins
3. **Influenced 386** design (what NOT to do)
4. **Pioneered ideas** later used in Itanium (also troubled)

---

## Usage

```python
from intel_iapx432_model import InteliAPX432QueueModel

model = InteliAPX432QueueModel('intel_iapx432_model.json')
ipc, _ = model.predict_ipc(0.02)
print(f"IPC: {ipc:.4f}")  # Terribly slow

# See why it failed
for reason in model.why_failed():
    print(reason)
```

---

**Version:** 1.0  
**Date:** January 25, 2026

*"The 432: A masterpiece of overengineering."*
