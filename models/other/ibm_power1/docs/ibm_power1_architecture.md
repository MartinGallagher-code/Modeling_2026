# IBM POWER1 Architectural Documentation

## Era Classification

**Era:** RISC/Superscalar
**Period:** 1986-1994
**Queueing Model:** Pipeline + cache hierarchy

## Architectural Features

- Multi-chip design
- Branch processor
- FXU+FPU+BRU

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | IBM |
| Year | 1990 |
| Clock | 25.0 MHz |
| Transistors | 6,900,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 1.0um CMOS |

## Description

Original POWER architecture, RS/6000, foundation of PowerPC

## Model Implementation Notes

1. This processor uses the **RISC/Superscalar** architectural template
2. Target CPI: 1.4
3. Primary bottleneck: branch_unit
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/IBM_POWER1)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
