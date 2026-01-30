# AT&T DSP16 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- 16-bit
- Low power
- Voice processing

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AT&T |
| Year | 1987 |
| Clock | 25.0 MHz |
| Transistors | 150,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | 1.0um CMOS |

## Description

16-bit fixed-point, low-power, modems/voice

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.3
3. Primary bottleneck: mac_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/AT&T_DSP16)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
