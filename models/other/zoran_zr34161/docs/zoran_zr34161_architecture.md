# Zoran ZR34161 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- JPEG/MPEG decode
- DCT engine
- Digital imaging

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zoran |
| Year | 1991 |
| Clock | 25.0 MHz |
| Transistors | 300,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | 0.8um CMOS |

## Description

JPEG/MPEG decoder DSP, early digital imaging

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: codec_pipeline
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Zoran_ZR34161)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
