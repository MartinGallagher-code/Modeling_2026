# Z80 Peripheral Chips - Quick Reference

## NOT CPUs - These are I/O Support Chips

The Z80 family includes matched peripheral chips. No performance model - this is a reference only.

---

## The Four Main Peripherals

| Chip | Function | Key Feature |
|------|----------|-------------|
| **Z80-PIO** | Parallel I/O | 2×8-bit ports, bit control |
| **Z80-SIO** | Serial I/O | 2 channels, HDLC support |
| **Z80-CTC** | Counter/Timer | 4 channels, interrupts |
| **Z80-DMA** | DMA Controller | 1.25 MB/s, search mode |

---

## Why They Matter

```
Intel 8080 system: CPU + 8224 + 8228 + 8255 + 8251 + 8253 = 6+ chips
Z80 system:        CPU + PIO + SIO + CTC = 4 chips

Fewer chips, directly compatible, designed together.
```

---

## Daisy-Chain Interrupts

```
IEI → [PIO] → [SIO] → [CTC] → [DMA] → (ground)
       High ──────────────────────► Low Priority
```

All peripherals support Z80 Mode 2 vectored interrupts.

---

**Reference document only - no queueing model.**

---
**Version:** 1.0
