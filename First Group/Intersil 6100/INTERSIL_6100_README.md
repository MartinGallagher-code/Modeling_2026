# Intersil 6100 CPU Queueing Model

## Executive Summary

The Intersil 6100 (1974) was a **PDP-8 minicomputer on a single chip** - one of the first CMOS microprocessors ever made. It was fully compatible with DEC's popular PDP-8 minicomputer, allowing existing software to run on a single-chip processor.

**Key Finding:** The 6100 represents an alternative approach to microprocessor design: instead of creating a new architecture, put an existing successful architecture on a chip. This guaranteed software compatibility but limited architectural innovation.

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Year | 1974 |
| Word Size | **12 bits** (PDP-8) |
| Address Space | 4K words (32K extended) |
| Clock | 4 MHz |
| Technology | **CMOS** |
| ISA | **PDP-8 compatible** |

---

## The PDP-8 Connection

### What Was PDP-8?
```
DEC PDP-8 (1965):
- First successful minicomputer
- 12-bit architecture
- ~50,000 sold
- Huge software library
- Used in labs, industry, education

The 6100 was a single-chip PDP-8!
```

### Why 12 Bits?
```
The PDP-8 used 12-bit words because:
- 12 bits = 4096 addresses (enough for 1965)
- 12 bits = 4 octal digits (easy display)
- Smaller than 16-bit = cheaper

The 6100 inherited this unusual word size.
```

---

## CMOS Pioneer

The 6100 was one of the **first CMOS microprocessors**:

| Advantage | Benefit |
|-----------|---------|
| Low power | Battery operation |
| Static | Can halt clock |
| Rad-tolerant | Military/space use |
| Low heat | No cooling needed |

---

## DEC VT78 Terminal

The most famous 6100 application was the DEC VT78:
```
VT78 (1978):
- Video terminal with built-in computer!
- Intersil 6100 CPU
- Could run PDP-8 software locally
- OS/78 operating system
- BASIC interpreter

A "smart terminal" decades before PCs.
```

---

## Architecture (PDP-8)

### Registers
```
AC: 12-bit Accumulator
MQ: 12-bit Multiplier Quotient
PC: 12-bit Program Counter
L:  1-bit Link (carry)

Only 3 registers! Very simple.
```

### Instruction Format
```
12-bit instruction word:
  Bits 0-2:  Opcode
  Bit 3:     Indirect flag
  Bit 4:     Page 0/Current flag
  Bits 5-11: Address

Only 8 basic opcodes!
```

---

## Legacy

### Impact
- Proved minicomputer could fit on chip
- Showed CMOS viability for microprocessors
- Enabled portable PDP-8 systems
- Military/space applications

### Limitation
- 12-bit architecture was dead end
- Industry chose 8-bit and 16-bit
- PDP-8 software base declined

---

## Conclusion

The Intersil 6100 was a technological achievement - a complete minicomputer on one chip using advanced CMOS technology. But it also showed the limits of backward compatibility: the 12-bit PDP-8 architecture couldn't compete with newer 8-bit and 16-bit designs that didn't carry legacy constraints.

**Lesson:** Compatibility has value, but architecture matters for the long term.

---

**Version:** 1.0 | **Date:** January 24, 2026
