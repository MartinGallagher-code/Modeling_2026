# Intel 8231 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s arithmetic coprocessor era
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Arithmetic Processing Unit (APU) -- simpler predecessor to the 8087 FPU
- Fixed-point and floating-point arithmetic via 8-bit data bus
- 32-bit internal operations transferred through 8-bit external interface
- Hardware floating-point add, multiply, and divide
- Fixed-point arithmetic support for integer-heavy workloads
- Designed as companion chip for 8080/8085 systems
- Multi-cycle operations (15-65 cycles typical)

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1977 |
| Clock | 2.0 MHz |
| Transistors | ~8,000 |
| Data Width | 8-bit (bus), 32-bit (internal) |
| Address Width | 8-bit |

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

The 8231 is a coprocessor that receives commands and operands over the 8-bit bus.
Execution dominates the pipeline since arithmetic operations take 15-65 cycles,
while bus transfers take 10-20 cycles. The execute stage is the clear bottleneck.

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| FP Add | 30.0 | Floating-point addition (25-35 cycles) |
| FP Multiply | 45.0 | Floating-point multiplication (40-50 cycles) |
| FP Divide | 65.0 | Floating-point division (55-75 cycles) |
| Fixed Point | 25.0 | Fixed-point arithmetic (20-30 cycles) |
| Data Transfer | 15.0 | Bus transfer operations (10-20 cycles) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - As a coprocessor, the 8231 does not fetch its own instructions from memory
   - Commands and operands are pushed to the 8231 by the host CPU over the 8-bit bus
   - Floating-point multiply (45 cycles) dominates typical workload (~48.5% weight)
   - FP division is the most expensive single operation at 65 cycles
   - The 8-bit bus creates a bottleneck for 32-bit operand transfers (4 bytes per operand)
   - Data transfer overhead (15 cycles) accounts for multi-byte bus serialization
   - Simpler than the later 8087 FPU: fewer operations, no register stack
   - Typical workload CPI is high (~37 cycles) due to multi-cycle math operations

## Validation Approach

- Compare against original Intel 8231 APU datasheet
- Validate arithmetic operation timing against documentation
- Cross-check with 8232 (enhanced version) for consistency
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/8231)
- [Wikipedia](https://en.wikipedia.org/wiki/Intel_8231)

---
Generated: 2026-01-29
