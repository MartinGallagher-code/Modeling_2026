# OKI MSM5205 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit ADPCM (Adaptive Differential Pulse-Code Modulation) speech synthesis processor
- Specialized for voice and sound output in arcade games
- 384 kHz clock
- ADPCM decode, reconstruction filter, and DAC output stages
- Sample sequencing control
- Widely used in arcade game hardware for voice effects

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI |
| Year | 1983 |
| Clock | 0.384 MHz |
| Transistors | ~3,000 |
| Data Width | 4-bit |
| Address Width | 12-bit |

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
   - Specialized DSP-like architecture for ADPCM speech synthesis
   - ADPCM decode at 3.0 cycles; reconstruction filter at 4.0 cycles
   - DAC output at 4.0 cycles; sample sequencing control at 5.0 cycles
   - Instruction categories reflect audio pipeline stages rather than general CPU ops
   - Low clock (384 kHz) sufficient for audio sample rates
   - 4-bit ADPCM input produces analog audio output

## Validation Approach

- Compare against original OKI datasheet
- Validate with arcade hardware emulator audio timing
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/oki)
- [Wikipedia](https://en.wikipedia.org/wiki/Oki_MSM5205)

---
Generated: 2026-01-29
