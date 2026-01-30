# IBM RS64 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- POWER convergence
- 64-bit
- AS/400 target

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | IBM |
| Year | 1994 |
| Clock | 135.0 MHz |
| Transistors | 8,000,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.35um CMOS |

## Description

POWER/PowerPC convergence, AS/400 transition

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 0.7
3. Primary bottleneck: issue_width
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/IBM_RS64)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
