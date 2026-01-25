# Intel 8008 CPU Queueing Model

## THE FIRST 8-BIT MICROPROCESSOR (1972)

The Intel 8008 was the **first 8-bit microprocessor ever made**. Every x86 processor - from the original IBM PC to today's Core i9 - traces its lineage back to this chip.

---

## Executive Summary

| Specification | Value |
|---------------|-------|
| Year | 1972 |
| Word Size | 8 bits |
| Clock | 500 kHz - 800 kHz |
| Address Space | 16 KB (14-bit) |
| Transistors | 3,500 |
| Package | 18-pin DIP |
| IPC | ~0.04 |
| Price | $120 |

---

## The Datapoint Story

### How the 8008 Almost Didn't Happen

```
1969: Datapoint Corporation needs a CPU for their 2200 terminal
      ↓
      Intel agrees to design a single-chip CPU
      ↓
1971: Intel delivers the 8008
      ↓
      Datapoint rejects it: "Too slow, we'll use TTL instead"
      ↓
      Datapoint takes cash payment instead of chip rights
      ↓
      Intel keeps the 8008 and creates the microprocessor industry
      
THE IRONY: Datapoint could have owned the microprocessor!
```

---

## Architecture

### Register Set

```
┌─────────────────────────────────────────────────────┐
│                 Intel 8008 Registers                │
├─────────────────────────────────────────────────────┤
│                                                     │
│    ┌─────┐                                          │
│    │  A  │  ← Accumulator (all arithmetic here)    │
│    └─────┘                                          │
│                                                     │
│    ┌─────┬─────┐                                    │
│    │  B  │  C  │  ← General purpose                │
│    └─────┴─────┘                                    │
│                                                     │
│    ┌─────┬─────┐                                    │
│    │  D  │  E  │  ← General purpose                │
│    └─────┴─────┘                                    │
│                                                     │
│    ┌─────┬─────┐                                    │
│    │  H  │  L  │  ← Memory pointer (HL = address)  │
│    └─────┴─────┘                                    │
│                                                     │
│    These register names survive in x86 today!       │
│    (AL, BL, CL, DL, AH, BH, CH, DH)                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### The 7-Level Stack Problem

Unlike later processors with stack in RAM, the 8008 had a **hardware stack of only 7 levels**:

```
┌─────────────────────┐
│   On-Chip Stack     │
├─────────────────────┤
│ Level 7 (deepest)   │
│ Level 6             │
│ Level 5             │  ← Only 7 levels!
│ Level 4             │     No recursive algorithms!
│ Level 3             │     No deep call chains!
│ Level 2             │
│ Level 1 (top)       │
└─────────────────────┘

Exceeding 7 levels = CRASH (stack overflow wraps around)
```

This was a **major limitation** that the 8080 fixed with stack in RAM.

### Memory Map

```
0000h ┌─────────────────────┐
      │                     │
      │    Program ROM      │
      │                     │
      ├─────────────────────┤
      │                     │
      │    Data RAM         │
      │                     │
3FFFh └─────────────────────┘
      
      Only 16 KB addressable!
      (14-bit address bus)
```

---

## Instruction Set

### 48 Instructions Total

| Category | Instructions | Example |
|----------|--------------|---------|
| Data Transfer | MOV, MVI | MOV A,B (A←B) |
| Arithmetic | ADD, SUB, INR, DCR | ADD B (A←A+B) |
| Logical | ANA, ORA, XRA | ANA C (A←A AND C) |
| Branch | JMP, Jcc, CALL, RET | JMP 1234h |
| I/O | IN, OUT | IN 5 |
| Control | HLT, NOP | HLT |

### No Multiply or Divide!
All multiplication and division had to be done in software loops.

### Instruction Timing

| Instruction Type | Clock States |
|------------------|--------------|
| Register-Register | 5 |
| Immediate Load | 8 |
| Memory Read | 8 |
| Memory Write | 7 |
| Jump | 11 |
| Call | 11 |
| Return | 5 |

At 500 kHz: ~20,000 instructions per second

---

## The Multiplexed Bus Problem

### 18-Pin Package Limitation

The 8008 came in an **18-pin DIP** package - far too few pins for separate address and data buses. Solution: multiplex them.

```
8008 Pinout (18 pins):
┌──────────────────────────────┐
│                              │
│  D0-D7: Data/Address (low)   │  ← 8 pins do double duty!
│  S0-S2: State outputs        │
│  SYNC: Cycle start           │
│  +5V, -9V, GND               │  ← Needed THREE voltages!
│  φ1, φ2: Two-phase clock     │
│  READY, INT                  │
│                              │
└──────────────────────────────┘
```

### External Support Required

A complete 8008 system needed ~20 TTL chips:

```
                    ┌────────────┐
                    │   8008     │
                    │    CPU     │
                    └─────┬──────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Address │      │  State  │      │  Clock  │
   │ Latches │      │ Decode  │      │Generator│
   │ (8212)  │      │  Logic  │      │         │
   └─────────┘      └─────────┘      └─────────┘
        │                 │
        ▼                 ▼
   ┌─────────┐      ┌─────────┐
   │ Memory  │      │   I/O   │
   │ Decode  │      │ Control │
   └─────────┘      └─────────┘
   
   Total: ~20 support chips!
