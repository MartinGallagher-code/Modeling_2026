# Signetics 2650 CPU Queueing Model

## Executive Summary

The Signetics 2650 (1975) was an innovative 8-bit processor that never achieved mainstream success. Its most notable limitation was a **15-bit address bus** that restricted it to just **32KB of memory** when competitors offered 64KB. Despite some clever features like position-independent code support, this fundamental limitation doomed it to obscurity.

**Key Finding:** The 2650 demonstrates that **architectural limitations can kill otherwise good designs**. Its 32KB address space ceiling meant it couldn't grow with applications, causing customers to choose competitors with 64KB addressing.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1975 |
| Word Size | 8 bits |
| Data Bus | 8 bits |
| Address Bus | **15 bits** (32KB only!) |
| Clock Speed | 1.25 MHz |
| Registers | 7 |
| Page Size | 8KB |
| Typical IPC | ~0.06 |

---

## The 32KB Problem

### Address Space Comparison
```
Processor    Address Bits    Maximum Memory
---------    ------------    --------------
8080         16              64KB
6800         16              64KB
6502         16              64KB
2650         15              32KB  ← PROBLEM!
```

### Why 15 Bits?
```
Design decision for simplicity:
- 8KB pages (13 bits)
- 4 pages maximum (2 bits)
- Total: 15 bits = 32KB

Seemed adequate in 1975...
But applications grew quickly.
```

### The Consequence
```
1975: 32KB seems fine
1977: Applications need more
1979: 32KB is crippling limitation

Customers chose 8080/6502 instead.
```

---

## Architecture

### Register Set
```
R0:    8-bit accumulator
R1-R3: 8-bit general registers
R4-R6: 8-bit index registers

PSU:   Program Status Upper
PSL:   Program Status Lower (flags)
```

### Memory Organization
```
Page 0: 0x0000 - 0x1FFF (8KB)
Page 1: 0x2000 - 0x3FFF (8KB)
Page 2: 0x4000 - 0x5FFF (8KB)
Page 3: 0x6000 - 0x7FFF (8KB)
              Total: 32KB
```

### Addressing Modes
- Immediate
- Absolute (within page)
- Relative (position-independent)
- Indexed
- Indirect

### Good Features (Overshadowed by 32KB limit)
1. **Relative addressing** - Good for PIC
2. **Sense flag** - External input testable
3. **Clean instruction set** - Fairly orthogonal
4. **Condition codes** - Complete flag set

---

## Historical Context

### Development
```
Designer: Signetics (Philips subsidiary)
Year: 1975
Market: European computers, game consoles
Competition: 8080, 6800, 6502
```

### Systems Using 2650
- **Interton VC 4000** - Console family (Europe)
- **Emerson Arcadia 2001** - Game console
- Various European hobby computers
- Some industrial controllers

### The VC 4000 Family
```
A confusing ecosystem of clones:
- Interton VC 4000 (Germany)
- Acetronic MPU-1000 (UK)
- Hanimex HMG-1292 (France)
- Fountain various (Asia)
- 20+ different brands, same hardware

All limited by 2650's 32KB ceiling.
```

### Why It Failed
| Issue | Impact |
|-------|--------|
| 32KB limit | Couldn't grow with apps |
| European focus | Missed US market |
| Weak ecosystem | Limited software/tools |
| Unusual arch | Hard to port code |

---

## Performance Model

### Queueing Architecture
```
λ → [Execute (sequential)] → Completed
```

### Timing
```
Clock cycles per machine cycle: 3
Average instruction: 2-3 machine cycles
Total: 6-9 clock cycles per instruction
```

### Service Time
- Average: ~7.9 cycles per instruction
- Maximum IPC: ~0.13
- Practical IPC: ~0.06

---

## Comparison with Competitors

### vs 8080 (1974)
| Feature | 2650 | 8080 |
|---------|------|------|
| Address Space | 32KB | 64KB |
| Clock | 1.25 MHz | 2 MHz |
| Ecosystem | Weak | Strong |
| Winner | - | **8080** |

### vs 6502 (1975)
| Feature | 2650 | 6502 |
|---------|------|------|
| Address Space | 32KB | 64KB |
| Cost | Medium | Low |
| Ecosystem | Weak | Growing |
| Winner | - | **6502** |

---

## Usage

```python
from signetics_2650_model import Signetics2650QueueModel

model = Signetics2650QueueModel('signetics_2650_model.json')

# Predict IPC
ipc, metrics = model.predict_ipc(0.05)
print(f"IPC: {ipc:.4f}")

# Note the address limitation
print(f"Max memory: {model.config['memory_system']['max_memory_kb']}KB")
# Output: 32KB - the fatal flaw!
```

---

## Legacy

### What 2650 Teaches
1. **Address space matters** - Don't limit growth
2. **Ecosystem matters** - Technical merit isn't enough
3. **Standards matter** - Unusual = incompatible
4. **Regional focus limits reach** - Need global market

### Modern Parallels
```
32-bit address (4GB) vs 64-bit:
- Same lesson, larger scale
- 32-bit hit limits by 2000s
- 64-bit now standard

The 2650's mistake repeated!
```

---

## Conclusion

The Signetics 2650 is a cautionary tale about architectural limitations:

- **Good design** in many respects
- **Fatal flaw:** 32KB address space
- **Couldn't compete** with 64KB competitors
- **Forgotten** except by retro enthusiasts

**Lesson:** When setting architectural limits, err on the side of more capacity. The 2650 saved a few pins but lost the market.

---

**Version:** 1.0  
**Date:** January 24, 2026
