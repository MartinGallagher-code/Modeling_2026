# Analog Devices ADSP-21020 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- IEEE float
- SHARC predecessor
- Multi-function

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Analog Devices |
| Year | 1990 |
| Clock | 33.0 MHz |
| Transistors | 450,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.8um CMOS |

## Description

32-bit floating-point SHARC predecessor

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.2
3. Primary bottleneck: memory_bandwidth
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Analog_Devices_ADSP-21020)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
