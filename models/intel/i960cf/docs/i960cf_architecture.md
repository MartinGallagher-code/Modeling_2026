# Intel i960CF Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- On-chip FPU
- 4KB I-cache
- Superscalar

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1992 |
| Clock | 33.0 MHz |
| Transistors | 900,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

Enhanced i960 with on-chip FPU

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 0.85
3. Primary bottleneck: issue_width
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Intel_i960CF)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
