# Namco 53xx Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s arcade custom silicon
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Custom 4-bit input multiplexer chip
- Simplest of the Namco custom chip family (~1,500 transistors)
- Multiplexes multiple input sources to main CPU
- Channel selection and data routing
- Used in Pole Position, Phozon, and related Namco arcade boards
- Fixed-function state machine with minimal complexity

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Namco |
| Year | 1981 |
| Clock | 1.5 MHz |
| Transistors | ~1,500 |
| Data Width | 4-bit |
| Address Width | 8-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│   MUX   │──►│  DATA   │──►│   I/O   │──►│ CONTROL │──►│ TIMING  │
│ SELECT  │   │TRANSFER │   │         │   │ (state) │   │ (sync)  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue
  3 cyc          3 cyc          5 cyc          4 cyc          5 cyc

CPI = Mux Select + Data Transfer + I/O + Control + Timing (serial sum)
```

## Operation Categories

| Operation | Cycles | Description |
|-----------|--------|-------------|
| Mux Select | 3 | Multiplexer channel selection |
| Data Transfer | 3 | Data routing between channels |
| I/O | 5 | Input/output operations |
| Control | 4 | State and mode control |
| Timing | 5 | Synchronization timing |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The 53xx is the simplest Namco custom chip at only ~1,500 transistors
   - Mux select and data transfer are equally fast (3 cycles each), reflecting the chip's simple routing function
   - I/O and timing operations are slower (5 cycles) due to external synchronization requirements
   - The chip primarily acts as a data router between multiple input sources and the main CPU
   - Target CPI is ~4.0 for typical multiplexing workloads

## Workload Profiles

| Profile | Description | Dominant Operation |
|---------|-------------|--------------------|
| Typical | Standard multiplexing operation | I/O / Mux Select / Data Transfer |
| High Throughput | Fast channel switching | Mux Select / Data Transfer |
| Idle | Waiting state | Timing / Control |

## Validation Approach

- Compare against MAME emulation timing analysis
- Validate with Pole Position/Phozon input handling behavior
- Cross-reference with multiplexer channel switching timing
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [MAME Source - Namco 53xx](https://github.com/mamedev/mame/blob/master/src/mame/namco/)
- [Pole Position Hardware](https://en.wikipedia.org/wiki/Pole_Position)

---
Generated: 2026-01-29
