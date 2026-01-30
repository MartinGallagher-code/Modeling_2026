# GI SP0256 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1981)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Dedicated speech synthesis processor using LPC (Linear Predictive Coding)
- 64 allophone ROM for English speech synthesis
- 8-bit data path with 16-bit address bus
- On-chip excitation generator for voice synthesis
- LPC filter coefficient update engine
- Audio output DAC interface
- Used in Mattel Intellivoice speech module
- 3.12 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1981 |
| Clock | 3.12 MHz |
| Transistors | ~10,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |

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
   - Not a general-purpose CPU -- dedicated speech synthesis engine
   - Allophone fetch from ROM averages 8 cycles
   - LPC filter coefficient updates are compute-intensive (10 cycles)
   - Excitation generation averages 8 cycles
   - Audio output is the most expensive operation (14 cycles)
   - Real-time audio constraints drive the execution model
   - Pipeline-like operation between allophone processing stages

## Validation Approach

- Compare against original GI datasheet timing
- Validate with Intellivision emulator speech timing
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/general_instrument/sp0256)
- [Wikipedia](https://en.wikipedia.org/wiki/General_Instrument_SP0256)

---
Generated: 2026-01-29
