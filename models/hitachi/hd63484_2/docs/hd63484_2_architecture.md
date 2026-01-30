# Hitachi HD63484-2 ACRTC Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- Enhanced ACRTC
- Hardware drawing
- Faster fill

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Hitachi |
| Year | 1987 |
| Clock | 10.0 MHz |
| Transistors | 120,000 |
| Data Width | 16-bit |
| Address Width | 20-bit |
| Technology | 1.0um CMOS |

## Description

Enhanced ACRTC, faster drawing commands

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 3.5
3. Primary bottleneck: drawing_engine
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Hitachi_HD63484-2_ACRTC)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
