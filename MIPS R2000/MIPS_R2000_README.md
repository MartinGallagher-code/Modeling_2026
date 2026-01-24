# MIPS R2000 CPU Queueing Model

## Executive Summary

The MIPS R2000 (1985) was the **purest expression of RISC principles**, designed by John Hennessy at Stanford. It became THE teaching architecture - millions of computer science students learned architecture through MIPS via the Patterson & Hennessy textbook.

**Key Finding:** MIPS succeeded not just commercially (PlayStation, SGI) but educationally. Its clean, simple design made it the perfect teaching tool, influencing how an entire generation thinks about processors.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Word Size | 32 bits |
| Registers | 32 (R0 = 0) |
| Pipeline | **5 stages** |
| Instructions | All 32 bits |
| Transistors | 110,000 |

---

## RISC Purity

### The MIPS Philosophy
```
1. Simple instructions (one operation each)
2. Fixed instruction size (32 bits)
3. Load/store architecture (only L/S access memory)
4. Large register file (32 registers)
5. Hardwired control (no microcode)
6. Delayed branches (fill delay slots)
```

### R0 = Zero
```
R0 is HARDWIRED to zero. Always reads as 0.

Why? Simplifies many operations:
  MOV R1, R2   →  ADD R1, R0, R2
  CLR R1       →  ADD R1, R0, R0
  NOP          →  ADD R0, R0, R0
```

---

## The 5-Stage Pipeline

```
┌────┐   ┌────┐   ┌────┐   ┌─────┐   ┌────┐
│ IF │ → │ ID │ → │ EX │ → │ MEM │ → │ WB │
└────┘   └────┘   └────┘   └─────┘   └────┘

IF:  Instruction Fetch
ID:  Instruction Decode + Register Read
EX:  Execute (ALU) or Address Calculation
MEM: Memory Access (load/store only)
WB:  Write Back to register file
```

This 5-stage pipeline became THE reference model for teaching.

---

## Educational Impact

### The Textbook
```
"Computer Organization and Design"
by Patterson and Hennessy

- First edition: 1994
- Still in print (6th edition)
- Used in >1000 universities
- Translated into many languages

MIPS is the architecture used throughout.
```

### Why MIPS for Teaching?
```
1. Clean design (easy to understand)
2. Regular instruction encoding
3. Clear pipeline model
4. Good documentation
5. Available simulators (SPIM, MARS)
6. Real commercial processor
```

---

## Commercial Success

### SGI Workstations
```
Silicon Graphics used MIPS processors:
- IRIS series
- Indigo
- Indy
- O2
- Octane

Famous for:
- Jurassic Park rendering
- Movie visual effects
- 3D graphics leadership
```

### PlayStation
```
PlayStation 1 (1994): MIPS R3000 @ 33 MHz
PlayStation 2 (2000): MIPS R5900 @ 295 MHz
PlayStation Portable (2004): MIPS-based

300+ million consoles with MIPS!
```

### Networking
```
Cisco routers used MIPS extensively.
Your internet traffic probably passed
through MIPS processors.
```

---

## Pipeline Hazards

### Data Hazards
```
ADD R1, R2, R3   ; R1 = R2 + R3
SUB R4, R1, R5   ; Needs R1! (not ready)

Solution: Forwarding
- Pass result directly from EX to next instruction
- No stall needed
```

### Control Hazards
```
BEQ R1, R2, target  ; Branch
ADD R3, R4, R5      ; Delay slot (always executes)
...
target:

MIPS uses delayed branches:
- Instruction after branch always executes
- Compiler fills with useful work (or NOP)
```

---

## Performance

### Ideal vs Actual CPI
```
Ideal CPI: 1.0 (one instruction per cycle)
Actual CPI: 1.2-1.5 (hazards, cache misses)

Still excellent for 1985!
```

### MIPS vs Competition (1987)
| Processor | MIPS | Architecture |
|-----------|------|--------------|
| MIPS R2000 | 10 | RISC |
| SPARC | 10 | RISC |
| Intel 386 | 6 | CISC |
| 68020 | 5 | CISC |

---

## Usage

```python
from mips_r2000_model import MIPSR2000QueueModel

model = MIPSR2000QueueModel('mips_r2000_model.json')
ipc, _ = model.predict_ipc(0.70)
print(f"IPC: {ipc:.4f}")

# See the famous pipeline
pipeline = model.explain_pipeline()
for stage, desc in pipeline.items():
    print(f"{stage}: {desc}")
```

---

## Legacy

### MIPS Today
- MIPS Technologies acquired multiple times
- MIPS architecture still used in embedded
- MIPS instruction set influenced RISC-V

### Educational Legacy
- Millions of students learned MIPS
- Shaped how we teach architecture
- Patterson & Hennessy textbook remains standard

---

## Conclusion

The MIPS R2000 succeeded on two fronts: commercially in workstations and game consoles, and educationally as THE teaching architecture. Its clean, simple design made complex concepts accessible to students worldwide.

**Lesson:** Elegance in design enables understanding. MIPS's success as a teaching tool stems from its conceptual clarity.

---

**Version:** 1.0 | **Date:** January 24, 2026
