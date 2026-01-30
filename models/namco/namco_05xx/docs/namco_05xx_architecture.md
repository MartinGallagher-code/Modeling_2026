# Namco 05xx Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Early 1980s arcade custom silicon
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Custom 4-bit starfield generator chip
- Produces iconic parallax scrolling starfield backgrounds (Galaga, Bosconian)
- Star position calculation engine
- Pixel data output to video hardware
- Scroll offset management for multi-layer parallax effect
- Fixed-function state machine architecture (no general-purpose instruction set)

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
│STAR CALC│──►│PIXEL OUT│──►│ SCROLL  │──►│ CONTROL │──►│ TIMING  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
  M/M/1          M/M/1          M/M/1          M/M/1          M/M/1
  Queue          Queue          Queue          Queue          Queue
  3 cyc          4 cyc          4 cyc          3 cyc          5 cyc

CPI = Star Calc + Pixel Out + Scroll + Control + Timing (serial sum)
```

## Operation Categories

| Operation | Cycles | Description |
|-----------|--------|-------------|
| Star Calc | 3 | Star position calculation |
| Pixel Out | 4 | Pixel data output to video |
| Scroll | 4 | Scroll offset update for parallax |
| Control | 3 | State machine control |
| Timing | 5 | Video sync timing |

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - The 05xx is a fixed-function chip, not a general-purpose processor
   - All operations are pixel-driven, tied to video timing
   - Star position calculations dominate during dense starfield scenes
   - Timing operations synchronize output with the CRT raster
   - Target CPI is ~4.0 for typical starfield rendering workloads

## Workload Profiles

| Profile | Description | Dominant Operation |
|---------|-------------|--------------------|
| Typical | Standard starfield rendering during gameplay | Star Calc / Pixel Out |
| Dense Field | Many visible stars on screen | Star Calc / Pixel Out |
| Scrolling | Heavy parallax movement | Scroll |
| Idle | Static display or blanked screen | Timing / Control |

## Validation Approach

- Compare against MAME emulation timing analysis
- Validate with video output frame timing measurements
- Cross-reference with Galaga/Bosconian PCB analysis
- Target: <5% CPI prediction error

## References

- [Original Datasheet](TODO: Add link)
- [MAME Source - Namco 05xx](https://github.com/mamedev/mame/blob/master/src/mame/namco/)
- [Galaga Hardware](https://en.wikipedia.org/wiki/Galaga)

---
Generated: 2026-01-29
