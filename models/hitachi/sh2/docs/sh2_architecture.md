# Hitachi SH-2 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 5-stage pipeline
- Hardware multiply
- Sega Saturn CPU

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1994 |
| Clock | 28.6 MHz |
| Transistors | 700,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

Dual SH-2 in Sega Saturn, 5-stage pipeline

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.3
3. Primary bottleneck: pipeline_stall
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Hitachi_SH-2)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
