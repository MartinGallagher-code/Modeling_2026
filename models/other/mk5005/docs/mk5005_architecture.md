# Mostek MK5005 Architecture

## Overview

The Mostek MK5005 is one of the earliest calculator-on-a-chip integrated circuits,
produced by Mostek Corporation in 1972. Using PMOS technology with approximately
3,000 transistors, it integrates all the logic needed for a basic four-function
calculator onto a single chip.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1972 |
| Manufacturer | Mostek Corporation |
| Data Width | 4-bit (serial) |
| Clock Speed | 200 kHz |
| Transistors | ~3,000 |
| Technology | PMOS |
| Package | 28-pin DIP |

## Architecture Details

### Serial BCD Processing

Like other early calculator chips, the MK5005 uses a serial 4-bit data path that
processes BCD digits one at a time. This minimizes transistor count at the cost of
slower multi-digit operations.

### Shift Register Architecture

All data storage uses recirculating shift registers. Numbers circulate through
the shift registers continuously, with arithmetic operations performed as digits
pass through the ALU. This approach was standard for early 1970s calculator chips
because shift registers were far more area-efficient than static RAM.

### Display Multiplexing

Integrated display driver that multiplexes segment outputs across digit positions.
The display refresh cycle consumes a significant portion of the chip's processing
bandwidth, as each digit must be refreshed frequently enough to avoid visible
flicker.

### Keyboard Scanning

Built-in keyboard matrix scanning logic. The chip polls the keyboard matrix
during display blanking intervals, sharing timing resources between display
refresh and key detection.

### PMOS Technology

The MK5005 uses PMOS (P-channel Metal-Oxide-Semiconductor) technology, which was
the dominant process for LSI circuits in the early 1970s. PMOS offered:
- Simpler fabrication than NMOS
- Lower transistor density
- Slower switching speeds
- Higher power consumption per gate

The slow PMOS technology contributes to the high cycle counts across all
instruction categories.

## Historical Context

Mostek was founded in 1969 by former TI engineers and became a significant player
in the calculator chip market. The MK5005 competed with TI's TMS0100/TMS0200
series and other early calculator chips from companies like General Instrument,
National Semiconductor, and Rockwell.

The calculator-on-a-chip revolution of the early 1970s dramatically reduced
calculator costs, making electronic calculators affordable for consumers for
the first time.

## Related Mostek Products

- MK5005 - Basic four-function calculator
- MK5017 - Enhanced calculator with memory
- MK5020 - Scientific function calculator
- MK5025 - Programmable calculator chip
