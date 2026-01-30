# U808 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1970s-1980s (pre-pipeline microprocessors)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- East German clone of the Intel 8008 by VEB Mikroelektronik Erfurt
- First microprocessor produced in East Germany
- 8-bit data bus, 14-bit address bus (16KB addressable)
- Full Intel 8008 instruction set compatibility
- On-chip 7-level hardware stack (no external stack)
- PMOS technology (negative logic)
- 5-11 T-states per instruction
- Very limited address space (16KB) compared to later 8-bit processors
- Used in early East German industrial controllers and educational systems

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | VEB Mikroelektronik Erfurt (East Germany) |
| Year | 1978 |
| Clock | 0.5 MHz |
| Transistors | ~3,500 |
| Data Width | 8-bit |
| Address Width | 14-bit |
| Process | PMOS |
| Western Equivalent | Intel 8008 |

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
   - Instruction timing identical to Intel 8008
   - PMOS technology results in very slow clock speed (500 kHz)
   - On-chip 7-level stack limits call depth (no external stack pointer)
   - 14-bit address space limits to 16KB -- very constrained
   - Each T-state is 2 clock periods (1 cycle = 2 states)
   - JMP and CALL both take 11 T-states
   - RET is fast at 5 T-states (stack is on-chip)
   - Target CPI of ~10.0 for typical workloads matches Intel 8008

## Validation Approach

- Compare against original Intel 8008 datasheet timing
- Validate with cycle-accurate 8008 emulator (if available)
- Cross-reference with VEB Mikroelektronik Erfurt documentation
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/8008)
- [Wikipedia - Intel 8008](https://en.wikipedia.org/wiki/Intel_8008)

---
Generated: 2026-01-29
