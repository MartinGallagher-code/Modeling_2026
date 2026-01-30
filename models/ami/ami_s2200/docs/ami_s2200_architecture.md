# AMI S2200 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s Calculator Chips
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- S2000 variant with expanded ROM (1972)
- PMOS technology with 200 kHz clock
- 4-bit data path for BCD arithmetic
- 10-bit address bus (1024 bytes ROM addressable, expanded from S2000's 512 bytes)
- Same instruction timing as the S2000 base model
- Simple serial instruction execution with no pipelining
- Keyboard scanning and segment display driver interface
- Approximately 3,500 transistors (additional ROM capacity over S2000)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | American Microsystems Inc. (AMI) |
| Year | 1972 |
| Clock | 0.2 MHz (200 kHz) |
| Transistors | ~3,500 |
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

The S2200 shares the same serial execution model as the S2000 family. Each
instruction passes through fetch, decode, execute, and memory stages sequentially
with no overlap. The expanded ROM (10-bit address, 1K vs 512 bytes) allows more
complex calculator programs but does not change the instruction timing model.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Instruction timing is identical to the S2000 (6-10 cycles per category)
   - The expanded address width (10-bit vs 9-bit) doubles available ROM to 1024 bytes
   - Additional transistors (~3,500 vs ~3,000) are primarily for the larger ROM array
   - Same PMOS technology and 200 kHz clock as the S2000
   - Target CPI of 8.0 matches the S2000 baseline
   - The larger ROM enables more sophisticated calculator functions (e.g., scientific functions)
   - No execution performance improvement over the S2000 -- only program capacity increased

## Validation Approach

- Compare against original AMI S2200 datasheet timing specifications
- Cross-validate against S2000 timings (expected to be identical)
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected IPS at 200 kHz: ~25,000 instructions per second

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ami/s2200)
- [Wikipedia](https://en.wikipedia.org/wiki/AMI_S2000)
- AMI S2000 Series Calculator Chip Technical Reference Manual

---
Generated: 2026-01-29
