# TI SN74S481 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s Schottky TTL Bit-Slice
**Queueing Model:** Serial M/M/1 chain (single-stage)

## Architectural Features

- 4-bit Schottky TTL bit-slice ALU
- Single-cycle operation for all functions
- Carry lookahead capability for high-speed cascading
- Compatible with 74S182 carry lookahead generator
- Faster than I2L-based alternatives (SBP0400/SBP0401)
- Arithmetic, logic, compare, and pass-through operations

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Texas Instruments |
| Year | 1976 |
| Clock | 8.0 MHz |
| Transistors | ~180 |
| Data Width | 4-bit |
| Address Width | 4-bit |

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

Note: As a purely combinational ALU slice, the SN74S481 collapses to a single-stage model. All operations complete in exactly one clock cycle. CPI = 1.0.

Target CPI: 1.0

### Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| Arithmetic | 1 | ADD, SUB, INCR, DECR |
| Logic | 1 | AND, OR, XOR, NOT, NAND, NOR |
| Compare | 1 | Compare operations |
| Pass | 1 | Pass through (A, B, zero, ones) |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template (degenerate single-cycle case)
2. Key modeling considerations:
   - All operations are single-cycle -- CPI is always exactly 1.0
   - Schottky TTL process provides faster switching than I2L (compare SBP0400 at 10 MHz with multi-cycle ops)
   - The key advantage over the SN74181 is improved functionality and cascadability
   - When used in a bit-slice CPU design, the microsequencer adds additional cycles, but the ALU itself is always single-cycle
   - The 74S182 companion carry lookahead generator enables high-speed 16-bit and wider configurations

## Validation Approach

- Compare against original Texas Instruments datasheet
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ti/sn74s481)
- [Wikipedia](https://en.wikipedia.org/wiki/74181)

---
Generated: 2026-01-29
