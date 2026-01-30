# Toshiba TLCS-12 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s (1973)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- First Japanese microprocessor (1973)
- 12-bit data path with PMOS technology (~2500 transistors)
- Designed for Ford EEC (Electronic Engine Control) system
- Limited instruction set with multi-cycle execution for all instructions
- No instruction overlap or pipelining
- 1 MHz clock speed constrained by PMOS process
- 12-bit address space (4096 words)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Toshiba |
| Year | 1973 |
| Clock | 1.0 MHz |
| Transistors | 2,500 |
| Data Width | 12-bit |
| Address Width | 12-bit |
| Process | PMOS |
| Target CPI | 8.0 |

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

**Stage Timing:**
- Fetch: 4 cycles (12-bit instruction fetch, PMOS slow)
- Decode: 1 cycle
- Execute: 3 cycles (weighted average)
- Memory: 4 cycles (for load/store operations)

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 6 | Arithmetic operations (ADD, SUB, AND, OR) |
| Data Transfer | 5 | Move/transfer operations |
| Memory | 10 | Load/store from memory |
| I/O | 12 | Port I/O operations |
| Control | 8 | Branch/jump operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - PMOS technology results in inherently slow multi-cycle operations across all instruction types
   - No instruction overlap means CPI is a pure weighted sum of instruction category cycles
   - I/O operations are the slowest at 12 cycles, reflecting the slow PMOS bus interface
   - The 12-bit word size is unusual and limits addressable memory to 4K words
   - Designed as a dedicated engine controller, not a general-purpose CPU

## Validation Approach

- Compare against original Toshiba datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 8.0

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/toshiba/tlcs-12)
- [Wikipedia](https://en.wikipedia.org/wiki/TLCS-12)

---
Generated: 2026-01-29
