# AMI S2000 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1970s Calculator Chips
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- One of the earliest 4-bit calculator chips (1971)
- PMOS technology with 200 kHz clock
- 4-bit data path for BCD arithmetic
- 9-bit address bus (512 bytes ROM addressable)
- Simple serial instruction execution with no pipelining
- Dedicated calculator instruction set (add, subtract, display control)
- Keyboard scanning and segment display driver interface
- Approximately 3,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | American Microsystems Inc. (AMI) |
| Year | 1971 |
| Clock | 0.2 MHz (200 kHz) |
| Transistors | ~3,000 |
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

The S2000 uses a simple serial execution model. Each instruction passes through
fetch, decode, execute, and memory stages sequentially. No overlap or pipelining
exists. The weighted CPI model uses five instruction categories (ALU, data transfer,
memory, I/O, control) with cycle counts ranging from 6 to 10 cycles per instruction.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - All instructions execute serially with no overlap between stages
   - PMOS technology results in very slow switching speeds (200 kHz clock)
   - I/O operations (display/keyboard) are the slowest at 10 cycles due to external device timing
   - ALU operations are the fastest at 6 cycles, performing simple 4-bit BCD arithmetic
   - Target CPI of 8.0 reflects the high overhead of early PMOS design
   - Instruction mix is modeled as uniform (20% each category) for typical calculator workloads

## Validation Approach

- Compare against original AMI S2000 datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected IPS at 200 kHz: ~25,000 instructions per second

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ami/s2000)
- [Wikipedia](https://en.wikipedia.org/wiki/AMI_S2000)
- AMI S2000 Series Calculator Chip Technical Reference Manual

---
Generated: 2026-01-29
