# Hitachi SH-1 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 16-bit instruction encoding
- 5-stage pipeline
- Compact ISA

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1992 |
| Clock | 20.0 MHz |
| Transistors | 400,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

32-bit RISC for embedded, 16-bit compressed ISA

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

- [Wikipedia](https://en.wikipedia.org/wiki/Hitachi_SH-1)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
