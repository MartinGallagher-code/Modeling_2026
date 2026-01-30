# AMI S2400 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s Calculator Chips
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Improved S2000 series calculator chip (1973)
- PMOS technology with faster 300 kHz clock (50% increase over S2000)
- 4-bit data path for BCD arithmetic
- 10-bit address bus (1024 bytes ROM addressable)
- Improved instruction timing over the S2000 baseline
- Simple serial instruction execution with no pipelining
- Keyboard scanning and segment display driver interface
- Approximately 4,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | American Microsystems Inc. (AMI) |
| Year | 1973 |
| Clock | 0.3 MHz (300 kHz) |
| Transistors | ~4,000 |
| Data Width | 4-bit |
| Address Width | 10-bit |
| Technology | PMOS |
| Package | 28-pin DIP |
| Target Application | Electronic calculators |

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

The S2400 uses the same serial execution model as the S2000 family but with
improved instruction timing. Each instruction passes through fetch, decode,
execute, and memory stages sequentially with no overlap. Cycle counts are
reduced by approximately 1 cycle per category compared to the S2000.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Clock frequency increased to 300 kHz (from 200 kHz), a 50% improvement
   - Instruction cycle counts reduced by ~1 cycle per category vs S2000 (5-9 vs 6-10)
   - Combined effect: both higher clock AND fewer CPI yield significantly better throughput
   - Target CPI of 7.0 (down from S2000's 8.0), representing a 12.5% CPI improvement
   - ALU operations are the fastest at 5 cycles (vs S2000's 6 cycles)
   - I/O operations remain the slowest at 9 cycles (vs S2000's 10 cycles)
   - The S2400 represents the most refined member of the original S2000 calculator family
   - Expected IPS improvement over S2000: ~71% (higher clock x lower CPI)

## Validation Approach

- Compare against original AMI S2400 datasheet timing specifications
- Cross-validate against S2000 family timings (expect ~1 cycle improvement per category)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected IPS at 300 kHz: ~42,857 instructions per second

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ami/s2400)
- [Wikipedia](https://en.wikipedia.org/wiki/AMI_S2000)
- AMI S2000 Series Calculator Chip Technical Reference Manual

---
Generated: 2026-01-29
