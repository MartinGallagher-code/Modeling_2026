# Yamaha YM2151 OPM Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 8 channels with 4 operators each (32 total FM operators)
- 4-operator FM synthesis with 8 configurable algorithms
- Hardware LFO with 4 waveforms (sine, square, sawtooth, noise)
- Per-channel stereo output (L/R panning)
- Programmable ADSR envelope per operator
- Key scaling for natural instrument response
- Timer A (10-bit) and Timer B (8-bit) for sequencing
- IRQ output for CPU synchronization

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Yamaha |
| Year | 1983 |
| Clock | 3.58 MHz |
| Transistors | ~20,000 |
| Data Width | 8-bit |
| Address Width | 8-bit (256 registers) |
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
   - FM operator computation dominates cycle budget (32 operators per sample)
   - Each operator performs sine table lookup + phase modulation
   - 8 algorithms define operator routing (serial, parallel, mixed)
   - LFO modulates pitch and amplitude globally
   - Stereo output requires per-channel L/R routing

## Validation Approach

- Compare against Yamaha application manual timing
- Validate with arcade game emulator cycle counts
- Target: <5% CPI prediction error

## References

- [Yamaha YM2151 Application Manual](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Yamaha_YM2151)
- [MAME Source](https://github.com/mamedev/mame/blob/master/src/devices/sound/ym2151.cpp)

---
Generated: 2026-01-29
