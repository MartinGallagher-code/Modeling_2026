# National Semiconductor NSC800 Queueing Model

## Z80-Compatible with CMOS and 8080 Pinout (1979)

The NSC800 was National Semiconductor's Z80-compatible processor, featuring CMOS technology and an 8080-like pinout.

---

## Executive Summary

| Spec | Z80 | NSC800 |
|------|-----|--------|
| Instructions | Z80 | **Z80 (compatible!)** |
| Process | NMOS | **CMOS** |
| Pinout | Z80 | **8080-like** |
| Clock | Two-phase | **Single-phase** |
| Static | No | **Yes** |

---

## Why a Different Pinout?

National Semiconductor chose an **8080-like pinout** because:

1. Many engineers familiar with 8080 systems
2. Could reuse 8080 support chip designs
3. Differentiated from Zilog's Z80
4. Better bus timing signals for some applications

**Trade-off:** Not a drop-in Z80 replacement.

---

## CMOS Advantages

| Feature | Benefit |
|---------|---------|
| Lower power | Battery applications |
| Static design | Can stop clock to save power |
| Single-phase clock | Simpler clock generation |
| Lower voltage | 3V operation possible |

---

## Z80 Clone Market

The NSC800 was one of many Z80 clones:

| Company | Chip | Notes |
|---------|------|-------|
| Zilog | Z80 | Original |
| **NSC** | **NSC800** | **CMOS, 8080 pinout** |
| NEC | μPD780 | Direct clone |
| Sharp | LH0080 | Direct clone |
| SGS | Z80 | Second source |
| Mostek | MK3880 | Second source |

This shows how successful the Z80 architecture was!

---

## Applications

The NSC800 was popular in:

- **Battery-powered devices** (CMOS = low power)
- **Military/aerospace** (radiation tolerance)
- **Industrial control** (static design = reliable)
- **Portable computers** (power efficiency)

---

## Performance

| Metric | Value |
|--------|-------|
| Clock | 4 MHz |
| IPC | ~0.08 |
| MIPS | ~0.32 |

Similar to Z80 - the value was in CMOS, not speed.

---

## Files

| File | Description |
|------|-------------|
| `nsc_nsc800_model.py` | Python implementation |
| `nsc_nsc800_model.json` | Configuration |
| `NSC_NSC800_README.md` | This document |
| `QUICK_START_NSC800.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

---

**Version:** 1.0 | **Date:** January 25, 2026

*"The NSC800: Z80 software, CMOS efficiency."*
