# HP PA-7100 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- PA-RISC 1.1
- Multimedia
- External cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | HP |
| Year | 1992 |
| Clock | 100.0 MHz |
| Transistors | 850,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

Second-gen PA-RISC, multimedia instructions

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.2
3. Primary bottleneck: cache_miss
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/HP_PA-7100)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
