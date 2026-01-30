# TI SN76489 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1980)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 3 square wave tone generators with 10-bit frequency dividers
- 1 noise generator (white or periodic noise)
  - 3 frequency options: N/512, N/1024, N/2048, or channel 3's frequency
- 4-bit attenuation per channel (2 dB steps, 0 to -28 dB + off)
- No envelope generator (CPU must handle volume changes)
- Simple write-only register interface (latch byte + data byte)
- Single 8-bit data bus input

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1980 |
| Clock | 4.0 MHz (internally /16 = 250 kHz) |
| Transistors | ~4,000 |
| Data Width | 8-bit |
| Address Width | 3-bit (8 registers) |
| Package | DIP-16 |
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
   - Very simple chip with only ~4000 transistors
   - No envelope generator means CPU overhead for volume effects
   - Tone generators are simple countdown timers
   - Noise LFSR can be clocked from channel 3 for variable noise pitch
   - Write-only interface (no register readback)
   - Internal clock is input/16

## Validation Approach

- Compare against TI datasheet timing specifications
- Validate with Sega Master System emulator cycle counts
- Target: <5% CPI prediction error

## References

- [TI SN76489 Datasheet](TODO: Add link)
- [Sega Master System Technical Manual](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Texas_Instruments_SN76489)

---
Generated: 2026-01-29
