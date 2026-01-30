# ATI Mach32 Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- GUI acceleration
- Hardware cursor
- PCI support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | ATI |
| Year | 1992 |
| Clock | 44.0 MHz |
| Transistors | 600,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

ATI's first true graphics coprocessor

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 1.8
3. Primary bottleneck: pixel_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/ATI_Mach32)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
