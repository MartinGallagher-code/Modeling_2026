# Ensoniq ES5503 DOC Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 32 independent digital oscillators (DOC = Digital Oscillator Chip)
- Wavetable synthesis from external RAM (up to 64KB per bank)
- Variable wavetable sizes: 256 bytes to 32K bytes per oscillator
- Hardware linear interpolation between sample points
- Per-oscillator volume control (8-bit)
- Per-oscillator frequency control (16-bit accumulator)
- Sample rate varies with number of active oscillators
  - 32 oscillators: ~26 kHz per oscillator
  - 1 oscillator: ~833 kHz
- Oscillator halt/interrupt mechanism for CPU synchronization
- 8 channels of audio output (4 stereo pairs)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ensoniq |
| Year | 1985 |
| Clock | 7.0 MHz |
| Transistors | ~40,000 |
| Data Width | 8-bit |
| Address Width | 16-bit (64K wavetable) |
| Package | DIP-40 |
| Technology | CMOS |

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
   - Interpolation is the most expensive operation (multi-point math)
   - Wavetable reads require external memory access (6 cycles)
   - Volume scaling is straightforward multiply (4 cycles)
   - Oscillator control includes halt detection and interrupt generation
   - Sample rate tradeoff: more oscillators = lower per-oscillator rate
   - Apple IIGS uses 15 of 32 oscillators for DOC sound

## Validation Approach

- Compare against Ensoniq DOC datasheet timing
- Validate with Apple IIGS and Ensoniq synth emulator cycle counts
- Target: <5% CPI prediction error

## References

- [Ensoniq ES5503 DOC Datasheet](TODO: Add link)
- [Apple IIGS Hardware Reference](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Ensoniq_ES5503)

---
Generated: 2026-01-29
