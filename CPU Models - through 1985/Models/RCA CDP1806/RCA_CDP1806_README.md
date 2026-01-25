# RCA CDP1806 Queueing Model

## THE FINAL COSMAC (1985)

The CDP1806 is the ultimate evolution of RCA's COSMAC family - the radiation-hardened processors that power spacecraft from Voyager to New Horizons.

---

## COSMAC Family Evolution

```
CDP1802 (1976) - Original
    │   46 instructions, no RAM
    │   Voyager 1 & 2, Galileo
    │
    ▼
CDP1804 (1980) - Enhanced
    │   64B RAM, timer added
    │   75 instructions
    │
    ▼
CDP1805 (1984) - Further enhanced
    │   More instructions (83)
    │   New Horizons probe
    │
    ▼
CDP1806 (1985) - FINAL ← THIS CHIP
        128B RAM, 91 instructions
        All enhancements combined
```

---

## CDP1806 Specifications

| Feature | CDP1802 | CDP1806 |
|---------|---------|---------|
| Year | 1976 | 1985 |
| On-chip RAM | None | **128 bytes** |
| Instructions | 46 | **91** |
| Timer | None | **Enhanced** |
| Clock | 2 MHz | **8 MHz** |

---

## Space Heritage

The COSMAC family is **still flying**:

| Mission | Launch | Processor | Status (2026) |
|---------|--------|-----------|---------------|
| Voyager 1 | 1977 | 1802 | **Still running!** |
| Voyager 2 | 1977 | 1802 | **Still running!** |
| Galileo | 1989 | 1802 | Ended 2003 |
| Hubble | 1990 | 1802+ | **Operating** |
| New Horizons | 2006 | 1805 | **8+ billion km!** |

---

## Why Silicon-on-Sapphire?

```
Regular Silicon:              Silicon-on-Sapphire:
┌─────────────────┐          ┌─────────────────┐
│    Silicon      │          │    Silicon      │
├─────────────────┤          ├─────────────────┤
│    Silicon      │          │    SAPPHIRE     │ ← Insulator!
│    Substrate    │          │    Substrate    │
└─────────────────┘          └─────────────────┘
        │                            │
  Radiation causes            Radiation CANNOT
  latch-up (fatal)           cause latch-up
```

The sapphire substrate isolates each transistor, preventing radiation-induced latch-up.

---

## Corporate Journey

```
RCA (1976) ─── Creates COSMAC
    │
    ▼
GE (1986) ─── Acquires RCA
    │
    ▼
Harris (1988) ─── Acquires RCA Solid State
    │
    ▼
Intersil (1999) ─── Spun off from Harris
    │
    ▼
Renesas (2017) ─── Acquires Intersil
    │
COSMAC STILL SUPPORTED!
```

---

## Still Available

Radiation-hardened versions of COSMAC chips are **still manufactured** for space and military applications. The 1806 represents the culmination of the family's development.

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The CDP1806: COSMAC perfected."*
