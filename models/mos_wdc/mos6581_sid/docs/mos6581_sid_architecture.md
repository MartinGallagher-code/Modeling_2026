# MOS 6581 SID Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1982)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 3 independent oscillators with 4 waveforms (sawtooth, triangle, pulse, noise)
- Programmable multi-mode resonant filter (lowpass, bandpass, highpass, notch)
- 3 independent ADSR envelope generators
- Ring modulation between voices 1-3 and 3-1
- Oscillator sync (hard sync between adjacent voices)
- External audio input with filter routing
- 29 write-only registers, 4 read-only registers
- 8-bit data bus, active-low chip select

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology |
| Year | 1982 |
| Clock | 1.0 MHz |
| Transistors | ~11,500 |
| Data Width | 8-bit |
| Address Width | 5-bit (32 registers) |
| Package | DIP-28 |
| Technology | NMOS |
| Supply Voltage | 12V |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  FETCH  │──►│ DECODE  │──►│ EXECUTE │──►│ MEMORY  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue

CPI = Fetch + Decode + Execute + Memory (serial sum)
```

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - SID is a dedicated audio synthesis chip, not a general-purpose CPU
   - Voice mixing is the most expensive operation (analog summation)
   - Filter is analog and varies between individual chips
   - Oscillator operations include waveform generation and frequency accumulation
   - ADSR envelopes use rate counters with exponential decay curves

## Validation Approach

- Compare against original MOS Technology timing specifications
- Validate with C64 SID player cycle counts
- Target: <5% CPI prediction error

## References

- [MOS 6581 SID Datasheet](TODO: Add link)
- [C64 Programmer's Reference Guide](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6581)

---
Generated: 2026-01-29
