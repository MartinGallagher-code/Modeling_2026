# General Instrument PIC1650 Queueing Model

## THE FIRST PIC MICROCONTROLLER (1977)

The PIC1650 started as a simple I/O controller but became the ancestor of one of the most successful microcontroller families ever - billions shipped!

---

## Executive Summary

| Spec | Value |
|------|-------|
| Year | 1977 |
| Instructions | 33 |
| Program Memory | 512 words (12-bit) |
| Data RAM | 32 bytes |
| Architecture | Harvard |
| IPC | ~0.90 |

---

## Origin Story

```
1975: GI designs CP1600 CPU (for Intellivision)
      Needs a cheap I/O controller
      
1976-77: Designs "Peripheral Interface Controller" (PIC)
         Simple, cheap, easy to use
         
1980s: PICs become popular standalone MCUs
       Much simpler than 8051
       
1989: GI spins off Microchip Technology
      PIC becomes their main product
      
2020s: Billions of PICs shipped
       Still one of top MCU families
```

---

## Harvard Architecture

The PIC used **Harvard architecture** (separate program and data buses):

```
┌─────────────────────────────────────────┐
│              PIC1650                     │
│                                          │
│  ┌────────────┐      ┌────────────┐     │
│  │  Program   │      │   Data     │     │
│  │  Memory    │      │   RAM      │     │
│  │  512×12    │      │   32×8     │     │
│  └─────┬──────┘      └─────┬──────┘     │
│        │ 12-bit            │ 8-bit      │
│        ▼                   ▼            │
│  ┌────────────────────────────────┐     │
│  │           CPU Core             │     │
│  │   ┌───┐                        │     │
│  │   │ W │ ← Working register     │     │
│  │   └───┘                        │     │
│  └────────────────────────────────┘     │
│                                          │
└─────────────────────────────────────────┘

Advantage: Can fetch next instruction while executing current
Result: Most instructions = 1 cycle!
```

---

## Simple Instruction Set

Only 33 instructions:

| Type | Examples | Purpose |
|------|----------|---------|
| Byte | MOVF, ADDWF, SUBWF | Register operations |
| Bit | BSF, BCF, BTFSC | Bit manipulation |
| Literal | MOVLW, ADDLW | Constants |
| Control | GOTO, CALL, RETURN | Flow control |

**All instructions are one word (12 bits).**
**Almost all execute in 1 cycle.**

---

## Why PIC Succeeded

### 1. Simplicity
- Only 33 instructions to learn
- Regular, predictable architecture
- Easy to hand-code assembly

### 2. Cost
- Extremely cheap to manufacture
- Available for pennies in volume

### 3. Availability
- Could buy them anywhere
- Multiple package options
- Easy to prototype with

### 4. Documentation
- Excellent datasheets
- Hundreds of application notes
- Clear, practical examples

### 5. Community
- Huge hobbyist following
- Free tools (assembler, programmer)
- Countless tutorials and projects

---

## Evolution

```
PIC1650 (1977)
    │ Original, 33 instructions
    ▼
PIC16C5x (1985)
    │ Enhanced, more memory
    ▼
PIC16F84 (1998)
    │ Flash memory, hobbyist favorite
    ▼
PIC18 (2000s)
    │ Enhanced architecture
    ▼
PIC24/dsPIC (2004+)
    │ 16-bit
    ▼
PIC32 (2007+)
    │ 32-bit (MIPS core)
    ▼
Still going strong!
```

---

## Legacy

The PIC architecture established:

1. **Harvard architecture** for MCUs (now common)
2. **Simple RISC-like** instruction sets
3. **Cheap, available** embedded processors
4. **Hobbyist-friendly** ecosystem

---

## Files

| File | Description |
|------|-------------|
| `gi_pic1650_model.py` | Python implementation |
| `gi_pic1650_model.json` | Configuration |
| `GI_PIC1650_README.md` | This document |
| `QUICK_START_PIC1650.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0  
**Date:** January 25, 2026

*"The PIC: Simple enough to learn, powerful enough to use."*
