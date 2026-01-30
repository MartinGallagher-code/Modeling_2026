# HP PA-7200 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- Dual-issue superscalar
- PA-RISC 1.1
- Alchemist

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | HP |
| Year | 1994 |
| Clock | 140.0 MHz |
| Transistors | 1,260,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

Superscalar PA-RISC, dual-issue

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 0.9
3. Primary bottleneck: issue_width
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/HP_PA-7200)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
