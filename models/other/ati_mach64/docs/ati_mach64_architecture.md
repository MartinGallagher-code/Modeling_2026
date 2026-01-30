# ATI Mach64 Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- Video playback
- 2D + video
- PCI bus master

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | ATI |
| Year | 1994 |
| Clock | 66.0 MHz |
| Transistors | 1,000,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

Hardware video playback, foundation for Rage line

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: pixel_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/ATI_Mach64)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
