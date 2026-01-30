# DEC Alpha 21064A Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 2-issue
- 16KB I+D cache
- 300 MHz

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | DEC |
| Year | 1994 |
| Clock | 300.0 MHz |
| Transistors | 2,850,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.5um CMOS |

## Description

Faster 21064, 300 MHz

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.2
3. Primary bottleneck: pipeline_stall
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/DEC_Alpha_21064A)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
