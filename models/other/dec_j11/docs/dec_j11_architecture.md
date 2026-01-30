# DEC J-11 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Early 1980s (1983)
**Queueing Model:** Pipeline queueing network

## Architectural Features

- Fastest PDP-11 microprocessor implementation
- Pipelined architecture for improved throughput
- 175,000 transistors
- 22-bit addressing (4 MB address space)
- Full PDP-11 instruction set
- Used in PDP-11/73 and PDP-11/84 systems
- 15 MHz clock speed

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | DEC |
| Year | 1983 |
| Clock | 15.0 MHz |
| Transistors | 175,000 |
| Data Width | 16-bit |
| Address Width | 22-bit |

## Queueing Model Architecture

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│  IF  │─►│  ID  │─►│  OF  │─►│  EX  │─►│  WB  │
└──────┘  └──────┘  └──────┘  └──────┘  └──────┘
   │         │         │         │         │
   I1        I1        I1        I1        I1
             I2        I2        I2        I2

Ideal CPI = 1.0
Actual CPI = 1.0 + hazards + stalls + cache_misses
```

## Model Implementation Notes

1. This processor uses the **Pipelined Execution** architectural template
2. Key modeling considerations:
   - Target CPI of 4.0 despite pipelining (CISC overhead)
   - ALU and data transfer operations are fastest at 3 cycles
   - Memory and control operations take 5 cycles
   - Stack operations are most expensive at 5.5 cycles
   - PDP-11's complex addressing modes add execution overhead
   - Pipeline stalls from variable-length instructions

## Validation Approach

- Compare against original DEC J-11 datasheet
- Validate with PDP-11/73 benchmark data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/J-11)

---
Generated: 2026-01-29
