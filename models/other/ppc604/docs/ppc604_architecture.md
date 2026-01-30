# PowerPC 604 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 4-issue superscalar
- 16KB I+D cache
- 6-stage pipeline

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Motorola/IBM |
| Year | 1994 |
| Clock | 133.0 MHz |
| Transistors | 3,600,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

High-performance PowerPC, 4-issue superscalar

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 0.8
3. Primary bottleneck: issue_width
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/PowerPC_604)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
