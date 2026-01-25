# Texas Instruments TMS9995 Queueing Model

## Enhanced TMS9900 (1981)

The TMS9995 was an improved version of the TMS9900, featuring on-chip RAM and an 8-bit external bus for lower system cost.

---

## Executive Summary

| Spec | TMS9900 | TMS9995 |
|------|---------|---------|
| Year | 1976 | 1981 |
| External Bus | 16-bit | **8-bit** |
| On-chip RAM | None | **256 bytes** |
| Clock | 3 MHz | 12 MHz (/4) |
| Timer | External | **On-chip** |

---

## The Workspace Architecture

TMS99xx processors had a unique design: **registers lived in RAM**.

```
Traditional CPU:              TMS99xx:
┌─────────────────┐          ┌─────────────────┐
│      CPU        │          │      CPU        │
│  ┌───────────┐  │          │  ┌───────────┐  │
│  │ R0-R15    │  │          │  │    WP     │──┼──┐
│  │ (on-chip) │  │          │  │(workspace │  │  │
│  └───────────┘  │          │  │ pointer)  │  │  │
└─────────────────┘          └─────────────────┘  │
        │                            │            │
        ▼                            ▼            │
┌─────────────────┐          ┌─────────────────┐  │
│     Memory      │          │     Memory      │  │
│                 │          │  ┌───────────┐  │◄─┘
│                 │          │  │ R0-R15    │  │
│                 │          │  │ (in RAM!) │  │
│                 │          │  └───────────┘  │
└─────────────────┘          └─────────────────┘
```

### Advantages
- **Instant context switch**: Just change WP pointer
- **Multiple register sets**: Each task has own workspace
- **Fast interrupts**: Hardware changes WP automatically

### Disadvantages
- **Slower register access**: Every register op hits memory
- **Memory bandwidth**: Registers compete with data

---

## TMS9995 Improvements

| Feature | Benefit |
|---------|---------|
| 256B on-chip RAM | Workspace can be on-chip (fast!) |
| 8-bit bus | Lower cost PCB |
| On-chip timer | No external chip needed |
| Higher clock | 12 MHz (3 MHz effective) |

---

## Systems Using TMS9995

### TI-99/8 (Unreleased)
- Would have been TI-99/4A successor
- Cancelled when TI exited home computers (1983)

### Myarc Geneve 9640 (1987)
- Third-party TI-99 compatible
- TMS9995 at 12 MHz
- 512KB RAM
- Popular with TI-99 enthusiasts

---

## Performance

| Metric | Value |
|--------|-------|
| IPC | ~0.07 |
| MIPS @ 3 MHz | ~0.21 |
| Limitation | Workspace memory access |

The workspace architecture trades raw speed for fast context switching.

---

## Files

| File | Description |
|------|-------------|
| `ti_tms9995_model.py` | Python implementation |
| `ti_tms9995_model.json` | Configuration |
| `TI_TMS9995_README.md` | This document |
| `QUICK_START_TMS9995.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The TMS9995: Fast context switches, unique architecture."*
