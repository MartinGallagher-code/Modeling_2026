# National NS32381 Model Changelog

This file contains the complete history of all work on this model.
**Append-only: Never delete previous entries.**

---

## 2026-01-29 - Initial validation and documentation

**Session goal:** Validate the NS32381 grey-box queueing model and create documentation.

**Starting state:**
- Model existed with no validation JSON or documentation files
- Model implements 7 FP instruction categories
- Target CPI: 8.0

**Changes attempted:**

1. Ran model across all four workloads to collect CPI/IPC results
   - typical: CPI=8.042, IPC=0.124, IPS=1,865,208, bottleneck=fp_pipeline
   - compute: CPI=10.376, IPC=0.096, IPS=1,445,644, bottleneck=fp_pipeline
   - memory: CPI=5.949, IPC=0.168, IPS=2,521,432, bottleneck=slave_bus
   - control: CPI=7.212, IPC=0.139, IPS=2,079,867, bottleneck=slave_bus

2. Created validation JSON, README.md, CHANGELOG.md, and HANDOFF.md

**What we learned:**
- The NS32381 is a floating-point coprocessor (not a general CPU), successor to NS32081
- 15 MHz clock, ~60K transistors, 32-bit data width, pipelined FP execution
- Model applies a 0.93 pipeline benefit factor to reduce base CPI
- Queueing factor adds overhead based on bottleneck utilization (rho * 0.06)
- FP operations range from 4 cycles (compare) to 35 cycles (sqrt), plus 1.5 memory cycles each
- Bottleneck shifts between fp_pipeline (compute-heavy) and slave_bus (memory/control-heavy)
- 3 utilization metrics tracked: fp_pipeline, slave_bus, divider

**Final state:**
- CPI: 8.042 (0.5% error vs 8.0 target)
- Validation: PASSED

**References used:**
- Model docstring referencing NS32000 FPU specifications
- NS32381 datasheet cycle counts (add=5, mul=7, div=25, sqrt=35)
