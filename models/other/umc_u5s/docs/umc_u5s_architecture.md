# UMC U5S Green CPU Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- 486-compatible
- 8KB cache
- Ultra low power

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | UMC |
| Year | 1994 |
| Clock | 40.0 MHz |
| Transistors | 1,200,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

Taiwanese 486 clone, super low power

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 1.9
3. Primary bottleneck: pipeline
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/UMC_U5S_Green_CPU)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
