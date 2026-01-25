# AMD Am2901 Bit-Slice Queueing Model

## BUILD YOUR OWN CPU! (1975)

The Am2901 is a 4-bit ALU "slice" - cascade them to build custom CPUs of any width with your own instruction set.

---

## The Bit-Slice Concept

```
Want a 16-bit CPU?     Use 4 slices:
                       ┌────────┬────────┬────────┬────────┐
                       │ Am2901 │ Am2901 │ Am2901 │ Am2901 │
                       │ Slice 3│ Slice 2│ Slice 1│ Slice 0│
                       │ (MSB)  │        │        │ (LSB)  │
                       └───┬────┴────┬───┴───┬────┴────┬───┘
                           │         │       │         │
                           └────┬────┴───┬───┴────┬────┘
                                │        │        │
                              D15-12   D11-8    D7-4    D3-0

Want 32-bit? Use 8 slices!
Want 64-bit? Use 16 slices!
```

---

## What's Inside Each Slice

```
┌─────────────────────────────────────┐
│            Am2901 Slice             │
│                                     │
│  ┌─────────────────────────────┐    │
│  │   16 x 4-bit Register File  │    │
│  │   (Dual-port RAM)           │    │
│  └─────────────┬───────────────┘    │
│                │                    │
│         ┌──────┴──────┐             │
│         ▼             ▼             │
│      ┌─────┐       ┌─────┐          │
│      │  A  │       │  B  │          │
│      └──┬──┘       └──┬──┘          │
│         └──────┬──────┘             │
│                ▼                    │
│         ┌───────────┐               │
│         │  4-bit    │               │
│         │   ALU     │ ← 8 functions │
│         └─────┬─────┘               │
│               │                     │
│         ┌─────▼─────┐               │
│         │  Shifter  │               │
│         └─────┬─────┘               │
│               │                     │
│         ┌─────▼─────┐               │
│         │  Q Reg    │               │
│         └───────────┘               │
└─────────────────────────────────────┘
```

---

## Am2900 Family

| Chip | Function |
|------|----------|
| **Am2901** | **4-bit ALU slice** |
| Am2902 | Carry lookahead |
| Am2903 | Enhanced ALU |
| Am2904 | Status/shift control |
| Am2909 | Microprogram sequencer |
| Am2910 | Enhanced sequencer |

---

## Why Bit-Slice?

### Advantages
- **FAST**: Schottky TTL = fastest available
- **Custom**: Define your own instruction set
- **Scalable**: Any word width

### Disadvantages
- **Complex**: Many chips, complex design
- **Expertise**: Need microcode skills
- **Cost**: Expensive in chip count

### Used Where Speed Justified Cost
- Minicomputers
- Supercomputers
- Military
- High-end graphics

---

## Famous Systems Using 2901

| System | Use |
|--------|-----|
| DEC VAX-11/780 | Floating point |
| Symbolics 3600 | Lisp machine |
| Xerox Star | Workstation |
| Atari arcade | Star Wars, etc. |
| Williams arcade | Defender, Joust |

---

## Modeling Approach

The 2901 is different - it's a building block, not a complete CPU.

Performance depends on:
1. Number of slices (width)
2. Microcode design
3. Clock speed
4. Supporting chips

This model provides framework for analyzing bit-slice systems.

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The Am2901: CPU construction kit."*
