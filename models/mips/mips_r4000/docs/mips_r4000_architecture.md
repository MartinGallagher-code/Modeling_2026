# MIPS R4000 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 8-stage superpipeline
- 64-bit
- On-chip caches

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MIPS |
| Year | 1991 |
| Clock | 100.0 MHz |
| Transistors | 1,350,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.8um CMOS |

## Description

First commercial 64-bit RISC, 8-stage superpipeline

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: superpipeline_hazard
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/MIPS_R4000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
