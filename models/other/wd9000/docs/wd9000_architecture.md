# Western Digital WD9000 Pascal MicroEngine Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1979)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Microprogrammed processor executing UCSD Pascal p-code directly in hardware
- 16-bit stack-based architecture
- Hardware procedure call/return with automatic frame setup
- Hardware array bounds checking
- Writable microcode store for p-code execution
- Stack-oriented execution model (no general-purpose registers)
- Eliminates need for software p-code interpreter
- 10 MHz clock
- Approximately 10,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Western Digital |
| Year | 1979 |
| Clock | 10.0 MHz |
| Transistors | ~10,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |

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
   - p-code instructions are complex, requiring multiple microcode cycles
   - Stack operations (push/pop) are fastest at 4 cycles
   - Arithmetic (add/sub/mul) requires 8 cycles of microcode execution
   - Memory indirect load/store costs 6 cycles
   - Procedure call/return is most expensive at 14 cycles (frame setup)
   - Control flow (branch/jump) averages 5 cycles
   - Comparison operations cost 6 cycles
   - Target CPI: ~8.0 (high due to complex p-code instructions)
   - Significant speedup over software p-code interpreter despite high CPI

## Validation Approach

- Compare against original Western Digital WD9000 datasheet
- Validate against UCSD Pascal p-code timing specifications
- Cross-validate with software p-code interpreter performance
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/western_digital/wd9000)
- [Wikipedia](https://en.wikipedia.org/wiki/Pascal_MicroEngine)

---
Generated: 2026-01-29
