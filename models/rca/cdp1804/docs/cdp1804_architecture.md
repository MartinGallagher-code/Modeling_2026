# RCA CDP1804 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Enhanced COSMAC architecture with on-chip counter/timer
- Compatible with RCA 1802 instruction set
- Faster execution due to process improvements over 1802
- On-chip timer for interrupt generation
- Same 16-register architecture as 1802 (sixteen 16-bit registers)
- CMOS technology for radiation hardness and low power
- DMA and interrupt support inherited from 1802

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | RCA |
| Year | 1980 |
| Clock | 2.0 MHz |
| Transistors | 6,000 |
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
| Register Ops | 7 | Register-to-register (faster than 1802) |
| Immediate | 10 | Immediate operand |
| Memory Read | 11 | Load from memory |
| Memory Write | 11 | Store to memory |
| Branch | 11 | Branch/jump |
| Call/Return | 18 | Subroutine call/return |

**Target CPI:** 10.0 (typical workload)
**Expected IPS:** ~200 KIPS at 2 MHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The CDP1804 is an enhanced 1802 with ~17% faster CPI (10.0 vs 12.0)
   - On-chip timer adds transistor count but does not change instruction timing
   - Same COSMAC register-pointer architecture (R0-RF as 16-bit registers)
   - Process improvements reduce per-cycle time but instruction cycle counts remain multi-cycle
   - No pipeline or instruction overlap -- strictly serial execution

## Validation Approach

- Compare against original RCA COSMAC datasheet timing
- Validate CPI is faster than 1802 (CPI < 12) but retains same instruction set
- Target: <5% CPI prediction error vs 10.0 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rca/cosmac)
- [Wikipedia](https://en.wikipedia.org/wiki/RCA_1802)

---
Generated: 2026-01-29
