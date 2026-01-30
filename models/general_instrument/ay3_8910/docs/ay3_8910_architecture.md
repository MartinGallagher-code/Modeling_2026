# GI AY-3-8910 PSG Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 3 square wave tone generators with 12-bit frequency dividers
- 1 noise generator with 5-bit period control (LFSR)
- 1 shared envelope generator with 16 envelope shapes
- Per-channel mixer with independent tone/noise enable
- 2 general-purpose 8-bit I/O ports (active-high)
- 16 registers accessed via address/data bus protocol
- Clock input divided by 16 for internal tone generator clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1978 |
| Clock | 1.79 MHz |
| Transistors | ~5,000 |
| Data Width | 8-bit |
| Address Width | 4-bit (16 registers) |
| Package | DIP-40 |
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
   - Only 1 envelope generator shared across all 3 channels (major limitation)
   - Tone generators are simple 12-bit countdown timers
   - Noise generator uses linear feedback shift register
   - I/O ports are general-purpose, used for joysticks/keyboard in many systems
   - Variants: 8912 (1 I/O port, DIP-28), 8913 (no I/O ports, DIP-24)

## Validation Approach

- Compare against GI datasheet timing specifications
- Validate with ZX Spectrum/MSX emulator cycle counts
- Target: <5% CPI prediction error

## References

- [GI AY-3-8910 Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/General_Instrument_AY-3-8910)

---
Generated: 2026-01-29
