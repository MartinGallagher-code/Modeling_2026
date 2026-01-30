# Tesla MHB8080A Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Czechoslovak clone of the Intel 8080A by Tesla Piestany
- 8-bit data bus, 16-bit address bus (64KB addressable)
- Full Intel 8080 instruction set compatibility
- Non-multiplexed address and data buses
- 4-18 T-states per instruction
- Hardware interrupt system
- Used in PMI-80, PMD 85, Tesla SAPI-1, and various Czechoslovak computers

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Tesla Piestany (Czechoslovakia) |
| Year | 1982 |
| Clock | 2.0 MHz |
| Transistors | ~6,000 |
| Data Width | 8-bit |
| Address Width | 16-bit |
| Process | NMOS |
| Western Equivalent | Intel 8080A |

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
   - Instruction timing identical to Intel 8080A (full timing compatibility maintained by Tesla Piestany)
   - MOV r,r takes 5 T-states; MOV r,M takes 7 T-states
   - CALL takes 17 T-states, making subroutine overhead significant
   - PUSH takes 11 T-states, POP takes 10 T-states
   - XTHL (exchange top-of-stack with HL) takes 18 T-states
   - I/O instructions (IN/OUT) require 10 T-states
   - Target CPI of ~7.5 for typical workloads matches Intel 8080

## Validation Approach

- Compare against original Intel 8080A datasheet timing
- Validate with cycle-accurate 8080 emulator (if available)
- Cross-reference with Tesla Piestany documentation and PMD 85 technical manuals
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/8080)
- [Wikipedia - Intel 8080](https://en.wikipedia.org/wiki/Intel_8080)

---
Generated: 2026-01-29
