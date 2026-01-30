# KR580VM1 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Soviet 8080 extension (NOT a direct clone)
- Extends Intel 8080 with 128KB addressing via bank switching (vs 64KB)
- 8-bit data bus, 17-bit effective address space
- Full Intel 8080 instruction set plus bank management instructions
- Bank-switching mechanism for extended memory access
- Base timing similar to 8080 with extra overhead for bank operations
- Used in Soviet industrial controllers and Elektronika BK series peripherals

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Soviet Union (various fabs) |
| Year | 1980 |
| Clock | 2.5 MHz |
| Transistors | ~6,500 |
| Data Width | 8-bit |
| Address Width | 17-bit (128KB via bank switching) |
| Process | NMOS |
| Western Equivalent | Intel 8080 (extended) |

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
   - Base instruction timing matches Intel 8080
   - Bank-switch instructions add ~12 states overhead per bank change
   - Cross-bank memory transfers incur additional overhead beyond standard 8080 timing
   - Not a direct clone -- the ISA is extended with bank management instructions
   - Target CPI of ~8.0 for typical workloads (slightly slower than 8080's ~7.5 due to bank management overhead)
   - Workload profiles account for bank-switching frequency (10-20% of instructions in memory-heavy workloads)

## Validation Approach

- Compare base instruction timing against Intel 8080 datasheet
- Account for bank-switching overhead in mixed workloads
- Validate with Soviet-era technical documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/8080)
- [Wikipedia - Intel 8080](https://en.wikipedia.org/wiki/Intel_8080)

---
Generated: 2026-01-29
