# NEC V20 CPU Queueing Model

## The Chip That Beat Intel (1984)

The NEC V20 was a **drop-in replacement for the Intel 8088** that ran 10-40% faster and included a hardware 8080 emulation mode. It sparked the famous Intel vs NEC lawsuit - which NEC won, enabling the entire x86 clone industry.

---

## Executive Summary

| Specification | Intel 8088 | NEC V20 |
|---------------|------------|---------|
| Year | 1979 | 1984 |
| Clock | 5-8 MHz | 8-10 MHz |
| Pin Compatible | - | **YES** |
| 16-bit MUL | 118 cycles | **25 cycles (4.7×)** |
| 16-bit DIV | 150 cycles | **30 cycles (5×)** |
| 8080 Mode | No | **YES** |
| IPC | 0.10 | **0.12** |

---

## Drop-In Upgrade

```
BEFORE:                         AFTER:
┌─────────────────┐            ┌─────────────────┐
│   IBM PC/XT     │            │   IBM PC/XT     │
│  ┌───────────┐  │            │  ┌───────────┐  │
│  │  Intel    │  │            │  │   NEC     │  │
│  │   8088    │  │  ──────►   │  │   V20     │  │
│  └───────────┘  │   Swap!    │  └───────────┘  │
│                 │            │                 │
└─────────────────┘            └─────────────────┘
     Standard                    10-40% FASTER!

Just pull out the 8088 and plug in the V20.
No other changes needed.
```

---

## Performance Improvements

### Multiply/Divide Revolution

| Operation | 8088 Cycles | V20 Cycles | Speedup |
|-----------|-------------|------------|---------|
| MUL 8×8 | 70-77 | 13 | **5.7×** |
| MUL 16×16 | 118-133 | 25 | **4.7×** |
| DIV 16/8 | 80-90 | 16 | **5.0×** |
| DIV 32/16 | 144-162 | 30 | **5.0×** |

### Barrel Shifter

```
8088:  SHL AX, CL  ; Takes 4 + n cycles (n = shift count)
       SHL AX, 8   ; = 12 cycles!

V20:   SHL AX, CL  ; Takes 1 cycle regardless!
       SHL AX, 8   ; = 1 cycle!
```

### Optimized String Operations

REP MOVSB, REP STOSB, etc. run 20-30% faster.

---

## Hardware 8080 Mode

The V20 could switch to **native 8080 mode**:

```asm
    ; Switch to 8080 mode
    DB 0Fh, 0FFh    ; BRKEM instruction
    
    ; Now running 8080 code!
    ; Full 8080 instruction set
    ; 64KB address space
    ; Can run CP/M!
    
    ; Switch back to 8086 mode
    DB 0EDh, 0FDh   ; RETEM instruction
```

This let IBM PC owners run CP/M software!

---

## The Lawsuit (1984-1989)

### Timeline

```
1984: NEC releases V20/V30
      Intel sues NEC for "copying microcode"
      
1985-1988: Legal battle
           NEC proves clean-room design
           
1989: Verdict - NEC WINS!
      Judge rules NEC did not copy Intel
      Intel's microcode copyright not infringed
      
RESULT: Legal precedent for x86 clones!
```

### Impact

The NEC victory enabled:
- **AMD** to make 386/486/K5/K6/Athlon clones
- **Cyrix** to make x86-compatible chips
- **VIA** to continue x86 development
- The entire x86 clone industry

**Intel's lawsuit backfired spectacularly.**

---

## V20 vs V30

| Chip | Replaces | Data Bus | Target |
|------|----------|----------|--------|
| V20 | 8088 | 8-bit | PC/XT |
| V30 | 8086 | 16-bit | AT-class |

---

## Technical Specifications

| Spec | Value |
|------|-------|
| Clock | 8-10 MHz |
| Transistors | ~63,000 |
| Package | 40-pin DIP |
| Process | 2.0 µm CMOS |
| Voltage | +5V |

---

## New Instructions

The V20 added instructions beyond 8088:

| Instruction | Function |
|-------------|----------|
| INM/OUTM | Block I/O |
| ROL4/ROR4 | Nibble rotate (BCD) |
| REPC/REPNC | Conditional repeat |
| TEST1/SET1/CLR1 | Bit operations |
| ADD4S/SUB4S | BCD arithmetic |

---

## Market Success

- **Millions sold** as PC/XT upgrades
- Many "turbo" PCs shipped with V20/V30
- Popular with power users
- Created V40/V50 embedded variants

---

## Usage

```python
from nec_v20_model import NECV20QueueModel

model = NECV20QueueModel('nec_v20_model.json')
ipc, _ = model.predict_ipc(0.10)
print(f"IPC: {ipc:.4f}")

# Compare to 8088
comp = model.compare_8088()
print(f"Multiply speedup: {comp['multiply_16_cycles']['speedup']}")
```

---

## Files

| File | Description |
|------|-------------|
| `nec_v20_model.py` | Python implementation |
| `nec_v20_model.json` | Configuration |
| `NEC_V20_README.md` | This document |
| `QUICK_START_V20.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0  
**Date:** January 25, 2026

*"The V20: Faster than Intel, and legally so."*
