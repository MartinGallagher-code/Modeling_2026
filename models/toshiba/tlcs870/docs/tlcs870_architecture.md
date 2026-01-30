# Toshiba TLCS-870 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain (sequential execution with variable timing)

## Architectural Features

- Proprietary 8-bit MCU architecture (not Z80 or 6502 compatible)
- Unique Toshiba ISA with bit manipulation instructions
- On-chip peripherals: ROM, RAM, Timer, I/O, UART
- Low power CMOS design
- 8 MHz clock
- 16-bit address space (64K)
- Used in automotive, industrial, and consumer applications
- Estimated ~15,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Toshiba |
| Year | 1985 |
| Clock | 8.0 MHz |
| Transistors | ~15,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | CMOS |
| On-chip UART | Yes |
| Target CPI | 4.5 |

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
| ALU | 3 | ADD, SUB, AND, OR, XOR |
| Data Transfer | 3 | LD, MOV |
| Memory | 5 | Indirect, indexed addressing |
| I/O | 6 | Port operations |
| Control | 5 | JP, CALL, RET |
| Bit Operations | 3 | SET, CLR, TEST |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Unique proprietary ISA -- not derived from Z80 or any other common architecture
   - Bit manipulation instructions (SET, CLR, TEST) are a distinguishing feature, modeled as a separate category at 3 cycles
   - CMOS design enables 8 MHz clock with low power, a significant improvement over earlier PMOS/NMOS Toshiba designs
   - I/O operations are the slowest at 6 cycles, as port access requires bus setup
   - Typical embedded workloads are memory and I/O heavy, reflected in workload profiles
   - Variable instruction timing across categories (3-6 cycles) produces a moderate target CPI of 4.5

## Validation Approach

- Compare against original Toshiba datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected typical workload CPI: 4.5

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/toshiba/tlcs-870)
- [Wikipedia](https://en.wikipedia.org/wiki/TLCS-870)

---
Generated: 2026-01-29
