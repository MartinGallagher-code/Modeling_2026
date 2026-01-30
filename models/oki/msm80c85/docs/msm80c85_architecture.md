# OKI MSM80C85 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- CMOS second-source implementation of Intel 8085
- 8-bit data path with 16-bit address bus
- Low-power CMOS technology for portable applications
- Full 8085 instruction set compatibility
- Sequential execution with no pipeline
- 5 MHz clock
- Pin-compatible with Intel 8085

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | OKI |
| Year | 1983 |
| Clock | 5.0 MHz |
| Transistors | ~6,500 |
| Data Width | 8-bit |
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
   - 8085-compatible timing: ALU and data transfer at 4 cycles each
   - Memory at 7 cycles; control flow at 7 cycles
   - Stack operations (push/pop) slowest at 10 cycles
   - CMOS technology provides lower power but same timing as NMOS 8085
   - Cross-validation against Intel 8085 timing data
   - Used in portable/battery-powered systems where CMOS power savings matter

## Validation Approach

- Compare against original OKI datasheet
- Cross-validate against Intel 8085 timing (should be identical)
- Validate with cycle-accurate 8085 emulator
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/oki)
- [Wikipedia](https://en.wikipedia.org/wiki/Intel_8085)

---
Generated: 2026-01-29
