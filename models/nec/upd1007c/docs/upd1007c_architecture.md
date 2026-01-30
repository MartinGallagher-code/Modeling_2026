# NEC uPD1007C Architecture

## Overview

The NEC uPD1007C is a custom 4-bit CMOS calculator CPU produced by NEC Corporation
in 1978. It was designed specifically for Casio's scientific and programmable
calculator product line, featuring native BCD arithmetic and an integrated display
driver for LCD/LED displays.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1978 |
| Manufacturer | NEC Corporation |
| Data Width | 4-bit |
| Clock Speed | 500 kHz |
| Transistors | ~6,000 |
| Technology | CMOS |
| Address Space | 12-bit (4 KB) |
| Package | 42-pin DIP |

## Architecture Details

### 4-bit Data Path

The uPD1007C processes data 4 bits (one BCD digit) at a time. This nibble-oriented
architecture is efficient for decimal arithmetic, as each nibble directly represents
one decimal digit (0-9).

### BCD Arithmetic

Native support for Binary Coded Decimal arithmetic, including:
- Multi-digit BCD addition and subtraction
- Decimal adjust after addition (DAA)
- BCD increment and decrement
- Digit-level comparison operations

### Register File

Internal register file for storing multi-digit BCD numbers. The register file
provides faster access than external memory and holds operands, intermediate
results, and display data.

### Display Driver

Integrated LCD/LED display driver capable of multiplexing segment outputs.
Display operations are the most cycle-intensive category, as the chip must
scan and drive each digit position sequentially.

### Control Logic

- Conditional branching based on flags
- Subroutine call/return with limited stack
- Skip instructions for conditional execution
- Simple loop support

### Low-Power CMOS

The CMOS technology was chosen specifically for battery-operated calculator
applications. CMOS provides significantly lower power consumption than PMOS
or NMOS, enabling longer battery life in handheld devices.

## Products Using uPD1007C

The uPD1007C was used in several Casio calculator models from the late 1970s
through the early 1980s, including:
- Casio fx-series scientific calculators
- Casio programmable calculators
- Various Casio desktop calculator models

## NEC Calculator CPU Family

The uPD1007C is part of NEC's broader calculator CPU family, which includes:
- uPD546 - Earlier 4-bit calculator CPU
- uPD751 - Enhanced 4-bit controller
- uPD1007C - Optimized for Casio calculators
- Later uPD7xxx series - Evolution toward general-purpose microcontrollers
