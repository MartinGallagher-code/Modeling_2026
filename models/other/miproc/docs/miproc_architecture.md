# Plessey MIPROC Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1975)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- PDP-11 compatible 16-bit processor on a single chip
- Used in NATO cryptographic equipment
- Military and defense applications
- 16-bit data path with full PDP-11 instruction set
- Stack operations for subroutine support
- Sequential execution with no pipeline
- 5 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Plessey |
| Year | 1975 |
| Clock | 5.0 MHz |
| Transistors | ~8,000 |
| Data Width | 16-bit |
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
   - PDP-11 compatible instruction set gives predictable timing
   - ALU and data transfer at 3 cycles; memory at 6 cycles
   - I/O operations slowest at 7 cycles (device register access)
   - Control flow at 5 cycles; stack operations at 6 cycles
   - Target CPI of 5.0 reflects typical PDP-11 workload
   - Stage timing: fetch=2, decode=1, execute=2, memory=3
   - Crypto workload profile available for specialized validation

## Validation Approach

- Compare against original Plessey datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/plessey)
- [Wikipedia](https://en.wikipedia.org/wiki/Plessey)

---
Generated: 2026-01-29
