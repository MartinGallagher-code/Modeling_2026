# Toshiba TLCS-90 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain (sequential execution with variable timing)

## Architectural Features

- 8-bit MCU with Z80-compatible instruction set
- Z80-compatible ISA with Toshiba extensions
- Block transfer and search instructions (LDIR, LDDR, CPIR)
- On-chip peripherals: ROM, RAM, Timer, I/O, UART
- 6 MHz clock
- 16-bit address space (64K)
- Estimated ~12,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Toshiba |
| Year | 1985 |
| Clock | 6.0 MHz |
| Transistors | ~12,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| ISA Compatibility | Z80 |
| On-chip UART | Yes |
| Target CPI | 5.0 |

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

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 4 | ADD, SUB, AND, OR, XOR, CP |
| Data Transfer | 4 | LD, EX, PUSH, POP |
| Memory | 5 | Indirect, indexed addressing |
| I/O | 6 | IN, OUT |
| Control | 5 | JP, JR, CALL, RET |
| Block | 10 | LDIR, LDDR, CPIR (per iteration) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Z80-compatible instruction set means similar instruction timing characteristics to the original Z80
   - Block transfer instructions (LDIR, LDDR, CPIR) are modeled at 10 cycles per iteration, reflecting Z80-heritage multi-byte operations
   - Variable instruction timing (4-10 cycles) is characteristic of the Z80 family
   - On-chip peripherals reduce external bus contention compared to a discrete Z80 system
   - Block operations have a low typical weight (5%) but dominate when used in memory-intensive workloads (20%)
   - I/O at 6 cycles is the slowest single-operation category, consistent with Z80 port timing

## Validation Approach

- Compare against original Toshiba datasheet timing specifications
- Cross-reference with Z80 instruction timing (compatible subset)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 5.0

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/toshiba/tlcs-90)
- [Wikipedia](https://en.wikipedia.org/wiki/TLCS-90)

---
Generated: 2026-01-29
