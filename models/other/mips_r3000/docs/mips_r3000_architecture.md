# MIPS R3000 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 5-stage pipeline
- 32-bit RISC
- No on-chip cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MIPS |
| Year | 1988 |
| Clock | 33.0 MHz |
| Transistors | 120,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 1.2um CMOS |

## Description

32-bit RISC, 5-stage pipeline, SGI/DECstation, PS1 variant

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

- [Wikipedia](https://en.wikipedia.org/wiki/MIPS_R3000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
