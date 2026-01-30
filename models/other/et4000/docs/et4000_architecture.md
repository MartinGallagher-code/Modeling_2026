# Tseng Labs ET4000 Architectural Documentation

## Era Classification

**Era:** Graphics Processor
**Period:** 1986-1994
**Queueing Model:** Pixel/drawing pipeline

## Architectural Features

- SVGA controller
- Hardware acceleration
- ISA/VLB

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Tseng Labs |
| Year | 1989 |
| Clock | 40.0 MHz |
| Transistors | 250,000 |
| Data Width | 32-bit |
| Address Width | 22-bit |
| Technology | 0.8um CMOS |

## Description

Fast SVGA with hardware acceleration

## Model Implementation Notes

1. This processor uses the **Graphics Processor** architectural template
2. Target CPI: 2.5
3. Primary bottleneck: bus_bandwidth
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Tseng_Labs_ET4000)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
