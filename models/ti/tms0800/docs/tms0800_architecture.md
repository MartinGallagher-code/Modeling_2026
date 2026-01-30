# TI TMS0800 Architecture

## Overview

The TI TMS0800 is a single-chip PMOS calculator integrated circuit produced by
Texas Instruments in 1973. It represents the second generation of TI's calculator
chip family, following the TMS0100 series. It was used in various TI desktop and
portable calculators for four-function arithmetic.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1973 |
| Manufacturer | Texas Instruments |
| Data Width | 4-bit (serial) |
| Clock Speed | 300 kHz |
| Transistors | ~5,000 |
| Technology | PMOS |
| Package | 28-pin DIP |

## Architecture Details

### Serial BCD Data Path

The TMS0800 uses a 4-bit serial data path that processes BCD (Binary Coded Decimal)
digits one at a time. Multi-digit numbers are stored in shift registers, with each
digit occupying 4 bits. Operations process digits serially from least significant
to most significant.

### Shift Register Storage

Data is stored in recirculating shift registers rather than random-access memory.
This was common in early calculator chips as shift registers required fewer
transistors than RAM cells. The registers can hold multiple BCD digits for
operands and results.

### Display Interface

Integrated display scanning and segment driving logic. The chip directly drives
LED or VFD (Vacuum Fluorescent Display) segments through multiplexed outputs.
Display refresh occurs continuously and consumes a significant portion of the
processing time.

### Hardwired Control

Unlike later programmable microcontrollers, the TMS0800 uses hardwired control
logic for its four-function arithmetic (add, subtract, multiply, divide). This
makes the chip specialized for calculator operations but not general-purpose
programmable.

### Keyboard Interface

Integrated keyboard scanning logic that polls a matrix keyboard for key presses.
The scan operates alongside display refresh in a time-multiplexed fashion.

## Calculator Products

The TMS0800 was used in several TI desktop and portable calculators in the
1973-1975 timeframe, including basic four-function models. It was eventually
superseded by the more advanced TMS1000 microcontroller family which offered
programmability.

## Relationship to TMS1000

The TMS0800 is a direct predecessor to the TMS1000 series. While the TMS0800 is a
dedicated calculator chip, the TMS1000 (1974) evolved into a general-purpose
microcontroller with programmable ROM, making it suitable for a wider range of
applications beyond calculators.
