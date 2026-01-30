# Monolithic Memories 6701 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1970s (1975)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit slice ALU, similar to AMD Am2901
- Bipolar Schottky technology for high speed
- Single-cycle microinstruction execution
- 16 general-purpose registers per slice
- Carry look-ahead support for multi-slice configurations
- Part of the 67xx bit-slice family
- Competitor to AMD Am2900 family (Monolithic Memories later acquired by AMD)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Monolithic Memories |
| Year | 1975 |
| Clock | 8.0 MHz |
| Transistors | ~180 |
| Data Width | 4-bit |
| Address Width | 4-bit |

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
   - All operations execute in exactly 1 cycle (single-cycle microinstructions)
   - Target CPI of 1.0 is constant across all workloads
   - ALU, shift, pass-through, and zero operations all at 1 cycle
   - Bipolar Schottky technology enables fast switching
   - Directly comparable to AMD Am2901 (same CPI, similar architecture)
   - 8 MHz clock with 125ns cycle time

## Validation Approach

- Compare against original Monolithic Memories datasheet
- Cross-validate against AMD Am2901 (comparable architecture)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/monolithic_memories)
- [Wikipedia](https://en.wikipedia.org/wiki/Monolithic_Memories)

---
Generated: 2026-01-29
