# AMD Am29116 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s microprogrammable processor era
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 16-bit single-chip microprogrammable CPU
- Integrates Am2901-equivalent ALU functionality in a single device
- Full 16-bit ALU with arithmetic and logic operations
- Barrel shifter for single-cycle shift/rotate operations
- 16 x 16-bit general-purpose register file
- Microprogrammable instruction set (user-defined microcode)
- Hardware multiply support
- Status register with carry, overflow, zero, and negative flags
- Bipolar technology for high-speed operation
- 48-pin package

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AMD |
| Year | 1983 |
| Clock | 10.0 MHz |
| Transistors | 20,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | Bipolar |
| Package | 48-pin |
| Register File | 16 x 16-bit |

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

The Am29116 executes micro-instructions sequentially. ALU and shift operations complete in 1 cycle, while memory and control (microsequencer) operations require 2 cycles due to external bus access and microcode sequencing overhead.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The Am29116 integrates the equivalent of four Am2901 4-bit ALU slices into a single 16-bit processor
   - ALU operations (ADD, SUB, etc.) and shift operations execute in 1 cycle thanks to the integrated datapath
   - Memory operations require 2 cycles due to external bus interface latency
   - Control/microsequencer operations require 2 cycles for microcode fetch and branch resolution
   - The typical workload distributes evenly across all four categories (25% each), yielding a typical CPI of 1.5
   - As a microprogrammable device, the actual instruction set is defined by the microcode, making workload profiles system-dependent

## Validation Approach

- Compare against original AMD Am29116 datasheet timing specifications
- Validate with cycle-accurate emulator (if available)
- Typical CPI of 1.5 reflects the mix of single-cycle ALU/shift and dual-cycle memory/control operations
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/amd/am29116)
- [Wikipedia](https://en.wikipedia.org/wiki/AMD_Am2900)
- AMD Am29000 Family Data Book
- AMD Bipolar/MOS Integrated Circuits Data Book (1985)

---
Generated: 2026-01-29
