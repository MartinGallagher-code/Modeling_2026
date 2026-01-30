# Rockwell PPS-4 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1971-1976
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Third commercial microprocessor (after Intel 4004 and 4040)
- 4-bit data bus with serial ALU (processes 1 bit at a time)
- Very slow compared to parallel ALU designs
- 200 kHz typical clock speed
- 12-bit address bus supporting 4KB ROM
- Used in calculators, pinball machines, and POS terminals
- Instructions take 1-4 instruction cycles, each cycle is ~5 clock cycles

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Rockwell International |
| Year | 1972 |
| Clock | 0.2 MHz |
| Transistors | 5,000 (estimated) |
| Data Width | 4-bit |
| Address Width | 12-bit |

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
| ALU | 14 | ADD/SUB via serial bit processing |
| Memory | 11 | Load/Store operations |
| Branch | 12 | Conditional/unconditional jumps |
| I/O | 10 | Discrete I/O operations |

**Target CPI:** 12.0 (typical workload)
**Expected IPS:** ~16,667 at 200 kHz

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Serial ALU processes one bit at a time, making arithmetic operations particularly slow
   - ALU operations are the most expensive at 14 cycles due to bit-serial processing
   - Each 4-bit operation requires multiple passes through the serial ALU
   - I/O operations are relatively fast (10 cycles) as they are discrete port accesses
   - The serial nature of the ALU is the primary performance bottleneck in compute workloads
   - Very low absolute throughput (~16K IPS) typical for early 1970s 4-bit processors

## Validation Approach

- Compare against original Rockwell PPS-4 datasheet timing
- Validate serial ALU is bottleneck in compute-intensive workloads
- Verify all workload CPIs fall in 10-14 cycle range
- Target: <5% CPI prediction error vs 12.0 target

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/rockwell/pps-4)
- [Wikipedia](https://en.wikipedia.org/wiki/Rockwell_PPS-4)

---
Generated: 2026-01-29
