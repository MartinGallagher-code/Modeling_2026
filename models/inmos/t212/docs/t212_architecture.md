# Inmos T212 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Mid 1980s (1985)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 16-bit transputer -- pioneer of parallel processing
- CSP (Communicating Sequential Processes) concurrency model
- 4KB on-chip SRAM for fast local execution
- Designed for Occam programming language
- Hardware process scheduler for lightweight context switching
- Four serial communication links for inter-transputer networking
- 32-bit address space despite 16-bit data path
- 15 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Inmos |
| Year | 1985 |
| Clock | 15.0 MHz |
| Transistors | 75,000 |
| Data Width | 16-bit |
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
   - ALU and data transfer operations are fast (1.5 cycles avg)
   - Memory operations average 3 cycles (on-chip SRAM helps)
   - Control/process operations are expensive (4 cycles) due to CSP scheduling
   - Stack operations average 3.5 cycles
   - Target CPI: ~2.5 for typical transputer workloads
   - On-chip SRAM significantly reduces memory latency
   - Process scheduling adds overhead to control flow

## Validation Approach

- Compare against original Inmos datasheet timing
- Validate with transputer emulator cycle counts
- Cross-validate with T424 and T800 transputer family
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/inmos/t212)
- [Wikipedia](https://en.wikipedia.org/wiki/Transputer)

---
Generated: 2026-01-29
