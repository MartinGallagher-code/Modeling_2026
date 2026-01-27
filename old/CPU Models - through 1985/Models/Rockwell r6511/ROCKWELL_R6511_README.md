# Rockwell R6511 Queueing Model

## 6502 MCU Variant (1980)

The R6511 was Rockwell's enhanced 6502 for embedded systems, adding on-chip RAM, I/O, serial port, and timers.

---

## On-Chip Features

| Feature | Specification |
|---------|---------------|
| CPU | 6502 core |
| RAM | 192 bytes |
| Parallel I/O | 32 lines (4 ports) |
| Serial | Full UART |
| Timers | 2 x 16-bit |
| Interrupts | Vectored controller |

---

## R65xx Family

```
Standard 6502
    │
    └── Rockwell Variants
            │
            ├── R6500/1: 6502 + 2KB ROM + 64B RAM
            │
            ├── R6511: 6502 + 192B RAM + UART ← THIS
            │
            └── R65C00: CMOS versions
```

---

## vs Standard 6502

| Component | 6502 System | R6511 |
|-----------|-------------|-------|
| CPU | 6502 | On-chip |
| RAM | External | **192B on-chip** |
| I/O | 6522 VIA | **On-chip** |
| Serial | 6551 ACIA | **On-chip** |
| Timer | External | **On-chip** |
| Chips needed | 5+ | **1** |

---

## Applications

- Industrial controllers
- Point-of-sale terminals
- Modems
- Test equipment
- Process control

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The R6511: 6502 made embedded-friendly."*
