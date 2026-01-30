# Mostek 3870 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1977)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- F8-compatible single-chip microcontroller
- 8-bit data bus
- On-chip RAM, ROM, I/O, and timer
- Faster than the original Fairchild F8 multi-chip design
- 64-byte scratchpad RAM
- 4-20 cycles per instruction
- Used in consumer electronics, games, and embedded control

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Mostek |
| Year | 1977 |
| Clock | 4.0 MHz |
| Transistors | ~8,000 |
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
   - Single-chip design is faster than original F8 multi-chip (CPI 6.0 vs 7.0)
   - Register operations at 4.5 cycles; immediate at 6.0 cycles
   - Memory read/write at 7.0 cycles each
   - Branch at 8.0 cycles; call/return slowest at 11.0 cycles
   - Target CPI of 6.0 reflects improved single-chip architecture
   - 64-byte scratchpad provides fast variable access
   - F8 compatibility maintained for software reuse

## Validation Approach

- Compare against original Mostek datasheet
- Cross-validate against Fairchild F8 timing (CPI should be lower)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mostek)
- [Wikipedia](https://en.wikipedia.org/wiki/Mostek)

---
Generated: 2026-01-29
