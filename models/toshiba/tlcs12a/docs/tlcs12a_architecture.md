# Toshiba TLCS-12A Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1975)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Improved version of the TLCS-12 (first Japanese microprocessor)
- NMOS technology replacing original PMOS for significant speed improvement
- 12-bit data path with minicomputer-style architecture
- 2 MHz clock (double the original TLCS-12)
- 12-bit address space (4096 words)
- Software compatible with TLCS-12
- Estimated ~5000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Toshiba |
| Year | 1975 |
| Clock | 2.0 MHz |
| Transistors | ~5,000 |
| Data Width | 12-bit |
| Address Width | 12-bit |
| Process | NMOS |
| Target CPI | 6.0 |

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
- Fetch: 3 cycles (12-bit, faster NMOS)
- Decode: 1 cycle
- Execute: 2 cycles
- Memory: 4 cycles

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 4 | ALU operations (ADD, SUB, AND, OR) |
| Data Transfer | 4 | Data transfer (load, store) |
| Memory | 7 | Memory operations (indirect) |
| I/O | 9 | I/O operations |
| Control | 6 | Control flow (branch, jump, skip) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - NMOS process provides roughly 2x speed improvement over PMOS TLCS-12
   - Lower CPI across all instruction categories compared to TLCS-12 (6.0 vs 8.0 target)
   - Minicomputer-style architecture with 12-bit word size
   - Software backward compatible with TLCS-12 but runs faster due to process and clock improvements
   - I/O operations remain the slowest category at 9 cycles

## Validation Approach

- Compare against original Toshiba datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 6.0

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/toshiba/tlcs-12a)
- [Wikipedia](https://en.wikipedia.org/wiki/TLCS-12)

---
Generated: 2026-01-29
