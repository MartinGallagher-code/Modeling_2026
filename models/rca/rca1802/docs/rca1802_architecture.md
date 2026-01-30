# RCA 1802 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- First CMOS microprocessor (COSMAC architecture)
- 16 general-purpose 16-bit registers (R0-RF)
- No instruction prefetch or pipeline
- Direct memory access on every instruction
- Variable-length instruction fetch
- Radiation-hardened design (used in space applications including Voyager)
- Very low power consumption due to CMOS technology
- Simple DMA and interrupt architecture

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | RCA |
| Year | 1980 |
| Clock | 1.0 MHz |
| Transistors | 10,000 |
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

## Instruction Timing Summary

| Category | Cycles | Description |
|----------|--------|-------------|
| Register Ops | 8 | Register-to-register operations |
| Immediate | 12 | Immediate operand |
| Memory Read | 14 | Load from memory |
| Memory Write | 14 | Store to memory |
| Branch | 14 | Branch/jump |
| Call/Return | 20 | Subroutine call/return |

**Target CPI:** 12.0 (typical workload)
**Expected IPS:** ~83 KIPS at 1 MHz

## Stage Timing

| Stage | Cycles |
|-------|--------|
| Fetch | 4 |
| Decode | 1 |
| Execute | 3 |
| Memory | 3 |
| Writeback | 0 |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The RCA 1802 was intentionally slow due to CMOS design for low power and radiation hardness
   - Multi-cycle instructions with no overlap or pipelining
   - Register-pointer architecture: any register can serve as the program counter
   - Call/return is expensive (20 cycles) because the 1802 uses register manipulation for subroutines
   - No dedicated stack pointer -- subroutine linkage uses register pairs
   - Instruction timing is much higher than contemporary NMOS processors

## Validation Approach

- Compare against original RCA COSMAC 1802 datasheet timing
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rca/cosmac)
- [Wikipedia](https://en.wikipedia.org/wiki/RCA_1802)

---
Generated: 2026-01-29
