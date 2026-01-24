# Intel 4004 CPU Queueing Model

## Executive Summary

The Intel 4004, announced on November 15, 1971, was **THE FIRST COMMERCIAL MICROPROCESSOR EVER MADE**. This tiny 4-bit chip, originally designed for a Japanese calculator company, launched a revolution that transformed every aspect of modern life.

**Key Finding:** The 4004 proves that revolutionary products don't need to be powerful - they need to be **possible**. With just 2,300 transistors running at 740 kHz, the 4004 demonstrated that a complete CPU could fit on a single chip, opening the door to everything that followed.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | November 15, 1971 |
| Word Size | 4 bits |
| Data Bus | 4 bits |
| Address Bus | 12 bits (4KB) |
| Clock Speed | 740 kHz |
| Transistors | **2,300** |
| Die Size | 12 mm² |
| Process | 10 µm |
| Package | 16-pin DIP |
| Price (1971) | $200 |

---

## Historical Significance

### The Birth of an Industry

Before the 4004:
- Computers filled rooms
- CPUs required multiple boards of chips
- Computing was for corporations and governments

After the 4004:
- Complete CPU on one chip
- Path to personal computers
- Computing for everyone

### The Busicom Story

```
1969: Busicom (Japan) approaches Intel for calculator chips
      Original design: 12 custom chips
      
1970: Ted Hoff proposes general-purpose processor instead
      Federico Faggin leads implementation
      
1971: 4004 completed, Busicom calculators ship
      Intel negotiates rights back for $60,000
      
Result: Intel owns the microprocessor
        Busicom goes bankrupt (1974)
        Intel becomes Intel
```

### The Designers

- **Federico Faggin** - Lead designer, chip layout
- **Ted Hoff** - Architecture concept
- **Stan Mazor** - Architecture and software
- **Masatoshi Shima** - Busicom engineer, logic design

---

## Architecture

### 4-Bit Design

```
Why 4 bits?
- Designed for BCD (Binary Coded Decimal)
- One digit (0-9) = 4 bits
- Perfect for calculators
- Simpler to implement
```

### Register Set

```
Accumulator:     4-bit main register
Index Registers: 16 × 4-bit (or 8 × 8-bit pairs)
Program Counter: 12-bit (4KB address space)
Stack:           3-level hardware stack (no RAM stack)
```

### Instruction Set

- 46 instructions
- 8-bit instruction width
- Some 2-byte instructions (jumps, calls)
- 8 or 16 clock cycles per instruction

---

## Performance

### By 1971 Standards

```
Clock: 740 kHz
Cycles/Instruction: ~10.8 average
Instructions/Second: ~68,500
Operations/Second: ~60,000

Equivalent to: Simple calculator operations
```

### By Modern Standards

```
Performance Comparison (1971 vs 2026):

                    4004            Modern CPU
Transistors:        2,300           50,000,000,000
Clock:              740 kHz         5,000 MHz
Performance:        0.07 MIPS       100,000+ MIPS

Improvement:        ~1,500,000× faster
                    ~22,000,000× more transistors
                    ~6,750× higher clock
```

---

## The MCS-4 Family

The 4004 was part of a chip set:

| Chip | Function |
|------|----------|
| 4001 | ROM (256 bytes) + I/O |
| 4002 | RAM (40 nibbles) + I/O |
| 4003 | Shift register |
| **4004** | **CPU** |

A complete system required multiple support chips.

---

## Queueing Model

### Architecture

```
λ → [Fetch-Decode-Execute] → Completed

Single-stage sequential execution
No pipeline, no parallelism
One instruction at a time
```

### Service Time

```
1-word instructions: 8 cycles
2-word instructions: 16 cycles
Average: ~10.8 cycles

At 740 kHz: ~14.6 µs per instruction
```

---

## Usage

```python
from intel_4004_model import Intel4004QueueModel

model = Intel4004QueueModel('intel_4004_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.08)
print(f"IPC: {ipc:.4f}")

# Historical comparison
comp = model.historical_comparison()
print(f"Transistors then: {comp['4004']['transistors']:,}")
print(f"Transistors now:  {comp['modern_cpu']['transistors']:,}")
print(f"Improvement: {comp['improvement']['transistors']:,.0f}×")
```

---

## Legacy

### What 4004 Started

```
1971: 4004 (4-bit) - First microprocessor
1972: 8008 (8-bit) - First 8-bit micro
1974: 8080 (8-bit) - First successful micro
1978: 8086 (16-bit) - x86 begins
1985: 80386 (32-bit) - Protected mode
2003: Opteron (64-bit) - Modern era
2026: Billions of transistors, GHz clocks, AI
```

### The Revolution

The 4004 enabled:
- Personal computers
- Smartphones
- Internet of Things
- Artificial Intelligence
- Modern civilization

**All from 2,300 transistors in 1971.**

---

## Conclusion

The Intel 4004 is the most historically significant processor ever made. Not because it was powerful - it wasn't. Not because it was fast - it wasn't. But because it **proved that a complete CPU could fit on a single chip**.

That proof changed everything.

**Lesson:** Revolutionary products open doors. What comes through those doors builds the future.

---

**Version:** 1.0  
**Date:** January 24, 2026
