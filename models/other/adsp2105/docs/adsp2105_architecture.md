# Analog Devices ADSP-2105 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- Low-cost
- Fixed-point
- Single-cycle MAC

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Analog Devices |
| Year | 1992 |
| Clock | 20.0 MHz |
| Transistors | 200,000 |
| Data Width | 16-bit |
| Address Width | 14-bit |
| Technology | 0.6um CMOS |

## Description

Low-cost fixed-point DSP, consumer audio

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

- [Wikipedia](https://en.wikipedia.org/wiki/Analog_Devices_ADSP-2105)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
