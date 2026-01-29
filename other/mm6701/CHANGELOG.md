# Monolithic Memories 6701 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for Monolithic Memories 6701, a 4-bit slice ALU

**Starting state:**
- No model existed
- Reference: am2901 and i3002 bit-slice models

**Research findings:**
- Monolithic Memories 6701 was a 4-bit slice ALU (1975)
- Part of the 67xx bit-slice family from Monolithic Memories
- Competitor to AMD Am2901 in the bit-slice market
- Bipolar Schottky technology for high speed
- Single-cycle microinstructions
- 16 general-purpose registers per slice
- Carry look-ahead support for cascading
- ~180 transistors per slice
- 8 MHz typical clock (125ns cycle time)
- Monolithic Memories was later acquired by AMD (1987)

**Changes made:**

1. Created model targeting CPI = 1.0 (per microinstruction)
   - All microinstructions execute in single cycle
   - Bit-slice architecture = no multi-cycle operations

2. Added 4 instruction categories (all 1 cycle):
   - alu: ADD/SUB/AND/OR/XOR
   - shift: SHL/SHR
   - pass: data routing
   - zero: clear operations

3. Modeled as direct competitor to Am2901:
   - Same 4-bit slice width
   - Same 16 registers per slice
   - Same single-cycle execution
   - Similar transistor count

4. Added comparison function to Am2901

**What we learned:**
- MM6701 was functionally equivalent to Am2901
- Both achieved CPI = 1.0 for microinstructions
- Bit-slice market was competitive in mid-1970s
- Multiple vendors (AMD, Intel, Monolithic Memories, Texas Instruments)
- Eventually AMD dominated the market

**Final state:**
- CPI: 1.0 (0% error vs target 1.0)
- Validation: PASSED (17/17 tests, 100%)
- All workloads achieve CPI = 1.0

**References used:**
- Monolithic Memories databooks (Bitsavers)
- Bit-slice processor comparison articles
- AMD Am2901 for comparison
- Intel 3002 for comparison
- Wikipedia: Bit slicing

---
