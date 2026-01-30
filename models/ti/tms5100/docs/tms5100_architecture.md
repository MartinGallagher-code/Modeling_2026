# TI TMS5100 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s Dedicated Speech Synthesis Processor
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Dedicated speech synthesis processor (Speak & Spell)
- LPC (Linear Predictive Coding) speech synthesis engine
- 8-bit data path for coefficient processing
- Lattice filter architecture for vocal tract modeling
- On-chip DAC (Digital-to-Analog Converter) for audio output
- Excitation generator (voiced/unvoiced/silence)
- Serial ROM interface for speech data storage

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1978 |
| Clock | 0.16 MHz (160 kHz) |
| Transistors | 8,000 |
| Data Width | 8-bit |
| Address Width | 14-bit |

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

Target CPI: 8.0 (typical speech synthesis workload)

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| LPC Decode | 6 | LPC parameter decoding (5-7 cycles) |
| Lattice Filter | 10 | Lattice filter computation (8-12 cycles) |
| Excitation | 6 | Excitation generation (5-7 cycles) |
| DAC | 10 | DAC output and conversion (8-12 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - This is a dedicated-function processor, not a general-purpose CPU
   - The instruction categories map to speech synthesis pipeline stages rather than traditional CPU operations
   - Lattice filter and DAC operations are the most expensive at 10 cycles each
   - LPC decode and excitation generation are lighter at 6 cycles each
   - The typical workload distributes equally across all four stages (25% each), yielding CPI = 8.0
   - Real-time speech output at ~8 kHz sample rate constrains the processing budget
   - The 160 kHz clock is very slow but sufficient for the dedicated speech synthesis task

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/tms5100)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_LPC_Speech_Chips)

---
Generated: 2026-01-29
