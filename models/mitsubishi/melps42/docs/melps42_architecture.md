# Mitsubishi MELPS 42 Architectural Documentation

## Era Classification

**Era:** Sequential Execution
**Period:** 1983
**Queueing Model:** Serial M/M/1 chain

## Architectural Features

- 4-bit microcontroller, CMOS version of the MELPS 4 family
- CMOS technology for low power consumption
- 1 MHz clock (doubled from MELPS 41's 500 kHz)
- Further improved instruction timing over NMOS predecessor
- Designed for battery-powered and low-power embedded devices
- 4 KB ROM addressable via 12-bit address

## Processor Specifications

| Parameter | Value |
|-----------|-------|
| Manufacturer | Mitsubishi |
| Year | 1983 |
| Clock | 1.0 MHz |
| Transistors | 10,000 |
| Data Width | 4-bit |
| Address Width | 12-bit |

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

## Instruction Timing

| Category | Cycles | Description |
|----------|--------|-------------|
| ALU | 3 | ADD, SUB, logical operations |
| Data Transfer | 4 | Register-memory transfers |
| Memory | 6 | Load/store operations |
| I/O | 7 | Input/output operations |
| Control | 5 | Branch, call, return |

**Target CPI:** 5.0 (typical workload, improved CMOS timing)

## Model Implementation Notes

1. This processor uses the **Sequential Execution** architectural template
2. Key modeling considerations:
   - CMOS technology reduces ALU cycles from 4 to 3, data transfer from 5 to 4 compared to NMOS MELPS 41
   - Memory and I/O cycles remain at 6 and 7 respectively (unchanged from MELPS 41)
   - Control flow improved from 5.5 to integer 5 cycles
   - 1 MHz clock with CPI 5.0 yields 200,000 IPS (a 3x improvement over original MELPS 4)
   - Low power CMOS makes this suitable for battery-powered consumer devices
   - Transistor count increased to 10,000 reflecting CMOS logic density improvements

## MELPS 4 Family Evolution

| Model | Year | Technology | Clock | CPI | IPS |
|-------|------|-----------|-------|-----|-----|
| MELPS 4 | 1978 | PMOS | 400 kHz | 6.0 | ~66,667 |
| MELPS 41 | 1980 | NMOS | 500 kHz | 5.5 | ~90,909 |
| MELPS 42 | 1983 | CMOS | 1 MHz | 5.0 | ~200,000 |

## Validation Approach

- Compare against original Mitsubishi datasheet timing specifications
- Cross-validate improvement ratios against MELPS 4 and MELPS 41 models
- Validate with cycle-accurate emulator (if available)
- Target: <5% IPC prediction error

## References

- [Original Datasheet](TODO: Add link)
- [WikiChip](https://en.wikichip.org/wiki/mitsubishi/melps)
- [Wikipedia](https://en.wikipedia.org/wiki/Mitsubishi_MELPS)

---
Generated: 2026-01-29
