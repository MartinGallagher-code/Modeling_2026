# GI AY-3-8900 STIC Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s (1978)
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- Standard Television Interface Chip (STIC) for Mattel Intellivision
- 8 hardware sprites with collision detection
- Background tile rendering
- 16-bit data path with 14-bit addressing
- Display synchronization and timing generation

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | General Instrument |
| Year | 1978 |
| Clock | 3.58 MHz |
| Transistors | 8,000 |
| Data Width | 16-bit |
| Address Width | 14-bit |

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
   - Sprite and background operations are medium cost at 5 cycles each
   - Collision detection is expensive at 7 cycles (hardware pixel comparison)
   - Display sync is most expensive at 8 cycles (timing-critical)
   - Workload is balanced between sprite, background, collision, and sync
   - Works in tandem with CP1600 CPU in the Intellivision

## Validation Approach

- Compare against original General Instrument AY-3-8900 STIC datasheet
- Validate with Intellivision emulator timing data
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [Wikipedia](https://en.wikipedia.org/wiki/Standard_Television_Interface_Chip)

---
Generated: 2026-01-29
