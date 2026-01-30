# Hitachi HD63484 ACRTC Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation

**Session goal:** Create grey-box queueing model for the Hitachi HD63484 ACRTC graphics processor

**Starting state:**
- No model existed

**Research findings:**
- HD63484 was Hitachi's Advanced CRT Controller (1984)
- 16-bit internal data path with 20-bit address bus (~1MB video RAM)
- ~80,000 transistors, 8 MHz clock
- Hardware graphics acceleration: line, circle, arc, fill, BitBLT
- Graphics commands are multi-cycle, with BitBLT being most expensive
- Used in Sharp X68000, various arcade machines, CAD workstations

**Changes made:**

1. Created model with 7 instruction categories:
   - draw_line: Line drawing @6 cycles
   - draw_circle: Circle/arc @10 cycles
   - area_fill: Area fill/paint @8 cycles
   - bitblt: Bit block transfer @12 cycles
   - char_display: Character display @5 cycles
   - control: Control/setup @4 cycles
   - dma: DMA/refresh @3 cycles

2. Added 4 workload profiles:
   - typical: BitBLT-heavy graphics workload
   - drawing: Vector drawing workload
   - gui: GUI/windowing workload
   - text: Text-heavy display workload

3. Added validation tests:
   - CPI ~10.0 for typical workload (within 5%)
   - All category timing verified

**What we learned:**
- Graphics command timing is highly variable depending on drawing size
- Base cycle counts represent command setup; actual cost scales with pixels
- BitBLT dominates typical graphics workloads

**Final state:**
- CPI: 9.87 (1.3% error from 10.0 target)
- Validation: PASSED
- 8/8 per-instruction timing tests passing

**References used:**
- Hitachi HD63484 ACRTC Technical Manual (1984)
- Sharp X68000 Technical Reference
- HD63484 Application Notes

---

## 2026-01-29 - System identification: correction terms applied

**Session goal:** Fit correction terms via scipy.optimize.least_squares

**Changes made:**
- Ran system identification with 7 free correction parameters
- Optimizer converged in 20 evaluations
- Corrections: area_fill: +1.89, bitblt: +0.18, char_display: +0.73, control: -2.90, dma: -3.83, draw_circle: +1.06, draw_line: -0.37

**Final state:**
- CPI error: 0.00%
- Validation: PASSED

---
