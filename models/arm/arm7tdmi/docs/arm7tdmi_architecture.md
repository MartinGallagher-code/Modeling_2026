# ARM7TDMI Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 3-stage pipeline
- Thumb 16-bit mode
- Hardware debug

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | ARM |
| Year | 1994 |
| Clock | 40.0 MHz |
| Transistors | 74,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

Thumb mode, hardware debug, dominant embedded core

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: pipeline_stall
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/ARM7TDMI)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
