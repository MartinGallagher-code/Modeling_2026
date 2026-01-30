# NexGen Nx586 Architectural Documentation

## Era Classification

**Era:** CISC/Microcoded
**Period:** 1986-1994
**Queueing Model:** Microcoded execution engine

## Architectural Features

- RISC86 core
- x86 translation
- Proprietary bus

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NexGen |
| Year | 1994 |
| Clock | 93.0 MHz |
| Transistors | 3,500,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.44um CMOS |

## Description

x86-compatible RISC core with x86 translation

## Model Implementation Notes

1. This processor uses the **CISC/Microcoded** architectural template
2. Target CPI: 1.3
3. Primary bottleneck: x86_translation
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/NexGen_Nx586)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
