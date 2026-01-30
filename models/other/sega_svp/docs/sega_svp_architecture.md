# Sega SVP (SSP1601) Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- Samsung SSP1601
- 16-bit DSP
- In-cartridge

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Samsung |
| Year | 1994 |
| Clock | 23.0 MHz |
| Transistors | 100,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | 0.6um CMOS |

## Description

DSP in Virtua Racing cartridge

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.5
3. Primary bottleneck: mac_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Sega_SVP_(SSP1601))
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
