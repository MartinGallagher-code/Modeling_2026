# Weitek P9000 Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- High-end 2D
- Quad-pixel ops
- NeXT Color

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Weitek |
| Year | 1991 |
| Clock | 40.0 MHz |
| Transistors | 500,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

High-end 2D coprocessor, Diamond Viper/NeXT

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

- [Wikipedia](https://en.wikipedia.org/wiki/Weitek_P9000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
