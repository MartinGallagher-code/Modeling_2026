# AMI S28211 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** Late 1970s DSP Peripherals
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- DSP peripheral chip designed for the Motorola 6800 bus (1979)
- NMOS technology with 8 MHz clock
- 16-bit data path for signal processing arithmetic
- Bus-attached coprocessor architecture (not standalone)
- Multiply-accumulate operations for filter computations
- 6800 bus interface for host CPU communication
- Designed to add DSP capability to existing 6800-based systems
- Approximately 5,000 transistors

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | American Microsystems Inc. (AMI) |
| Year | 1979 |
| Clock | 8.0 MHz |
| Transistors | ~5,000 |
| Data Width | 16-bit |
| Address Width | 16-bit |
| Technology | NMOS |
| Package | 40-pin DIP |
| Target Application | DSP coprocessor for Motorola 6800 systems |

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

The S28211 uses a serial execution model. As a bus-attached peripheral, it adds
I/O overhead from the 6800 bus interface that standalone processors would not have.
The model uses five instruction categories: MAC (4 cycles), ALU (3 cycles),
data move (4 cycles), control (6 cycles), and I/O (8 cycles). The I/O category
is notably expensive due to the 6800 bus handshake protocol overhead.

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - Bus-attached coprocessor architecture adds significant I/O overhead (8 cycles for bus operations)
   - ALU operations are the fastest at 3 cycles, reflecting the NMOS speed advantage
   - MAC (multiply-accumulate) operations take 4 cycles -- no dedicated hardware MAC unit
   - Data move operations also take 4 cycles due to bus interface arbitration
   - Control flow operations take 6 cycles due to microcode branching overhead
   - Target CPI of 5.0 is lower than the S2811 (8.0) due to the faster clock and more efficient design
   - The 6800 bus interface is a key bottleneck: I/O-heavy workloads see CPI rise significantly
   - 16-bit data width (vs S2811's 12-bit) provides improved signal processing precision
   - 8 MHz clock is double the S2811's 4 MHz, reflecting NMOS process improvements
   - As a peripheral, the S28211 depends on the host 6800 CPU for program sequencing

## Validation Approach

- Compare against original AMI S28211 datasheet timing specifications
- Validate bus interface overhead against Motorola 6800 bus timing specs
- Cross-reference with S2811 timings for architectural consistency
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error
- Expected IPS at 8 MHz: ~1,600,000 instructions per second

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/ami/s28211)
- [Wikipedia](https://en.wikipedia.org/wiki/AMI_S28211)
- Motorola 6800 Bus Interface Specification
- AMI S28211 DSP Peripheral Technical Reference Manual

---
Generated: 2026-01-29
