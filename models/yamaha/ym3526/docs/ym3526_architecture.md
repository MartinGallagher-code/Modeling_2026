# Yamaha YM3526 OPL Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1984)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 9 channels with 2 operators each (18 total FM operators)
- 2-operator FM synthesis (simpler than YM2151's 4-op)
- Rhythm mode: converts 3 channels into 5 percussion instruments
  - Bass drum, snare drum, tom-tom, cymbal, hi-hat
- Sine waveform only (no waveform selection)
- Mono output
- Timer A (10-bit) and Timer B (8-bit)
- CSM speech synthesis mode

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1984 |
| Clock | 3.58 MHz |
| Transistors | ~15,000 |
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
   - 2-operator FM is simpler than 4-op, reducing operator cycle count
   - Rhythm mode adds significant complexity (converts melodic to percussion)
   - Sine-only waveform simplifies operator computation vs OPL2
   - CSM mode uses all channels for speech synthesis via rapid key-on/off

## Validation Approach

- Compare against Yamaha application manual timing
- Validate with arcade game emulator cycle counts
- Target: <5% CPI prediction error

## References

- [Yamaha YM3526 Application Manual](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Yamaha_OPL)

---
Generated: 2026-01-29
