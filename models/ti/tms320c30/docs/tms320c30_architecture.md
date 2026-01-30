# TI TMS320C30 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- 32-bit floating-point
- Dual bus
- 60ns cycle

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | TI |
| Year | 1988 |
| Clock | 33.3 MHz |
| Transistors | 500,000 |
| Data Width | 32-bit |
| Address Width | 24-bit |
| Technology | 0.8um CMOS |

## Description

First floating-point TMS320, audio and scientific

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.3
3. Primary bottleneck: memory_bandwidth
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/TI_TMS320C30)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
