# General Instrument CP1600 Queueing Model

## THE INTELLIVISION CPU (1975)

The CP1600 was one of the first 16-bit microprocessors and is most famous as the brain of the Mattel Intellivision video game console.

---

## Executive Summary

| Spec | Value |
|------|-------|
| Year | 1975 |
| Bits | 16 |
| Clock | 894.886 kHz |
| Registers | 8 × 16-bit |
| Famous Use | **Intellivision** (3M+ sold) |

---

## The Intellivision

The CP1600's claim to fame was the **Mattel Intellivision** (1979):

- Sold **3+ million units**
- First serious Atari 2600 competitor
- 16-bit CPU vs Atari's 8-bit 6507
- First console with voice synthesis
- First downloadable content (PlayCable, 1981)

Notable games: Astrosmash, Utopia, AD&D Cloudy Mountain, MLB Baseball

---

## The PIC Connection

The CP1600 needed an I/O controller, so GI designed the **PIC1650** (1977):

```
CP1600 (1975)           PIC1650 (1977)
   │                        │
   │                        ▼
   └── Needed I/O ────► Designed PIC
       controller           │
                           ▼
                    PIC became MORE successful
                    than CP1600 itself!
                    (Billions shipped)
```

---

## Register Set

| Register | Purpose |
|----------|---------|
| R0-R5 | General purpose |
| R6 | Stack Pointer (SP) |
| R7 | Program Counter (PC) |

All registers are 16-bit and can be used for addressing.

---

## Comparison to Other 16-bit CPUs

| CPU | Year | MHz | Use |
|-----|------|-----|-----|
| CP1600 | 1975 | 0.9 | Intellivision |
| TMS9900 | 1976 | 3.0 | TI-99/4A |
| 8086 | 1978 | 5.0 | IBM PC |
| 68000 | 1979 | 8.0 | Mac |

The CP1600 was early but relatively slow.

---

## Files

| File | Description |
|------|-------------|
| `gi_cp1600_model.py` | Python implementation |
| `gi_cp1600_model.json` | Configuration |
| `GI_CP1600_README.md` | This document |
| `QUICK_START_CP1600.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The CP1600: Gaming history in 16 bits."*
