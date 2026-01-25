# Zilog Z80 Peripheral Chips Reference

## Overview

The Z80 wasn't just a CPU - Zilog created a complete **family of compatible peripheral chips** that worked seamlessly together. These chips are NOT processors, so they don't have performance models, but understanding them is essential for understanding Z80 systems.

**Note:** This is a reference document, not a queueing model. These are I/O and support chips, not CPUs.

---

## The Z80 Family

```
                    ┌─────────────────────────────────────────┐
                    │              Z80 SYSTEM                 │
                    │                                         │
    ┌───────────────┼───────────────────────────────────────┐ │
    │               │                                       │ │
    │  ┌────────┐   │   ┌────────┐   ┌────────┐            │ │
    │  │  Z80   │◄──┼──►│  Z80   │   │  Z80   │            │ │
    │  │  CPU   │   │   │  PIO   │   │  SIO   │            │ │
    │  └────────┘   │   └────────┘   └────────┘            │ │
    │       │       │        │            │                │ │
    │       │       │   ┌────────┐   ┌────────┐            │ │
    │       │       │   │  Z80   │   │  Z80   │            │ │
    │       └───────┼──►│  CTC   │   │  DMA   │            │ │
    │               │   └────────┘   └────────┘            │ │
    │               │                                       │ │
    │    Common Bus (active low, directly compatible)       │ │
    └───────────────┴───────────────────────────────────────┘ │
                    │     All chips share:                    │
                    │     - Same power (+5V)                  │
                    │     - Same clock                        │
                    │     - Same bus timing                   │
                    │     - Directly compatible               │
                    └─────────────────────────────────────────┘
```

---

## Z80-PIO: Parallel Input/Output

### Purpose
General-purpose parallel I/O with handshaking and interrupts.

### Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| I/O Ports | 2 × 8-bit (Port A, Port B) |
| Modes | Byte I/O, Bit I/O, Bidirectional |
| Interrupts | Fully vectored, daisy-chain |
| Package | 40-pin DIP |

### Operating Modes

```
Mode 0: Byte Output
  - All 8 bits output
  - Directly drive LEDs, latches, etc.

Mode 1: Byte Input
  - All 8 bits input
  - Read switches, sensors, etc.

Mode 2: Bidirectional (Port A only)
  - 8-bit bidirectional with handshaking
  - For communication with other devices

Mode 3: Bit I/O
  - Each bit individually input or output
  - Maximum flexibility
```

### Typical Applications
- Keyboard interface
- Printer parallel port
- Switch/LED panels
- General I/O expansion

---

## Z80-SIO: Serial Input/Output

### Purpose
Dual-channel serial communication (like two UARTs).

### Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| Channels | 2 independent |
| Modes | Async, Sync, SDLC/HDLC |
| Baud rate | Up to 1 Mbps (sync) |
| Interrupts | Fully vectored, per-channel |
| Package | 40-pin DIP |

### Variants
| Chip | Description |
|------|-------------|
| Z80-SIO/0 | Standard dual-channel |
| Z80-SIO/1 | Variant with different pinout |
| Z80-SIO/2 | Variant with different pinout |
| Z80-DART | Async-only version (simpler) |

### Operating Modes

```
Asynchronous:
  - Standard UART operation
  - 5-8 data bits, 1-2 stop bits
  - Odd/even/no parity
  - For terminals, modems, etc.

Synchronous (Byte):
  - External clock synchronization
  - For high-speed sync protocols

SDLC/HDLC:
  - Bit-oriented protocol support
  - Automatic CRC generation/checking
  - For networking (X.25, etc.)
```

### Typical Applications
- Terminal connections (RS-232)
- Modem interfaces
- Serial printers
- Computer-to-computer links
- Network interfaces (SDLC)

---

## Z80-CTC: Counter/Timer Circuit

### Purpose
Four independent counter/timer channels for timing and counting.

### Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| Channels | 4 independent |
| Counter size | 8-bit each |
| Modes | Timer, Counter |
| Prescaler | ÷16 or ÷256 |
| Interrupts | Fully vectored, per-channel |
| Package | 28-pin DIP |

### Operating Modes

```
Timer Mode:
  - Counts down from loaded value
  - Triggered by CPU clock (prescaled)
  - Generates interrupt at zero
  - Use: Periodic interrupts, timing

Counter Mode:
  - Counts external events
  - Edge-triggered input
  - Generates interrupt at zero
  - Use: Event counting, frequency measurement
```

### Typical Applications
- Baud rate generation (for SIO)
- Real-time clock interrupts
- Event counting
- Pulse width measurement
- Watchdog timer

### Baud Rate Generation Example
```
CPU Clock: 4 MHz
CTC Prescaler: ÷16
CTC Count: 13

Output frequency: 4,000,000 / 16 / 13 = 19,231 Hz
Baud rate (÷16): 19,231 / 16 = 1,202 baud (≈1200 baud)
```

---

## Z80-DMA: Direct Memory Access

### Purpose
High-speed data transfer without CPU involvement.

### Specifications
| Spec | Value |
|------|-------|
| Year | 1976 |
| Transfer rate | Up to 1.25 MB/sec |
| Modes | Memory↔Memory, Memory↔I/O |
| Addressing | 16-bit (64KB) |
| Block size | Up to 64KB |
| Search | Byte search capability |
| Package | 40-pin DIP |

