# Sharp LH5801 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1981)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 8-bit CPU designed for calculators and pocket computers
- Single instruction at a time, no instruction prefetch
- No pipeline
- Direct memory access on every instruction
- Variable-length instruction fetch
- Optimized for low power consumption and compact code
- Used in Sharp PC-1500 and PC-1600 pocket computers

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sharp |
| Year | 1981 |
| Clock | 1.3 MHz |
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
   - Low clock speed (1.3 MHz) optimized for battery-powered pocket computers
   - Register operations fastest at 4 cycles; call/return slowest at 10 cycles
   - Memory read/write and branch operations at 7 cycles each
   - Target CPI of 6.0 reflects pocket computer workload mix
   - Stage timing: fetch=2, decode=1, execute=2, memory=2

## Validation Approach

- Compare against original Sharp datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/sharp)
- [Wikipedia](https://en.wikipedia.org/wiki/Sharp_LH5801)

---
Generated: 2026-01-29
