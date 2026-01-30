# NEC uPD7759 Architectural Documentation

## Era Classification

**Era:** Sound Processor
**Period:** 1986-1994
**Queueing Model:** Waveform generation engine

## Architectural Features

- ADPCM decoding
- Speech synthesis
- Arcade standard

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1987 |
| Clock | 5.0 MHz |
| Transistors | 80,000 |
| Data Width | 8-bit |
| Address Width | 17-bit |
| Technology | 1.0um CMOS |

## Description

ADPCM voice synthesis for arcade games

## Model Implementation Notes

1. This processor uses the **Sound Processor** architectural template
2. Target CPI: 3.0
3. Primary bottleneck: sample_decode
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/NEC_uPD7759)
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
