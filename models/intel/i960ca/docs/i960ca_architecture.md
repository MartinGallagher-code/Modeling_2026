# Intel i960CA Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 3-issue superscalar
- 1KB I-cache
- Register scoreboard

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1989 |
| Clock | 33.0 MHz |
| Transistors | 600,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

Superscalar i960, 3-issue, RAID controller standard

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

- [Wikipedia](https://en.wikipedia.org/wiki/Intel_i960CA)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
