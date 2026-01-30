# Inmos T424 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 32-bit transputer (variant of T414 family)
- CSP (Communicating Sequential Processes) concurrency model
- 4KB on-chip SRAM
- Designed for Occam programming language
- Hardware process scheduler with lightweight context switching
- Four serial communication links for inter-transputer networking
- 32-bit data path and 32-bit address space
- Channel communication primitives in hardware
- 15 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1985 |
| Clock | 15.0 MHz |
| Transistors | 150,000 |
| Data Width | 32-bit |
| Address Width | 32-bit |

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
   - 32-bit data path allows full-width operations in single step
   - ALU and data transfer are fast (1.5 cycles avg)
   - On-chip memory access averages 2.5 cycles
   - Control/process operations average 3 cycles
   - Channel communication operations average 3.5 cycles (hardware CSP)
   - Faster than T212 due to wider data path and lower memory overhead
   - 2x transistor count vs T212 supports 32-bit operations

## Validation Approach

- Compare against original Inmos datasheet timing
- Validate with transputer emulator cycle counts
- Cross-validate with T212 (16-bit) and T800 (FPU) transputers
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/inmos/t424)
- [Wikipedia](https://en.wikipedia.org/wiki/Transputer)

---
Generated: 2026-01-29
