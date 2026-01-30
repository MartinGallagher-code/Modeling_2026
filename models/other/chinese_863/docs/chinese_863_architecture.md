# Chinese 863 Program CPU Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- Chinese 863 Program
- Reverse-engineered
- Research CPU

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | ICTS |
| Year | 1990 |
| Clock | 8.0 MHz |
| Transistors | 100,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | 2.0um CMOS |

## Description

Early Chinese CPU R&D, reverse-engineered Z80/8086 cores

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 4.5
3. Primary bottleneck: microcode
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Chinese_863_Program_CPU)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
