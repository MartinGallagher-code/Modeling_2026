# Namco 50xx Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s arcade custom silicon
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Custom 4-bit state machine chip for score and coin handling
- Used in Pac-Man, Galaga, Dig Dug, and related Namco arcade games
- Score calculation (BCD arithmetic)
- Coin counting and credit management
- Fixed command set with command/response protocol to main CPU
- Simple state machine architecture, no pipeline

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Namco |
| Year | 1981 |
| Clock | 1.5 MHz |
| Transistors | ~2,000 |
| Data Width | 4-bit |
| Address Width | 8-bit |

## Queueing Model Architecture

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│   ALU   │──►│  DATA   │──►│   I/O   │──►│ CONTROL │──►│  TIMER  │
│ (score) │   │TRANSFER │   │(coin/dsp)│   │ (state) │   │ (delay) │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue
  3 cyc          4 cyc          6 cyc          5 cyc          7 cyc

CPI = ALU + Data Transfer + I/O + Control + Timer (serial sum)
```

## Operation Categories

| Operation | Cycles | Description |
|-----------|--------|-------------|
| ALU | 3 | Score arithmetic: add/subtract/compare |
| Data Transfer | 4 | Register-to-register data movement |
| I/O | 6 | Coin switch input, display output |
| Control | 5 | State machine transitions |
| Timer | 7 | Timing and delay operations |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The 50xx handles all score tabulation in BCD format
   - Coin switch reads involve I/O latency (6 cycles)
   - Timer operations are the slowest at 7 cycles (used for debounce/delay)
   - Communicates with the main Z80 CPU via a command/response protocol
   - Target CPI is ~5.0 for typical arcade gameplay workloads

## Workload Profiles

| Profile | Description | Dominant Operation |
|---------|-------------|--------------------|
| Typical | Normal gameplay scoring | ALU / I/O |
| Scoring | Heavy scoring activity (bonus rounds) | ALU |
| Coin Handling | Coin insertion and credit management | I/O |
| Idle | Attract mode / idle state | Timer / Control |

## Validation Approach

- Compare against MAME emulation timing analysis
- Validate with Pac-Man/Galaga PCB behavior
- Cross-reference with known score update frame timing
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [MAME Source - Namco 50xx](https://github.com/mamedev/mame/blob/master/src/mame/namco/)
- [Pac-Man Hardware](https://en.wikipedia.org/wiki/Pac-Man_(video_game))

---
Generated: 2026-01-29
