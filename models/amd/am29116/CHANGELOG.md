# AMD Am29116 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial validation and documentation

**Session goal:** Validate the Am29116 grey-box queueing model and create documentation.

**Starting state:**
- CPI: 1.536 (2.4% error vs target 1.5)
- Key issues: None - model was already within validation threshold

**Changes attempted:**

1. Ran model across all four workloads
   - typical: CPI=1.536, IPC=0.651, IPS=6,510,942, bottleneck=alu
   - compute: CPI=1.455, IPC=0.687, IPS=6,873,112, bottleneck=alu
   - memory: CPI=2.018, IPC=0.496, IPS=4,956,563, bottleneck=register_file
   - control: CPI=1.464, IPC=0.683, IPS=6,832,028, bottleneck=alu
   - Result: All workloads produce reasonable CPI values; typical workload is 2.4% from target

**What we learned:**
- The Am29116 integrates a 16-bit ALU, 16-entry register file, and microinstruction decoder
- Most ALU/register/shift operations are 1 cycle; memory reads are 3 cycles (1 base + 2 memory), memory writes are 2 cycles, multiply steps are 3 cycles
- Bus contention adds modest overhead via M/M/1 queueing model
- Memory-intensive workloads push CPI to ~2.0 due to external bus latency
- ALU is the bottleneck for most workloads; register_file becomes bottleneck under memory-heavy loads

**Final state:**
- CPI: 1.536 (2.4% error)
- Validation: PASSED

**References used:**
- Am29116 datasheet (1983, AMD 16-bit microprogrammable CPU)

---
