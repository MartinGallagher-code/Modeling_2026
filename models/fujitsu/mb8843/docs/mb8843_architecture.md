# Fujitsu MB8843 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (4-bit microcontroller era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit NMOS microcontroller (MB8841 variant)
- Harvard architecture (separate program and data memory)
- 2KB ROM for program storage
- 4-bit parallel ALU
- Fixed-cycle instruction execution (all instructions 4 cycles)
- Used in consumer electronics and gaming applications
- No pipeline, no cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Clock | 1.0 MHz |
| Transistors | ~5,000 (estimated) |
| Data Width | 4-bit |
| Address Width | 11-bit (2KB ROM) |
| Process | NMOS |
| Package | DIP |
| ROM | 2KB |
| Instruction Set | MB8841-compatible |
| Target CPI | 4.0 |

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU (ADD/SUB/logic) | 4 | Arithmetic and logical operations |
| Data Transfer | 4 | Register-memory transfers |
| Memory (LD/ST) | 4 | Load/store operations |
| Control (Branch/Call/Return) | 4 | Control flow operations |
| I/O (IN/OUT) | 4 | Input/output port operations |

All instructions execute in exactly 1 machine cycle = 4 clock cycles, yielding a uniform CPI of 4.0 regardless of workload mix.

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
   - Uniform 4-cycle timing for all instruction categories simplifies the model significantly
   - CPI is constant at 4.0 regardless of workload composition
   - MB8841 variant targeted at consumer electronics and gaming rather than arcade-specific use
   - Same core architecture as MB8842 but different pin configuration and I/O arrangement
   - Harvard architecture provides separate program and data paths but execution remains sequential

## Validation Approach

- Compare against original Fujitsu MB884x family datasheet
- Validate uniform 4-cycle timing across all instruction categories
- Cross-reference with consumer electronics application notes
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/fujitsu/mb8843)
- [Wikipedia](https://en.wikipedia.org/wiki/Fujitsu_MB884x)
- [MAME Source](https://github.com/mamedev/mame) - MB884x emulation core

---
Generated: 2026-01-29
