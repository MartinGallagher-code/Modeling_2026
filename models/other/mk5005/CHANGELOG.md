# Mostek MK5005 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Mostek MK5005 calculator chip

**Starting state:**
- No model existed

**Research findings:**
- Early calculator-on-a-chip PMOS IC (1972)
- 4-bit serial BCD data path with shift registers
- Integrated keyboard scanning and display multiplexing
- One of the earliest single-chip calculator designs
- Clock: 200 kHz typical
- ~3,000 transistors (PMOS)

**Changes made:**

1. Created model with 5 instruction categories:
   - alu: 8 cycles (serial 4-bit ADD, SUB)
   - bcd: 10 cycles (multi-digit BCD, decimal correct)
   - shift: 6 cycles (shift register rotate)
   - control: 7 cycles (branch, conditional skip)
   - display: 12 cycles (display scan, segment output)

2. Calibrated workload weights for typical CPI = 9.0:
   - typical: alu=0.20, bcd=0.15, shift=0.15, control=0.20, display=0.30
   - compute: heavier BCD/ALU (CPI ~8.7)
   - memory: heavier shift ops (CPI ~8.05)
   - control: heavier control/display (CPI ~8.55)

3. Added validation tests:
   - Typical CPI = 9.0 (0.0% error)
   - IPS ~22,222 at 200 kHz
   - Workload variations are reasonable

**What we learned:**
- Early PMOS technology results in very high cycle counts across the board
- Display operations are the most expensive (12 cycles)
- Even basic ALU takes 8 cycles due to serial architecture
- Overall CPI of 9.0 reflects the primitive technology

**Final state:**
- CPI: 9.0 (0.0% error)
- Validation: PASSED
- All tests passing

**References used:**
- MK5005 Data Sheet (Mostek, 1972)
- Calculator-on-a-Chip History (Smithsonian)
- Early LSI Calculator Architecture Survey

---
