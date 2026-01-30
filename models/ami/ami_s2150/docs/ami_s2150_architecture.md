# AMI S2150 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s Calculator Chips
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- S2000 variant with minor enhancements (1972)
- PMOS technology with 200 kHz clock
- 4-bit data path for BCD arithmetic
- 9-bit address bus (512 bytes ROM addressable)
- Same instruction timing as the S2000 base model
- Simple serial instruction execution with no pipelining
- Keyboard scanning and segment display driver interface
- Approximately 3,200 transistors (slightly more than S2000)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | American Microsystems Inc. (AMI) |
| Year | 1972 |
| Clock | 0.2 MHz (200 kHz) |
| Transistors | ~3,200 |
| Data Width | 4-bit |
| Address Width | 9-bit |
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

The S2150 shares the same serial execution model as the S2000. Each instruction
passes through fetch, decode, execute, and memory stages sequentially with no
overlap. The weighted CPI model uses five instruction categories (ALU, data transfer,
memory, I/O, control) with identical cycle counts to the S2000 (6 to 10 cycles).

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Architecturally identical to the S2000 in terms of instruction timing
   - Minor enhancements in peripheral circuitry account for the slightly higher transistor count
   - Same PMOS technology and 200 kHz clock as the S2000
   - I/O operations remain the slowest at 10 cycles
   - ALU operations remain the fastest at 6 cycles
   - Target CPI of 8.0 matches the S2000 baseline
   - The S2150 is best understood as a pin-compatible or application-specific variant of the S2000

## Validation Approach

- Compare against original AMI S2150 datasheet timing specifications
- Cross-validate against S2000 timings (expected to be identical)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected IPS at 200 kHz: ~25,000 instructions per second

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ami/s2150)
- [Wikipedia](https://en.wikipedia.org/wiki/AMI_S2000)
- AMI S2000 Series Calculator Chip Technical Reference Manual

---
Generated: 2026-01-29
