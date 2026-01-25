# RCA CDP1804 Queueing Model

## Enhanced Space Processor (1980)

The CDP1804 is the middle member of RCA's COSMAC family, adding on-chip RAM and timer to the radiation-hardened 1802 design.

---

## Executive Summary

| Spec | CDP1802 | CDP1804 | CDP1805 |
|------|---------|---------|---------|
| Year | 1974 | **1980** | 1984 |
| On-chip RAM | None | **64 bytes** | 64 bytes |
| Timer | None | **Yes** | Yes |
| Clock | 2 MHz | **5 MHz** | 5 MHz |

---

## The COSMAC Family

```
CDP1802 (1974)
    │ Original "COSMAC"
    │ Voyager 1 & 2, Galileo
    ▼
CDP1804 (1980) ← THIS CHIP
    │ Added: 64B RAM, Timer
    │ Enhanced missions
    ▼
CDP1805 (1984)
    │ More instructions
    │ New Horizons probe
    ▼
CDP1806
    │ Final evolution
```

---

## Enhancements Over 1802

| Feature | 1802 | 1804 |
|---------|------|------|
| On-chip RAM | None | **64 bytes** |
| Timer | External | **On-chip** |
| Max clock | 2 MHz | **5 MHz** |
| ROM option | No | **Mask ROM** |

---

## Why Silicon-on-Sapphire?

The 1802 family used **Silicon-on-Sapphire (SOS) CMOS**:

```
Regular CMOS:           SOS CMOS:
┌─────────────┐         ┌─────────────┐
│   Silicon   │         │   Silicon   │
├─────────────┤         ├─────────────┤
│   Silicon   │         │  Sapphire   │ ← Insulator!
│  Substrate  │         │  Substrate  │
└─────────────┘         └─────────────┘
      │                       │
Radiation can            Radiation cannot
cause latch-up           cause latch-up
```

**Result:** Naturally radiation-hardened without special processing.

---

## Space Missions Using 1802 Family

| Mission | Year | Processor | Status (2026) |
|---------|------|-----------|---------------|
| Voyager 1 | 1977 | 1802 | **Still running!** |
| Voyager 2 | 1977 | 1802 | **Still running!** |
| Galileo | 1989 | 1802 | Ended 2003 |
| Hubble | 1990 | 1802 | Operating |
| New Horizons | 2006 | 1805 | **8+ billion km away** |

The 1804 was used in various other space and military systems.

---

## Performance

| Metric | Value |
|--------|-------|
| Clock | 4-5 MHz |
| IPC | ~0.06 |
| MIPS | ~0.24 |

Not fast, but **reliable** - which matters more in space!

---

## Files

| File | Description |
|------|-------------|
| `rca_cdp1804_model.py` | Python implementation |
| `rca_cdp1804_model.json` | Configuration |
| `RCA_CDP1804_README.md` | This document |
| `QUICK_START_CDP1804.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The CDP1804: Space-proven reliability."*
