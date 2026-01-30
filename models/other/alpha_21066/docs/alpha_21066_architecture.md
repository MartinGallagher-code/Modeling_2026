# DEC Alpha 21066 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- Alpha EV4 core
- Integrated PCI
- Low-cost Alpha PC

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | DEC |
| Year | 1993 |
| Clock | 166.0 MHz |
| Transistors | 1,750,000 |
| Data Width | 64-bit |
| Address Width | 64-bit |
| Technology | 0.675um CMOS |

## Description

Low-cost Alpha with integrated PCI/memory controller

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.3
3. Primary bottleneck: memory_controller
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/DEC_Alpha_21066)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
