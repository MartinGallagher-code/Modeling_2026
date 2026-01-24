# Motorola 6805 CPU Queueing Model

## Executive Summary
The Motorola 6805 (1979) is one of the **most successful microcontroller families ever**. Billions of units shipped. Its secret: extreme simplicity and low cost. Only 3 registers, but enough to control everything from car door locks to TV remotes.

## Technical Specifications
| Spec | Value |
|------|-------|
| Year | 1979 |
| Registers | **Only 3** (A, X, SP) |
| Address | 8 KB max |
| ROM | 112B to 8KB |
| RAM | 64 to 256 bytes |

## Minimalist Architecture
```
A:  8-bit Accumulator
X:  8-bit Index Register
SP: 5-bit Stack Pointer (32 bytes max!)
PC: 13-bit Program Counter

That's it! Enough for most MCU tasks.
```

## Why So Successful?
1. **Extremely low cost** - Pennies per chip
2. **Simple to program** - Minimal instruction set
3. **Hundreds of variants** - Right chip for every application
4. **Reliable** - Proven architecture

## Applications (Billions!)
- Automotive (door locks, windows, seats)
- Appliances (washers, microwaves)
- Toys and games
- Remote controls
- Sensors

## Evolution
6805 → 68HC05 → 68HC08 → HCS08 (still produced)

---
**Version:** 1.0 | **Date:** January 24, 2026
