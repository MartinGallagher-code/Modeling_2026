# OKI MSM5840 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1982)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit microcontroller with integrated LCD driver
- 500 kHz clock for low-power operation
- On-chip ROM and RAM
- Dedicated LCD controller/driver hardware
- Used in calculators, watches, and LCD-equipped devices
- 6 instruction categories including LCD-specific operations

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI Semiconductor |
| Year | 1982 |
| Clock | 0.5 MHz |
| Transistors | ~8,000 |
| Data Width | 4-bit |
| Address Width | 11-bit |

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
   - LCD operations are slowest at 8 cycles (display driver interface)
   - ALU operations fastest at 4 cycles
   - I/O at 7 cycles; memory and control at 6 cycles each
   - Data transfer at 5 cycles
   - Target CPI of 6.0 with equal-weight typical workload
   - Display-intensive workload profile for LCD refresh scenarios
   - 11-bit address space provides 2K addressing

## Validation Approach

- Compare against original OKI datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/oki)
- [Wikipedia](https://en.wikipedia.org/wiki/Oki_Electric_Industry)

---
Generated: 2026-01-29
