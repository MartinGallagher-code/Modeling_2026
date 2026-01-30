# IIT AGX Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- XGA compatible
- GUI acceleration
- VRAM support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | IIT |
| Year | 1993 |
| Clock | 50.0 MHz |
| Transistors | 400,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.6um CMOS |

## Description

XGA-compatible graphics accelerator

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 2.2
3. Primary bottleneck: pixel_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/IIT_AGX)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
