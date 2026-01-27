# TMS9900 CPU Queueing Model

## Executive Summary
The TMS9900 (1976) was Texas Instruments' 16-bit processor with a **unique "workspace" architecture** where registers live in RAM. It powered the TI-99/4A home computer (2.8 million sold).

## Technical Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| Word Size | 16-bit |
| Address | 15-bit (32KB) |
| Clock | 3 MHz |
| Registers | 16 (in RAM!) |

## The Workspace Concept
```
Instead of on-chip registers:
- R0-R15 are 16 words in RAM
- Workspace Pointer (WP) points to them
- Context switch = change WP

Advantage: Instant context switch
Disadvantage: Every register access hits RAM
```

## TI-99/4A (1981)
- TMS9900 @ 3 MHz
- 16KB RAM
- BASIC in ROM
- Sold 2.8 million units
- Lost to Commodore 64 in price war

## Unique Architecture
The only major CPU with registers in RAM. Innovative but slower for typical operations.

---
**Version:** 1.0 | **Date:** January 24, 2026
