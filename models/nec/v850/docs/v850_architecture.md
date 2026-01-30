# NEC V850 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 5-stage pipeline
- On-chip ROM/RAM
- Automotive grade

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1994 |
| Clock | 20.0 MHz |
| Transistors | 450,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.35um CMOS |

## Description

Embedded RISC for automotive ECUs

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

- [Wikipedia](https://en.wikipedia.org/wiki/NEC_V850)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
