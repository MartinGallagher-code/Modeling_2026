# HP PA-7100LC Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- On-chip cache
- Memory controller
- Low cost

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | HP |
| Year | 1994 |
| Clock | 100.0 MHz |
| Transistors | 900,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

Low-cost PA-RISC with on-chip cache/memory controller

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.4
3. Primary bottleneck: pipeline_stall
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/HP_PA-7100LC)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
