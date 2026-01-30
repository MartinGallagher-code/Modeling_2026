# Fujitsu MB8861 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (8-bit microprocessor era)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 8-bit NMOS microprocessor (Motorola 6800-compatible clone)
- 8-bit data bus, 16-bit address bus
- Two 8-bit accumulators (A and B)
- Single 16-bit index register (X)
- Variable instruction timing (2-12 cycles per instruction)
- Full timing compatibility with Motorola 6800
- Used in Japanese arcade machines and early Japanese computers
- No pipeline, no cache

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Fujitsu |
| Year | 1977 |
| Clock | 1.0 MHz |
| Transistors | ~4,100 (same as Motorola 6800) |
| Data Width | 8-bit |
| Address Width | 16-bit (64KB address space) |
| Process | NMOS |
| Package | DIP-40 |
| Registers | 2x 8-bit accumulators (A, B), 1x 16-bit index (X) |
| Compatibility | Motorola 6800 pin and software compatible |
| Target CPI | 4.0 |

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU (ADD/SUB/INC) | 2.8 | ADDA imm @2, INCA @2, weighted average |
| Data Transfer (LD/MOV) | 3.2 | LDAA imm @2, register moves |
| Memory (LD/ST extended) | 4.5 | LDAA dir @3, LDAA ext @4, STAA @4 |
| Control (JMP/Branch) | 4.5 | JMP @3, BEQ @4, weighted average |
| Stack (PUSH/PULL) | 5.0 | PSHA/PULA @4 cycles |
| Call/Return (JSR/RTS) | 9.0 | JSR @9, RTS @5, weighted average |

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

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Fujitsu's clone of the Motorola 6800 maintains full timing compatibility, so 6800 datasheet timings apply directly
   - Variable instruction timing (2-12 cycles) requires careful workload-weighted CPI calculation
   - JSR/RTS (call/return) instructions are the most expensive at 9 cycles, significantly impacting subroutine-heavy code
   - Six instruction categories provide finer granularity than the 4-bit MB884x models due to the richer 8-bit instruction set
   - Stack operations add overhead; control-flow-heavy workloads see higher CPI due to call/return costs
   - Unlike the MB884x 4-bit family, this is a full 8-bit microprocessor with von Neumann architecture

## Validation Approach

- Compare against original Motorola 6800 datasheet (Fujitsu maintained full timing compatibility)
- Validate with MAME emulator timing data for Japanese arcade hardware
- Cross-reference with Fujitsu MB8861 application notes
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/fujitsu/mb8861)
- [Wikipedia](https://en.wikipedia.org/wiki/Motorola_6800)
- [Motorola 6800 Datasheet](TODO: Add link) - timing reference
- [MAME Source](https://github.com/mamedev/mame) - MB8861/6800 emulation core

---
Generated: 2026-01-29
