# Intel 8096 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s 16-bit microcontroller era
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 16-bit register-based architecture (not accumulator-based)
- 232-byte register file (addresses 00h-E7h) with 8 dedicated registers
- Hardware 16x16->32 multiply and 32/16->16 divide
- On-chip PWM generator for motor control
- On-chip A/D converter for sensor input
- Serial port, timers, and watchdog timer
- Dominated automotive applications from 1985 to 2005
- State-time based execution: each state = 3 clock cycles

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel |
| Year | 1982 |
| Clock | 12.0 MHz |
| Transistors | ~120,000 (CHMOS version) |
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

The 8096 uses state-time-based execution where each state time equals 3 clock
cycles. Register operations take 2-4 state times, memory operations 3-6 state
times, and hardware multiply/divide 6-12 state times.

## Instruction Categories

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 2.9 | ADD/SUB/AND/OR/XOR register-to-register |
| Memory | 4.5 | LD/ST indirect memory access |
| Multiply | 6.0 | MUL 16x16->32 hardware multiplier |
| Divide | 12.0 | DIV 32/16->16 hardware divider |
| Branch | 4.0 | JMP/CALL/RET control flow |
| Peripheral | 4.0 | PWM/ADC/Timer SFR access |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Register-file architecture gives faster operand access than accumulator designs
   - Hardware multiply (6 cycles) and divide (12 cycles) are critical for automotive math
   - State time granularity (3 clocks per state) means timing is coarser than cycle-level
   - Peripheral access (PWM, ADC, timers) is modeled as SFR register operations
   - The fuel injection workload profile exercises multiply/divide heavily (20% combined)
   - Target CPI of 4.0 reflects typical automotive control loop execution
   - Short jumps execute faster than long jumps (3 vs 4 cycles)

## Validation Approach

- Compare against original Intel 8096 datasheet timing tables
- Validate with cycle-accurate emulator (if available)
- Cross-check hardware multiply/divide timing against documentation
- Target: <5% CPI prediction error (target CPI = 4.0)

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/intel/mcs-96)
- [Wikipedia](https://en.wikipedia.org/wiki/Intel_MCS-96)

---
Generated: 2026-01-29
