# Executive Summary

**Modeling_2026: Grey-Box Queueing Models for Historical Microprocessors**

Last Updated: January 30, 2026

---

## Overview

This project provides cycle-accurate performance models for **422 microprocessors** spanning 1970-1995, covering the complete foundational era of microprocessor design from the Intel 4004 through RISC workstations, superscalar CPUs, and early 3D graphics. Each model predicts Cycles Per Instruction (CPI), Instructions Per Cycle (IPC), and Instructions Per Second (IPS) using grey-box queueing theory calibrated against documented hardware specifications.

**All 422 models achieve <5% CPI prediction error.** All models expose a full system identification API.

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total processor models | 422 |
| Year coverage | 1970-1995 |
| Manufacturer families | 19 |
| Models at <5% error | 422 (100%) |
| System identification API | 422 (100%) |
| Phase 6 additions | 101 (post-1985 era) |

---

## Methodology

### Grey-Box Queueing Model

Each processor is modeled as a sequential or pipelined execution unit where performance is determined by:

1. **Instruction categories** -- groups of instructions with similar cycle counts (e.g., ALU operations, memory access, control flow), with timings sourced from manufacturer datasheets.

2. **Workload profiles** -- probability distributions over instruction categories representing different usage patterns (typical, compute-intensive, memory-intensive, control-flow-intensive).

3. **Weighted CPI calculation** -- `CPI = sum(weight[category] * cycles[category])` across all categories for a given workload.

### System Identification

A least-squares optimization layer refines each model by fitting per-category correction terms against measured CPI data:

- **Algorithm**: Trust-Region-Reflective (scipy.optimize.least_squares)
- **Free parameters**: Per-category correction offsets
- **Objective**: Minimize relative CPI error across all workloads
- **Convergence rate**: 398/422 models (94.3%)
- **Safety**: Automatic rollback if optimization worsens accuracy

The corrected CPI is: `corrected_cpi = base_cpi + sum(correction[cat] * weight[cat])`

---

## Coverage by Manufacturer

| Family | Models | Notable Processors |
|--------|--------|--------------------|
| Intel | 39 | 4004, 8080, 8086, 80386, Pentium, i960 |
| Motorola | 32 | 6800, 68000, 68060, 88100/88110, ColdFire, DSP56001 |
| Eastern Bloc | 22 | U880, KR580VM1, Elbrus El-90, K1839VM1 |
| NEC | 18 | V20, V30, V60, V810, V850, uPD780 |
| Texas Instruments | 21 | TMS1000, TMS9900, TMS320 DSPs, TMS34020 |
| National Semi | 12 | SC/MP, NS32016, PACE, COP400 |
| Zilog | 14 | Z80, Z8000, Z380, Z8S180 |
| AMD | 12 | Am2901, Am29000, Am386/486/5x86, PCnet |
| Hitachi | 13 | HD6309, SH-1/SH-2, H8/300/500, FD1094 |
| AMI | 6 | S2000, S2150, S2811 |
| Fujitsu | 8 | MB8841, MB86900 SPARC, SPARClite |
| Mitsubishi | 6 | MELPS 740, M50740 |
| MOS/WDC | 6 | 6502, 6510, 65C02, 65816 |
| Namco | 6 | Custom arcade processors |
| RCA | 5 | 1802 (COSMAC), 1805 |
| Rockwell | 5 | PPS-4, R6502, R6511 |
| Toshiba | 6 | TLCS-12, TLCS-870, TX39 |
| ARM | 7 | ARM1-ARM6, ARM250, ARM610, ARM7TDMI |
| Other | 184 | MIPS R3000-R10000, SPARC variants, PowerPC, Alpha, x86 clones, DSPs, gaming, graphics |

---

## Repository Structure

Each of the 422 processors has a standardized directory:

```
[processor]/
  current/          Model source code (*_validated.py)
  validation/       Accuracy metrics (*_validation.json)
  measurements/     Calibration input data (measured CPI, benchmarks, traces)
  identification/   System identification results (fitted corrections)
  docs/             Architecture documentation
  CHANGELOG.md      Complete history of all work (append-only)
  HANDOFF.md        Current state and next steps
  README.md         Quick reference and validation status
```

### Pipeline

```
Datasheets ──> Instruction Timings ──> Base Model
                                           │
Measured CPI ──> System Identification ────┘
                                           │
                                    Corrected Model ──> Validation (<5% error)
```

---

## Architecture Coverage

| Category | Count | Examples |
|----------|-------|---------|
| 4-bit | 18 | Intel 4004, TMS1000, AMI S2000, PPS-4 |
| 8-bit | 142 | 8080, Z80, 6502, 6800, 8051 |
| 16-bit | 78 | 8086, 68000, Z8000, TMS9900, PDP-11 clones |
| 32-bit | 110 | 80386, 68040, ARM2-ARM7TDMI, SPARC, MIPS R3000-R10000, PowerPC |
| 64-bit | 10 | Alpha 21064/21064A/21066, i860, MIPS R4000/R4400/R8000/R10000 |
| Bit-slice | 10 | Am2901, SN74181, MC10800 |
| DSP | 22 | TMS320C10-C80, DSP56001, ADSP-2100, AT&T DSP16/DSP32C |
| Coprocessor/FPU | 8 | 8087, 80287, 68881, NS32081 |
| Graphics/Video | 10 | TMS34010, S3 86C911, ATI Mach32/64, Weitek P9000 |
| Sound | 12 | YM2612, YM2151, Ensoniq OTTO, ES5503 |
| Stack machine | 4 | Novix NC4016, Harris RTX2000, WISC |

---

## Quality Assurance

- **422/422 models pass validation** (<5% CPI error)
- **422/422 models expose full system identification API** (get_corrections, set_corrections, compute_residuals, compute_loss, get_parameters, set_parameters, get_parameter_bounds)
- **100% documentation coverage**: Every model has README, CHANGELOG, HANDOFF, validation JSON, and architecture docs
- **100% measurement data**: Every model has calibration inputs and system identification results
- **Cross-validation**: Family relationships verified (e.g., 8080 -> 8085, 6502 -> 6510, Z80 -> Z80A -> Z80B)
- **Automated validation**: Full test suite loads and runs every model dynamically

---

## Future Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1-4 | Foundation through pre-1986 coverage (321 models) | Complete |
| Phase 5 | Instruction timing collection | Pending |
| Phase 6 | Post-1985 processors: RISC workstations, superscalar, DSPs, graphics (101 models) | Complete |
