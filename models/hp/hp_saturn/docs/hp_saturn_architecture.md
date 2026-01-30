# HP Saturn Architecture

## Overview

The HP Saturn is a custom CMOS CPU designed by Hewlett-Packard specifically for their
calculator product line. First introduced in 1984, it powered the HP 71B and later the
iconic HP 48 and HP 49 series scientific calculators.

## Key Specifications

| Parameter | Value |
|-----------|-------|
| Year | 1984 |
| Manufacturer | Hewlett-Packard |
| Data Width | 4-bit (nibble-serial) |
| Register Width | 64-bit (16 nibbles) |
| Address Space | 20-bit (1 MB) |
| Clock Speed | 640 kHz (original); up to 4 MHz (later) |
| Transistors | ~40,000 |
| Technology | CMOS |

## Architecture Details

### Nibble-Serial Design

Saturn uses a 4-bit data path but operates on 64-bit registers by processing them
nibble by nibble (16 steps). This allows large register widths with minimal silicon
area, at the cost of multi-cycle operations for wide fields.

### Register Set

- **A, B, C, D**: Four 64-bit working registers (16 nibbles each)
- **D0, D1**: Two 20-bit data pointer registers
- **PC**: 20-bit program counter
- **R0-R4**: Five 64-bit scratch registers
- **ST**: 16-bit status register
- **P**: 4-bit pointer register (field selector)

### Field Access

Saturn instructions can operate on sub-fields of the 64-bit registers:
- **W** (Word): All 16 nibbles
- **A** (Address): Nibbles 0-4 (20 bits)
- **B** (Byte): Nibbles 0-1 (8 bits)
- **X** (Exponent): Nibbles 0-2 (12 bits)
- **S** (Sign): Nibble 15
- **M** (Mantissa): Nibbles 3-14
- **P/WP**: Pointer-selected nibble(s)

### BCD Arithmetic

Native BCD (Binary Coded Decimal) arithmetic support provides the decimal precision
required for calculator applications. Each nibble stores one decimal digit (0-9).

### Memory Access

Memory is accessed through two pointer registers (D0, D1). Load/store operations
transfer data between registers and memory via these pointers. Memory access is
relatively expensive due to the external bus interface.

### Instruction Encoding

Variable-length instructions from 2 to 21 nibbles. The first nibble(s) determine
the instruction type and subsequent nibbles provide operands, addresses, or field
specifiers.

## Products Using Saturn

- HP 71B (1984) - First Saturn-based calculator
- HP 48S/SX (1990) - Scientific graphing calculator
- HP 48G/GX (1993) - Enhanced graphing calculator
- HP 49G (1999) - Advanced graphing calculator (Sacajawea variant)

## Saturn Variants

| Variant | Year | Clock | Notes |
|---------|------|-------|-------|
| Original | 1984 | 640 kHz | HP 71B |
| Clarke | 1990 | 2 MHz | HP 48SX |
| Yorke | 1993 | 4 MHz | HP 48GX |
| Lewis | 1995 | 4 MHz | HP 38G |
| Sacajawea | 1999 | 4 MHz | HP 49G (ARM+Saturn emulation) |
