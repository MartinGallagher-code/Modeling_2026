# National COP420 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s embedded microcontrollers
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Enhanced version of the COP400 family
- Harvard architecture with separate program and data memory
- 4-bit data path for BCD and control operations
- 1 KB on-chip ROM (doubled from COP400)
- 64 nibbles on-chip RAM
- Expanded instruction set over base COP400
- 10-bit address space enabling larger program storage
- Backward-compatible with COP400 software

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1979 |
| Clock | 1.0 MHz |
| Transistors | 6,000 |
| Data Width | 4-bit |
| Address Width | 10-bit |

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

### Instruction Category Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3.5 | Arithmetic/logic operations (3-4 cycles) |
| Data Transfer | 3.5 | Register and data transfers (3-4 cycles) |
| Memory | 4.5 | ROM/RAM access operations (4-5 cycles) |
| Control | 5.0 | Jump and call operations (5-6 cycles) |
| I/O | 4.5 | Input/output operations (4-5 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Same instruction timing as COP400 -- the enhancement is in memory capacity, not speed
   - 10-bit address space allows 1 KB ROM (vs 512 bytes on COP400)
   - 64 nibbles of RAM provide more data storage for applications
   - Harvard architecture maintains separate instruction and data paths
   - Identical cycle counts to COP400 reflect shared microarchitecture

## Validation Approach

- Compare against original National Semiconductor COP420 datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/national_semiconductor/cop420)
- [Wikipedia](https://en.wikipedia.org/wiki/COP400)

---
Generated: 2026-01-29