```

This complexity was a major factor in the 8008's limited adoption.

---

## Performance Analysis

### IPC Calculation

```
Average instruction time:
  Register ops (30%): 5 states × 0.30 = 1.5
  Memory ops (35%):   7.5 states × 0.35 = 2.625
  Branches (20%):     11 states × 0.20 = 2.2
  I/O ops (10%):      8 states × 0.10 = 0.8
  Other (5%):         4 states × 0.05 = 0.2
                                        -------
  Average:                              7.325 states

  Plus multiplexed bus overhead (~20%): 7.325 × 1.2 = 8.79 states
  
  IPC = 1 / 8.79 ≈ 0.04
```

### Throughput

| Clock | IPC | MIPS | Instructions/sec |
|-------|-----|------|------------------|
| 500 kHz | 0.04 | 0.02 | 20,000 |
| 800 kHz | 0.04 | 0.032 | 32,000 |

---

## Evolution to 8080

The 8008's limitations directly motivated the 8080 design:

| Problem in 8008 | Solution in 8080 |
|-----------------|------------------|
| 500 kHz clock | 2 MHz (4× faster) |
| 16 KB address | 64 KB address (4×) |
| 7-level stack | Stack in RAM (unlimited) |
| Multiplexed bus | Separate buses (simpler) |
| 18-pin package | 40-pin package |
| Three voltages | Single +5V (+12V for some) |
| ~20 support chips | ~5 support chips |

The 8080 was essentially "8008 done right" and launched the microcomputer revolution.

---

## Systems Using the 8008

Despite its limitations, the 8008 appeared in some notable systems:

### SCELBI-8H (1974)
- First commercially **advertised** personal computer
- $565 kit, $440 for board only
- 1 KB RAM standard

### Mark-8 (1974)
- Featured in Radio-Electronics magazine
- First widely-built hobby computer
- ~2,500 kits sold

### MCM/70 (1973)
- Portable computer from MCM
- Built-in APL interpreter
- Used in business applications

---

## Legacy

### Register Names Live On

```
8008 Register    →    Modern x86
     A           →    AL (low byte of EAX)
     B           →    BL
     C           →    CL
     D           →    DL
     H           →    (became part of addressing)
     L           →    (became part of addressing)
```

### The Lineage

```
8008 (1972)
  │
  ▼
8080 (1974) ─── launched CP/M, Altair
  │
  ▼
8085 (1976)
  │
  ▼
8086 (1978) ─── launched IBM PC architecture
  │
  ├──► 80286 ──► 80386 ──► 80486 ──► Pentium ──► ...
  │
  ▼
Core i9 (2024) ─── still runs 8086 code!
```

**Every x86 processor can trace its instruction set back to the 8008.**

---

## Model Usage

```python
from intel_8008_model import Intel8008QueueModel

model = Intel8008QueueModel('intel_8008_model.json')

# Predict performance
ipc, metrics = model.predict_ipc(0.035)
print(f"IPC: {ipc:.4f}")

# Compare to successors
comp = model.compare_to_successors()
print(f"8008→8080 improvement: {comp['improvement_8008_to_8080']}")
```

---

## Files

| File | Description |
|------|-------------|
| `intel_8008_model.py` | Python implementation |
| `intel_8008_model.json` | Configuration |
| `INTEL_8008_README.md` | This document |
| `QUICK_START_8008.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

## References

- Intel 8008 Data Sheet (1972)
- "A History of Modern Computing" - Paul Ceruzzi
- Computer History Museum archives
- Datapoint 2200 documentation

---

**Version:** 1.0  
**Date:** January 24, 2026

*"The 8008: Where the x86 journey began."*
