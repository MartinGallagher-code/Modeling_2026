# Rockwell R6500/1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Single-chip microcontroller based on the MOS 6502 core
- Same instruction set and timing as the MOS Technology 6502
- On-chip 2KB ROM for program storage
- On-chip 64 bytes RAM for data storage
- Integrated I/O ports and timer
- 8-bit data bus, 16-bit address bus
- 1 MHz clock speed
- Designed for embedded applications

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Rockwell |
| Year | 1978 |
| Clock | 1.0 MHz |
| Transistors | 10,000 (estimated) |
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
| ALU | 2 | ALU operations (ADC, SBC, AND, ORA, EOR) |
| Data Transfer | 3 | Data transfer (LDA, STA, TAX, TXA) |
| Memory | 4 | Memory operations (indirect, indexed modes) |
| Control | 3 | Control flow (BNE, BEQ, JMP, JSR) |
| Stack | 3 | Stack operations (PHA, PLA, JSR/RTS) |

**Target CPI:** 3.0 (typical workload, same as MOS 6502)
**Expected IPS:** ~333 KIPS at 1 MHz

## Stage Timing

| Stage | Cycles |
|-------|--------|
| Fetch | 1 |
| Decode | 1 |
| Execute | 1 |
| Memory | 1 |
| Writeback | 0 |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Identical instruction timing to the MOS Technology 6502
   - On-chip ROM/RAM eliminates external memory bus overhead for small programs
   - ALU operations are fast (2 cycles) due to parallel ALU design
   - Memory operations with indexed/indirect addressing are the most expensive (4 cycles)
   - Control flow and stack operations are moderate at 3 cycles each
   - The R6500/1 trades off external memory capacity for single-chip integration
   - Timer peripheral does not affect CPU instruction timing

## Validation Approach

- Compare against MOS Technology 6502 datasheet timing (identical instruction set)
- Validate individual instruction category cycle counts
- Target: <5% CPI prediction error vs 3.0 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rockwell/r6500)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6502)

---
Generated: 2026-01-29
