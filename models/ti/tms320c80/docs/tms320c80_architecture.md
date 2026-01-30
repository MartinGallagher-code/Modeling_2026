# TI TMS320C80 MVP Architectural Documentation

## Era Classification

**Era:** Digital Signal Processor
**Period:** 1986-1994
**Queueing Model:** MAC-optimized datapath

## Architectural Features

- 5 processors on chip
- RISC master + 4 DSPs
- 2 Gops peak

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | TI |
| Year | 1994 |
| Clock | 50.0 MHz |
| Transistors | 4,000,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |
| Technology | 0.5um CMOS |

## Description

RISC master + 4 DSP cores, early media processor

## Model Implementation Notes

1. This processor uses the **Digital Signal Processor** architectural template
2. Target CPI: 0.8
3. Primary bottleneck: parallel_dsp
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/TI_TMS320C80_MVP)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
