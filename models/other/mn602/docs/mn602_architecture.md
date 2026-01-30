# Data General mN602 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s (1982)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Enhanced microNova processor, successor to mN601
- Accumulator-based architecture (Data General Nova lineage)
- 16-bit data path
- 15-bit address space (32K words)
- Improved over mN601 with more transistors and features
- Sequential execution with no pipeline
- 4 MHz clock

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Data General |
| Year | 1982 |
| Clock | 4.0 MHz |
| Transistors | ~15,000 |
| Data Width | 16-bit |
| Address Width | 15-bit |

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
   - ALU and data transfer at 3.5 cycles each (accumulator architecture)
   - Memory at 6.0 cycles; control and stack at 7.0 cycles each
   - Target CPI of 5.0 reflects enhanced but still sequential design
   - 15-bit address width limits to 32K word address space
   - Maintains Nova compatibility while adding features
   - Higher CPI than mN601 due to more complex instruction encoding

## Validation Approach

- Compare against original Data General datasheet
- Cross-validate against mN601 and Nova performance data
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/data_general)
- [Wikipedia](https://en.wikipedia.org/wiki/Data_General_microNova)

---
Generated: 2026-01-29
