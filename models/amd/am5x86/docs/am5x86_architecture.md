# AMD Am5x86 Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- 4x clock multiplier
- 16KB write-back cache
- Pentium-class

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AMD |
| Year | 1995 |
| Clock | 133.0 MHz |
| Transistors | 1,600,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.35um CMOS |

## Description

486 with 4x clock, Pentium-class performance

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 1.6
3. Primary bottleneck: pipeline
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/AMD_Am5x86)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
