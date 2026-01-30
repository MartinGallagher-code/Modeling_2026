# Intel i960 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- Register scoreboarding
- 32-bit RISC
- Local register cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1988 |
| Clock | 33.0 MHz |
| Transistors | 250,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 1.0um CMOS |

## Description

32-bit embedded RISC, register scoreboarding

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: register_scoreboard
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Intel_i960)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