### Operating Modes

```
Byte-at-a-time:
  - CPU can interleave with DMA
  - Slower but allows CPU to continue

Burst Mode:
  - DMA takes bus until complete
  - Fastest transfer rate

Continuous Mode:
  - Like burst, for streaming

Search Mode:
  - Scan memory for byte match
  - Stop when found
```

### Typical Applications
- Floppy disk controller interface
- High-speed serial data capture
- Memory-to-memory block moves
- CRT display refresh
- Network packet handling

---

## Interrupt System: Daisy Chain

### How It Works

All Z80 peripherals use a **daisy-chain** interrupt scheme:

```
        IEI (Interrupt Enable In)
           │
    ┌──────┴──────┐
    │   Z80-PIO   │ ◄── Highest priority
    │   (or any)  │
    └──────┬──────┘
           │ IEO (Interrupt Enable Out)
    ┌──────┴──────┐
    │   Z80-SIO   │ ◄── Medium priority
    │             │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │   Z80-CTC   │ ◄── Lower priority
    │             │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │   Z80-DMA   │ ◄── Lowest priority
    │             │
    └─────────────┘

When a chip is servicing an interrupt, it blocks
IEO, preventing lower-priority chips from interrupting.
```

### Interrupt Modes

The Z80 CPU has three interrupt modes:

| Mode | Vector | Description |
|------|--------|-------------|
| IM 0 | External | 8080 compatible, external vector |
| IM 1 | Fixed | Always jumps to 0038h |
| **IM 2** | **Vectored** | **Peripheral provides vector (Z80 mode)** |

**IM 2** is the native Z80 mode where peripherals provide their own interrupt vectors, allowing direct jumps to specific handlers.

---

## Complete Z80 System Example

### Typical CP/M Computer

```
┌─────────────────────────────────────────────────────────────┐
│                     CP/M Computer                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐        │
│  │  Z80   │   │  Z80   │   │  Z80   │   │  Z80   │        │
│  │  CPU   │   │  SIO   │   │  CTC   │   │  PIO   │        │
│  │        │   │(serial)│   │(timing)│   │(printer│        │
│  │ 4 MHz  │   │        │   │        │   │  port) │        │
│  └────────┘   └────────┘   └────────┘   └────────┘        │
│       │            │            │            │              │
│       └────────────┴────────────┴────────────┘              │
│                         │                                   │
│                    System Bus                               │
│                         │                                   │
│       ┌─────────────────┼─────────────────┐                │
│       │                 │                 │                │
│  ┌────────┐       ┌────────┐       ┌────────┐             │
│  │  64KB  │       │ Floppy │       │  Boot  │             │
│  │  RAM   │       │  Disk  │       │  ROM   │             │
│  │        │       │ (FDC)  │       │  (2KB) │             │
│  └────────┘       └────────┘       └────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Connections:
- SIO Channel A → Terminal (RS-232)
- SIO Channel B → Modem (RS-232)
- CTC Channel 0 → SIO Clock (baud rate)
- CTC Channel 1 → SIO Clock (baud rate)
- CTC Channel 2 → Real-time clock interrupt
- PIO Port A → Printer (Centronics parallel)
- PIO Port B → Front panel switches/LEDs
```

---

## Why This Family Was Successful

### 1. Complete Compatibility
All chips designed together:
- Same bus timing
- Same interrupt scheme
- Same voltage (+5V only)
- Same clock requirements
- Direct connection, no glue logic

### 2. Powerful Features
Each chip was the best in class:
- SIO: HDLC support (networking)
- CTC: Multiple independent channels
- DMA: Search capability
- PIO: Flexible bit/byte modes

### 3. Reduced System Cost
One Z80 + PIO + SIO + CTC could replace:
- Intel 8080 + 8228 + 8224 + 8255 + 8251 + 8253
- Fewer chips = lower cost, higher reliability

---

## Comparison to Intel Equivalents

| Function | Zilog | Intel | Notes |
|----------|-------|-------|-------|
| CPU | Z80 | 8080/8085 | Z80 better |
| Parallel I/O | Z80-PIO | 8255 | Similar |
| Serial I/O | Z80-SIO | 8251 | SIO has HDLC |
| Timer | Z80-CTC | 8253/8254 | CTC has interrupts |
| DMA | Z80-DMA | 8237 | DMA has search |
| System | 4 chips | 6+ chips | Zilog simpler |

---

## Legacy

The Z80 peripheral family design influenced:
- Later Zilog chips (Z8000, Z180 peripherals)
- ARM's AMBA bus philosophy
- Modern SoC peripheral integration

The concept of a **designed-together chip family** rather than individual chips was revolutionary in 1976.

---

## Files in This Directory

| File | Description |
|------|-------------|
| `Z80_PERIPHERALS_README.md` | This document |
| `QUICK_START_Z80_PERIPHERALS.md` | Quick reference |
| `PROJECT_SUMMARY.md` | Executive summary |

**Note:** No Python model or JSON config - these are not CPUs.

---

**Version:** 1.0  
**Date:** January 24, 2026

*"The Z80 family: designed together, work together."*
