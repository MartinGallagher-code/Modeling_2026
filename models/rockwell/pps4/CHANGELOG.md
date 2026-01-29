# Rockwell PPS-4 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the third commercial microprocessor

**Starting state:**
- No model existed

**Research findings:**
- PPS-4 was the third commercial microprocessor (1972), after Intel 4004 (1971) and 4040 (1971)
- 4-bit data path with SERIAL ALU (processes 1 bit at a time)
- Serial bit processing makes it significantly slower than parallel designs
- Typical clock: 200 kHz
- Used in calculators, pinball machines (e.g., Bally), point-of-sale terminals
- Approximately 5000 transistors (estimated)
- 12-bit address space (4KB ROM)

**Changes made:**

1. Created model with serial ALU timing characteristics
   - Target CPI: 12.0 (slower than TMS1000's 6.0 due to serial processing)
   - Clock: 200 kHz (slower than most contemporaries)
   - Four instruction categories reflecting serial architecture

2. Added 4 instruction categories:
   - alu: Serial arithmetic @14 cycles (bit-by-bit processing)
   - memory: Load/store @10 cycles
   - branch: Control flow @12 cycles
   - io: I/O operations @10 cycles

3. Added 5 workload profiles:
   - typical: General embedded use
   - compute: Calculator-style arithmetic
   - memory: Data manipulation
   - control: Pinball machine logic
   - mixed: POS terminal operations

4. Added validation tests:
   - CPI ~12.0 for typical workload
   - IPS ~16,667 at 200 kHz
   - All workloads in reasonable CPI range
   - Serial ALU identified as bottleneck for compute workloads

**What we learned:**
- Serial ALU architecture significantly impacts performance
- Bit-serial processing trades speed for die area (fewer transistors)
- Despite slow speed, was successful in cost-sensitive applications
- Pinball machines particularly suited to low-speed requirements

**Final state:**
- CPI: ~12.0 (target achieved)
- Validation: PASSED
- Architecture correctly models serial processing overhead

**References used:**
- Rockwell PPS-4 documentation
- Wikipedia: Rockwell PPS-4
- "History of Microprocessors" technical archives
- Pinball machine technical manuals (Bally)

---
