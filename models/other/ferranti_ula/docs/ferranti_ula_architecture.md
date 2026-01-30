# Ferranti ULA Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1981)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Uncommitted Logic Array (ULA) for ZX Spectrum computer
- Memory controller with bus arbitration
- Video signal generation from display RAM
- I/O port decoding
- Bus contention management between CPU and video
- Custom gate array (not a general-purpose processor)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ferranti |
| Year | 1981 |
| Clock | 3.5 MHz |
| Transistors | 5,000 |
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
   - Not a CPU but a support chip for memory/video/IO management
   - Memory control operations at 4 cycles (bus arbitration)
   - Video generation and I/O decode at 5 cycles each
   - Bus contention is the most expensive operation at 6 cycles
   - Contention occurs when CPU and video access same memory bank
   - Video generation and I/O decode dominate workload (30% each)

## Validation Approach

- Compare against original Ferranti ULA specifications
- Validate with ZX Spectrum timing analysis and contention patterns
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/ZX_Spectrum_ULA)

---
Generated: 2026-01-29
