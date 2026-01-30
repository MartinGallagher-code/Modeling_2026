# SGS-Thomson D950 Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- GSM baseband
- European design
- Viterbi support

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | SGS-Thomson |
| Year | 1991 |
| Clock | 20.0 MHz |
| Transistors | 250,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | 0.8um CMOS |

## Description

European DSP for GSM baseband processing

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 1.4
3. Primary bottleneck: mac_throughput
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/SGS-Thomson_D950)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
