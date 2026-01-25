# Intel 8008 - Quick Start

## THE FIRST 8-BIT MICROPROCESSOR (1972)

Ancestor of all x86 processors.

---

## Quick Specs

| Spec | Value |
|------|-------|
| Year | 1972 |
| Bits | 8 |
| Clock | 500-800 kHz |
| Address | 16 KB (14-bit) |
| Transistors | 3,500 |
| IPC | ~0.04 |
| MIPS | ~0.02 |

---

## Key Limitations

| Limitation | Impact |
|------------|--------|
| 7-level stack | No recursion! |
| 16 KB address | Too small |
| Multiplexed bus | ~20 support chips needed |
| Three voltages | Complex power supply |

---

## Registers

```
A = Accumulator
B, C, D, E = General purpose
H, L = Memory pointer (HL)

These names survive in x86!
(AL, BL, CL, DL)
```

---

## Evolution

```
8008 (1972) → 8080 (1974) → 8086 (1978) → ... → Core i9
     │
     └── Datapoint rejected it - Intel kept it!
```

---

## Performance

| Clock | MIPS |
|-------|------|
| 500 kHz | 0.02 |
| 800 kHz | 0.032 |

---

**First 8-bit microprocessor. Started the x86 lineage.**

---
**Version:** 1.0
