# Intel 2920 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial model creation and validation

**Session goal:** Create validated performance model for Intel 2920 analog signal processor

**Starting state:**
- No existing model

**Changes made:**

1. Created Intel 2920 validated model
   - 5 instruction categories: arithmetic, data_transfer, adc_dac, control, shift
   - 4 workload profiles: typical, compute, memory, control
   - Clock: 5 MHz, instruction time minimum 400ns
   - CPI calibrated to 5.0 for typical DSP workloads
   - Accounts for lack of hardware multiplier

2. Created validation JSON with 10 timing tests
   - ADD/SUB: 2 cycles (400ns)
   - LDA/STA: 2 cycles (400ns)
   - ABA/ENA (ADC/DAC): 4 cycles (800ns)
   - JMP/JNZ: 3 cycles (600ns)
   - SHL/SHR: 2 cycles (400ns)

**What we learned:**
- The Intel 2920 (1979) was Intel's first DSP attempt
- 25-bit data path for analog signal processing
- On-chip ADC/DAC but no hardware multiplier
- The lack of hardware multiply makes MAC operations very expensive
- Commercial failure, but historically significant as first single-chip DSP attempt

**Final state:**
- CPI: 5.0 for typical workload
- Validation: PASSED

---
