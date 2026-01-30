# RCA CDP1806 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Final enhanced COSMAC variant in the 1802 family
- Fastest clock support in the COSMAC line (up to 5 MHz)
- Additional instructions beyond 1802/1804 set
- Improved bus timing for faster memory access
- Full backward compatibility with 1802/1804 instruction set
- CMOS technology for radiation hardness and low power
- 16-register architecture inherited from COSMAC design

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | RCA |
| Year | 1985 |
| Clock | 5.0 MHz |
| Transistors | 8,000 |
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
| Register Ops | 5 | Register-to-register (fastest COSMAC) |
| Immediate | 8 | Immediate operand |
| Memory Read | 9 | Load from memory |
| Memory Write | 9 | Store to memory |
| Branch | 10 | Branch/jump |
| Call/Return | 14 | Subroutine call/return |

**Target CPI:** 8.0 (typical workload)
**Expected IPS:** ~625 KIPS at 5 MHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The CDP1806 is the fastest COSMAC, with CPI of 8.0 vs 1804's 10.0 and 1802's 12.0
   - Improved bus timing reduces cycle counts across all instruction categories
   - Register operations drop to 5 cycles (from 7 on 1804, 8 on 1802)
   - Higher clock speed (5 MHz) combined with lower CPI yields significant throughput gain
   - Still strictly serial execution with no pipeline or overlap

## Validation Approach

- Compare against original RCA COSMAC datasheet timing
- Validate CPI is faster than 1804 (CPI < 10) and 1802 (CPI < 12)
- Target: <5% CPI prediction error vs 8.0 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rca/cosmac)
- [Wikipedia](https://en.wikipedia.org/wiki/RCA_1802)

---
Generated: 2026-01-29
