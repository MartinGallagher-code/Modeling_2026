# Ensoniq OTTO (ES5505) Architectural Documentation

## Era Classification

**Era:** Sound Processor
**Period:** 1986-1994
**Queueing Model:** Waveform generation engine

## Architectural Features

- 32 voices
- Wavetable synthesis
- 16-bit output

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ensoniq |
| Year | 1991 |
| Clock | 16.0 MHz |
| Transistors | 250,000 |
| Data Width | 16-bit |
| Address Width | 21-bit |
| Technology | 0.8um CMOS |

## Description

32-voice wavetable, Gravis Ultrasound / Taito F3

## Model Implementation Notes

1. This processor uses the **Sound Processor** architectural template
2. Target CPI: 2.2
3. Primary bottleneck: sample_fetch
4. 6 instruction categories modeled

## Validation Approach

- Compare against datasheet instruction timings
- Validate with published benchmark results where available
- Target: <5% CPI prediction error

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Ensoniq_OTTO_(ES5505))
- Manufacturer datasheet (where available)

---
Generated: 2026-01-30
