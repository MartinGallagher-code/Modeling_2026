# Signetics 2636 PVI Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1977)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Programmable Video Interface (PVI) with built-in CPU
- 8-bit data path with 12-bit address space
- Video rendering with hardware collision detection
- Designed for game console applications (Arcadia 2001)
- Integrated video generation and sprite handling
- 3.58 MHz clock (NTSC color burst frequency)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Signetics |
| Year | 1977 |
| Clock | 3.58 MHz |
| Transistors | ~5,000 |
| Data Width | 8-bit |
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
   - Combined CPU and video controller on single chip
   - Collision detection operations are compute-intensive (5.5 cycles avg)
   - Control flow operations are the most expensive (6 cycles)
   - Video rendering operations average 5 cycles
   - Basic ALU operations are fastest at 4 cycles
   - Clock derived from NTSC color burst for video sync

## Validation Approach

- Compare against original Signetics datasheet timing
- Validate with Arcadia 2001 emulator cycle counts
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/signetics/2636)
- [Wikipedia](https://en.wikipedia.org/wiki/Signetics_2636)

---
Generated: 2026-01-29
