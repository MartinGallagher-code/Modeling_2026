# AMD Am9511 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s arithmetic coprocessor era
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Stack-based arithmetic processing unit (APU) for 8-bit microprocessor systems
- 4-level internal operand stack
- 32-bit single-precision floating-point support (IEEE-like format)
- 16-bit and 32-bit fixed-point integer arithmetic
- Hardware implementation of transcendental functions (sqrt, trig)
- 8-bit data bus interface for host CPU communication
- Designed as coprocessor companion to Intel 8080/8085 and Zilog Z80
- Command/data register interface
- NMOS technology
- 24-pin DIP package

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | AMD |
| Year | 1977 |
| Clock | 3.0 MHz |
| Transistors | ~6,000 (estimated) |
| Data Width | 32-bit (internal) / 8-bit (bus) |
| Address Width | N/A (coprocessor) |
| Technology | NMOS |
| Package | 24-pin DIP |
| Stack Depth | 4 levels |
| Target CPI | 25.0 |

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

The Am9511 is a math coprocessor with highly variable execution times. Floating-point operations dominate the CPI, with square root (45 cycles) and division (32 cycles) being the most expensive. Fixed-point operations are significantly faster at 8 cycles. The serial execution model captures the sequential nature of stack-based operation processing.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Five instruction categories with widely varying cycle counts: fp_add (16), fp_mul (24), fp_div (32), fp_sqrt (45), and fixed_point (8)
   - The large CPI range (8-45 cycles) reflects the microcoded iterative algorithms used for floating-point operations
   - Stack-based architecture means all operands come from the internal 4-level stack, eliminating register selection overhead but limiting parallelism
   - Typical workload is dominated by floating-point multiply and divide operations, yielding CPI = 25.0
   - The Am9511 operates as a coprocessor -- the host CPU sends commands and data via an 8-bit bus interface, adding latency not captured in the core model
   - Square root uses successive approximation, accounting for its high cycle count
   - Fixed-point operations are much faster due to simpler hardware paths

## Validation Approach

- Compare against original AMD Am9511/Am9511A datasheet timing specifications
- Validate individual instruction cycle counts against datasheet tables
- Typical CPI of 25.0 represents a weighted mix of floating-point and fixed-point operations
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/amd/am9511)
- [Wikipedia](https://en.wikipedia.org/wiki/Am9511)
- AMD Am9511/Am9511A Arithmetic Processing Unit Data Sheet
- "Am9511A/Am9512 Floating Point Processor," AMD Technical Manual, 1981

---
Generated: 2026-01-29
