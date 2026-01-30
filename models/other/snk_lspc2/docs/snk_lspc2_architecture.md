# SNK LSPC2-A2 Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- 380 sprites on screen
- Hardware scaling
- Arcade standard

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | SNK |
| Year | 1990 |
| Clock | 24.0 MHz |
| Transistors | 200,000 |
| Data Width | 16-bit |
| Address Width | 24-bit |
| Technology | 0.8um CMOS |

## Description

Neo Geo video processor, hardware sprite scaler

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 2.5
3. Primary bottleneck: sprite_engine
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/SNK_LSPC2-A2)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
