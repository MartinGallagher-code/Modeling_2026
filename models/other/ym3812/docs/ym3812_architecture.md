# Yamaha YM3812 OPL2 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 9 channels with 2 operators each (18 total FM operators)
- 4 selectable waveforms per operator:
  - Sine, half-sine, absolute sine, quarter-sine
- Enhanced rhythm mode (5 percussion instruments)
- Backward compatible with YM3526 (OPL) register layout
- Mono output (stereo via YM3812 + DAC or OPL3)
- Timer A (10-bit) and Timer B (8-bit)
- CSM speech synthesis mode

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1985 |
| Clock | 3.58 MHz |
| Transistors | ~18,000 |
| Data Width | 8-bit |
| Address Width | 8-bit |
| Package | DIP-24 |
| Technology | NMOS |

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
   - 6 categories needed (vs 5 for OPL) due to waveform selection logic
   - Waveform shaping adds a distinct processing stage
   - Rhythm mode is slightly more efficient than OPL's
   - Register layout is backward compatible with YM3526
   - The AdLib card and Sound Blaster both use this chip

## Validation Approach

- Compare against Yamaha application manual timing
- Validate with AdLib/Sound Blaster emulator cycle counts
- Target: <5% CPI prediction error

## References

- [Yamaha YM3812 Application Manual](TODO: Add link)
- [AdLib Technical Reference](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Yamaha_OPL#OPL2)

---
Generated: 2026-01-29
