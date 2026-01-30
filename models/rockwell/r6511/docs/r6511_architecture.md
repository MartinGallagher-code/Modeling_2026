# Rockwell R6511 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 6502-compatible core with integrated peripherals
- 8-bit NMOS microcontroller
- Sequential execution with no pipeline
- Same instruction timing as MOS 6502
- 2-7 cycles per instruction
- On-chip RAM, ROM, I/O ports, and timer
- 16-bit address bus for full 64KB address space
- Up to 2 MHz clock speed
- Designed for embedded control and consumer electronics

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Rockwell |
| Year | 1980 |
| Clock | 2.0 MHz |
| Transistors | 5,000 (estimated) |
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
| ALU | 2.3 | INX/DEX @2, ADC imm @2, ADC zp @3, CMP @2-3 |
| Data Transfer | 2.8 | LDA imm @2, LDA zp @3, LDA abs @4, TAX @2 |
| Memory | 4.0 | STA zp @3, STA abs @4, indexed @4-5, indirect @5-6 |
| Control | 2.6 | Branch avg @2.55 (50% taken), JMP @3 |
| Stack | 3.5 | PHA @3, PLA @4, JSR @6, RTS @6 |

**Target CPI:** 3.0 (typical workload, same as MOS 6502)
**Expected IPS:** ~667 KIPS at 2 MHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Uses weighted-average cycle counts per category for more precise modeling
   - Memory operations are the most expensive category (4.0 cycles) due to indirect/indexed modes
   - Stack operations include expensive JSR/RTS at 6 cycles each, weighted with PHA/PLA
   - Branch prediction is modeled at 50% taken rate with 2.55 average cycles
   - The 2 MHz clock provides double the throughput of 1 MHz R6500/1
   - On-chip peripherals do not affect CPU instruction timing
   - IPC range of 0.15-0.6 is characteristic of 6502-family processors

## Validation Approach

- Compare against MOS Technology 6502 datasheet timing (compatible instruction set)
- Validate CPI is within 5% of 3.0 target
- Verify workload weight sums and cycle count reasonableness (1-10 range)
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rockwell/r6500)
- [Wikipedia](https://en.wikipedia.org/wiki/MOS_Technology_6502)

---
Generated: 2026-01-29
