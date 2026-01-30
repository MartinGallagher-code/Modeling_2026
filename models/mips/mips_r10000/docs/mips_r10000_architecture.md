# SGI R10000 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 4-issue out-of-order
- Register renaming
- 32KB I+D

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MIPS/SGI |
| Year | 1994 |
| Clock | 200.0 MHz |
| Transistors | 6,800,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.35um CMOS |

## Description

Out-of-order MIPS, register renaming

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 0.6
3. Primary bottleneck: issue_width
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/SGI_R10000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
