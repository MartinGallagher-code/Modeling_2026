# Atari POKEY Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1979)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-channel audio synthesis engine
- Serial I/O port for cassette and SIO bus
- Pseudo-random number generator (PRNG)
- Keyboard scanning controller
- Timer/counter functionality
- 8-bit data path with 4-bit address space
- Dedicated audio/I/O controller (not a general-purpose CPU)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Atari |
| Year | 1979 |
| Clock | 1.79 MHz |
| Transistors | ~5,000 |
| Data Width | 8-bit |
| Address Width | 4-bit |

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
   - POKEY is an I/O controller, not a general-purpose CPU
   - Audio generation and timer operations dominate the workload
   - Serial I/O operations have higher latency (4 cycles avg)
   - Keyboard scanning adds periodic overhead
   - Operates synchronously with Atari 800 system bus at 1.79 MHz

## Validation Approach

- Compare against original Atari datasheet timing
- Validate with Atari 800 emulator cycle counts
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/atari/pokey)
- [Wikipedia](https://en.wikipedia.org/wiki/POKEY)

---
Generated: 2026-01-29
