# AMD Am386 Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- 386-compatible
- 40 MHz
- No on-chip cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AMD |
| Year | 1991 |
| Clock | 40.0 MHz |
| Transistors | 275,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 1.0um CMOS |

## Description

AMD's 386 clone, 40 MHz (faster than Intel's 33 MHz)

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 4.0
3. Primary bottleneck: no_cache
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/AMD_Am386)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
