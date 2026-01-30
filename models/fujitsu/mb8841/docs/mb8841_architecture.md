# Fujitsu MB8841 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (4-bit microcontroller era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit NMOS microcontroller
- Harvard architecture (separate program and data memory)
- 1KB ROM for program storage
- 32 nibbles (128 bits) of RAM
- 64-instruction set
- Used in Namco arcade games (Galaga, Xevious, Bosconian)
- Fixed-cycle instruction execution (3-8 cycles depending on category)
- No pipeline, no cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Clock | 1.0 MHz |
| Transistors | ~3,000 |
| Data Width | 4-bit |
| Address Width | 10-bit (1KB ROM) |
| Process | NMOS |
| Package | DIP |
| ROM | 1KB |
| RAM | 32 nibbles |
| Instruction Set | 64 instructions |
| Target CPI | 4.0 |

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU (ADD/SUB/INC/DEC) | 3 | 4-bit arithmetic operations |
| Data Transfer (MOV) | 3 | Register-to-register moves |
| Memory (LD/ST) | 4 | 32-nibble RAM access |
| I/O (IN/OUT) | 6 | External port operations |
| Control (JMP/CALL/RET) | 5 | Branch and subroutine operations |

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
   - Harvard architecture means instruction fetch and data access use separate buses, but execution is still fully sequential
   - Variable instruction timing (3-8 cycles) requires weighted CPI calculation based on workload mix
   - I/O operations are significantly slower (6 cycles) due to external port access latency
   - Arcade game workloads have higher I/O weight than typical embedded applications
   - All instructions complete before the next begins (no overlap or pipelining)

## Validation Approach

- Compare against original Fujitsu MB8841 datasheet instruction timing
- Validate with MAME arcade emulator timing data (if available)
- Cross-reference with Namco arcade hardware documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/fujitsu/mb8841)
- [Wikipedia](https://en.wikipedia.org/wiki/Fujitsu_MB8841)
- [MAME Source](https://github.com/mamedev/mame) - MB8841 emulation core

---
Generated: 2026-01-29
