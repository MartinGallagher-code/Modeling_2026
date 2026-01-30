# General Instrument PIC1650 Architectural Documentation

## Era Classification

**Era:** Pipelined Execution
**Period:** Late 1970s (1977)
**Queueing Model:** Pipeline queueing network

## Architectural Features

- First PIC microcontroller
- Harvard architecture with separate instruction and data memory
- 12-bit instruction width, 8-bit data width
- Most instructions execute in 1 instruction cycle (4 oscillator clocks)
- Branch and call instructions take 2 instruction cycles
- Only 33 instructions total (highly orthogonal)
- 2-level hardware stack
- 512 words x 12-bit ROM
- 32 bytes RAM

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1977 |
| Clock | 0.25 MHz (instruction rate; 1 MHz oscillator / 4) |
| Transistors | ~3,000 |
| Data Width | 8-bit |
| Address Width | 9-bit |

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
   - Harvard architecture enables instruction fetch overlap with execution
   - Single-cycle execution for ALU, data transfer, bit, and literal ops (1 cycle)
   - Branch and call instructions take 2 cycles (pipeline flush)
   - Target CPI of 1.15 reflects ~85% single-cycle, ~15% two-cycle mix
   - 2-level hardware stack limits call depth but is very fast
   - 33 instructions keep decode simple and fast
   - 512-word ROM limits program size but sufficient for embedded control

## Validation Approach

- Compare against original General Instrument datasheet
- Validate with PIC emulator cycle-accurate data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/general_instrument/pic1650)
- [Wikipedia](https://en.wikipedia.org/wiki/PIC_microcontrollers)

---
Generated: 2026-01-29
