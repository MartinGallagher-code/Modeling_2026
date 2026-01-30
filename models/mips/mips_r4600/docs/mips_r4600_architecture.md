# MIPS R4600 Orion Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- 5-stage pipeline
- 64-bit
- Low-cost design

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | QED/IDT |
| Year | 1994 |
| Clock | 133.0 MHz |
| Transistors | 1,900,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.64um CMOS |

## Description

Low-cost R4000 derivative, Cisco routers

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

- [Wikipedia](https://en.wikipedia.org/wiki/MIPS_R4600_Orion)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
