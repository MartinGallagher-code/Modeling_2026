# NEC uPD7220 Graphics Display Controller Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated model for NEC uPD7220 - first LSI graphics display controller

**Starting state:**
- No existing model

**Changes made:**

1. Created initial model with graphics command timing calibrated for CPI = 12.0
   - draw_line: 16 cycles (LINE command per pixel step)
   - draw_arc: 24 cycles (ARC command per step)
   - area_fill: 14 cycles (FIGS area fill)
   - char_display: 8 cycles (CHAR display)
   - dma_transfer: 4 cycles (DMAW/DMAR per word)
   - control: 3 cycles (RESET, CURS, status)

**What we learned:**
- NEC uPD7220 (1981) was the first single-chip LSI graphics display controller
- NOT a general-purpose CPU - specialized for graphics rendering
- ~60000 transistors with 16-bit internal data path
- Hardware implementations of drawing algorithms (Bresenham line, etc.)
- Used in NEC PC-9801 and IBM Professional Graphics Controller
- CPI metric represents cycles per graphics command step

**Final state:**
- CPI: 12.0 (target)
- Validation: PASSED

**References used:**
- NEC uPD7220/7220A GDC Technical Manual
- NEC PC-9801 Technical Reference
- IBM Professional Graphics Controller documentation

---
