# Modeling_2026: Grey-Box Queueing Models for Historical Microprocessors

## Overview

This repository contains validated grey-box queueing models for **422 microprocessors** spanning the foundational era of computing (1970-1995). Each model provides performance analysis using category-based timing approaches and M/M/1 queueing theory.

**All 422 models validated with <5% CPI error.**

## Project Statistics

| Family | Count | Era | Highlights |
|--------|-------|-----|------------|
| Intel | 39 | 1971-1994 | 4004 to Pentium, i960, i82596 |
| Motorola | 32 | 1974-1994 | 6800 to 68060, 88100/88110, ColdFire, DSP56001 |
| MOS/WDC | 6 | 1975-1985 | 6502 family |
| Zilog | 14 | 1976-1994 | Z80 family, Z380, Z8S180 |
| NEC | 18 | 1972-1994 | V20/V30/V60/V70, V810/V850, uPD series |
| TI | 21 | 1970-1994 | TMS series, SN74181, TMS320 DSPs, TMS34020 |
| AMD | 12 | 1975-1995 | Am2901, Am29000, Am386/486/5x86, PCnet |
| Hitachi | 13 | 1977-1994 | 6309, SH-1/SH-2, H8/300/500, HD series |
| Fujitsu | 8 | 1977-1993 | MB884x arcade, MB86900 SPARC, SPARClite |
| AMI | 6 | 1970-1979 | S2000 calculator, S2811 DSP |
| Mitsubishi | 6 | 1978-1984 | MELPS 4-bit & 740 8-bit |
| Toshiba | 6 | 1973-1994 | TLCS-12 (first Japanese uP), TX39 |
| ARM | 7 | 1985-1994 | ARM1 to ARM6, ARM250, ARM610, ARM7TDMI |
| Namco | 6 | 1980s | Pac-Man era arcade custom |
| Eastern Bloc | 22 | 1978-1991 | DDR, Soviet, Czech, Bulgarian, Elbrus |
| RCA | 5 | 1976-1985 | COSMAC space processors |
| National | 12 | 1973-1984 | IMP-16, PACE, NS32000, COP400 |
| Rockwell | 5 | 1972-1983 | PPS-4, 6502 variants |
| Other | 184 | 1975-1995 | RISC workstations, DSPs, gaming, graphics, x86 clones |
| **Total** | **422** | **1970-1995** | **19 families** |

## Directory Structure

```
Modeling_2026/
├── index.json              # Master index of all 422 processors
├── models/                 # All processor model families
│   ├── intel/              # Intel (39) - 4004 to Pentium, i960
│   ├── motorola/           # Motorola (32) - 6800 to 68060, 88k, ColdFire
│   ├── mos_wdc/            # MOS/WDC (6) - 6502 family
│   ├── zilog/              # Zilog (14) - Z80 family, Z380
│   ├── nec/                # NEC (18) - V20-V850, μPD series
│   ├── ti/                 # Texas Instruments (21) - TMS CPUs, DSPs, GPUs
│   ├── amd/                # AMD (12) - Am2901, Am29000, Am386/486
│   ├── hitachi/            # Hitachi (13) - 6309, SH-1/SH-2, H8
│   ├── fujitsu/            # Fujitsu (8) - MB884x, SPARC, SPARClite
│   ├── ami/                # AMI (6) - S2000 calculator chips
│   ├── mitsubishi/         # Mitsubishi (6) - MELPS families
│   ├── toshiba/            # Toshiba (6) - TLCS series, TX39
│   ├── arm/                # ARM (7) - ARM1 to ARM7TDMI
│   ├── namco/              # Namco (6) - Pac-Man era arcade
│   ├── eastern_bloc/       # Eastern Bloc (22) - DDR, Soviet, Elbrus
│   ├── rca/                # RCA (5) - COSMAC space processors
│   ├── national/           # National Semi (12) - IMP-16, NS32000, COP400
│   ├── rockwell/           # Rockwell (5) - PPS-4, 6502 variants
│   └── other/              # Other manufacturers (184)
├── common/                 # Shared base classes and utilities
└── docs/                   # Methodology, family trees, comparisons
```

## Each Processor Package Contains

```
[processor]/
├── README.md                          # Quick reference
├── current/
│   └── [processor]_validated.py       # Validated model
├── validation/
│   └── [processor]_validation.json    # Validation data & timing tests
├── measurements/                       # Calibration input data
│   ├── measured_cpi.json              #   Per-workload CPI measurements
│   ├── benchmarks.json                #   Benchmark scores
│   └── instruction_traces.json        #   Instruction mix data
├── identification/                     # System identification results
│   └── sysid_result.json             #   Fitted correction terms
├── docs/                              # Architecture documentation
├── CHANGELOG.md                       # Full history of model work
└── HANDOFF.md                         # Current state & next steps
```

## Documentation

Historical context and methodology documentation is available in `docs/historical/`:

| Document | Description |
|----------|-------------|
| `METHODOLOGY.md` | Grey-box queueing model methodology and calibration process |
| `FAMILY_TREES.md` | Processor lineages and architectural relationships |
| `EVOLUTION_TIMELINE.md` | Visual timeline of microprocessor evolution 1971-1995 |
| `PERFORMANCE_COMPARISON.md` | Side-by-side performance metrics across all processors |
| `ARCHITECTURAL_GUIDE.md` | Guide to processor architectural concepts |

## Methodology

### Grey-Box Queueing Approach

1. **Category-Based Timing**: 5-15 instruction categories instead of 200+ individual instructions
2. **M/M/1 Queueing Networks**: Models pipeline stages and bottlenecks
3. **Workload Profiles**: Multiple profiles (typical, compute, memory, control)
4. **System Identification**: Least-squares correction term fitting
5. **Cross-Validation**: Per-instruction timing tests against datasheets

### System Identification API

Every model exposes a standard API for calibration:
- `get_corrections()` / `set_corrections()` - per-category correction terms
- `compute_residuals()` / `compute_loss()` - error metrics
- `get_parameters()` / `set_parameters()` / `get_parameter_bounds()` - full parameter access

### Key Insight

> Category-based timing with weighted averages for typical workloads is superior to exhaustive instruction enumeration.

## Usage

```python
# Example: Analyze Intel 8080
from i8080_validated import I8080Model

model = I8080Model()
result = model.analyze('typical')

print(f"IPS: {result.ips:,.0f}")
print(f"CPI: {result.cpi:.2f}")
print(f"Bottleneck: {result.bottleneck}")

# System identification
params = model.get_parameters()
corrections = model.get_corrections()
```

## Processor Coverage

### Intel (39)
- **4-bit**: 4004, 4040
- **8-bit**: 8008, 8048, 8051, 8080, 8085, 8748, 8751
- **8-bit MCU**: 8035/8039, 8061, 8044
- **16-bit**: 8086, 8088, 80186, 80188, 80286, 8096, 80C186
- **32-bit**: 80386, 80486, Pentium, iAPX 432, i860, i960, i960CA, i960CF
- **FPU**: 8087, 8087-2, 80287, 80387, 8231
- **Bit-slice**: 3002, 3003
- **Network**: 82586, 82730, 82557, 82596
- **Other**: Intel 2920, 8089

### Motorola (32)
- **8-bit**: 6800, 6801, 6802, 6803, 6804, 6805, 6805R2, 6809, 68HC05, 68HC11, 68HC11A1
- **16/32-bit**: 68000, 68008, 68010, 68020, 68030, 68040, 68060
- **Embedded**: CPU32, 68HC16, ColdFire, MC68302, MC68360
- **RISC**: 88100, 88110
- **FPU/MMU**: 68851, 68881, 68882
- **DSP**: DSP56001, DSP96002
- **Other**: MC14500B, 6854

### ARM (7)
- ARM1 (1985), ARM2 (1986), ARM3 (1989), ARM6 (1991)
- ARM250 (1990), ARM610 (1993), ARM7TDMI (1994)

### Other (184)
- **RISC Workstations**: MIPS R3000/R4000/R4400/R4600/R8000/R10000, IBM POWER1/POWER2, SPARC variants (Super/Micro/Hyper/Ultra), HP PA-7100/7200
- **PowerPC**: 601, 603, 604, 620
- **Alpha**: 21064, 21064A, 21066
- **x86 Clones**: Cyrix Cx486DLC/SLC/5x86, NexGen Nx586, IBM 486SLC2, UMC U5S, Hyundai 486
- **DSP**: TMS320C25/C30/C40/C50/C80, AT&T DSP16/DSP32C, ADSP-2100/2105/21020, Lucent DSP1600, Zoran ZR34161, SGS D950
- **Gaming**: Ricoh 5A22 (SNES), HuC6280 (TG-16), Sony R3000A (PS1), Sega VDP/SVP, SNK LSPC2, Yamaha FM chips (YM2612/2610, OPL3), Ensoniq OTTO
- **Graphics**: S3 86C911, Tseng ET4000, ATI Mach32/Mach64, Weitek P9000, C&T 65545
- **Academic RISC**: Berkeley RISC I/II, Stanford MIPS
- **Stack Machines**: Novix NC4016, Harris RTX2000, WISC CPU/16, WISC CPU/32
- **And many more**: Eastern Bloc, telecom, arcade, LISP machines, transputers, etc.

## Validation Results

All 422 models pass validation:

| Family | Models | Status |
|--------|--------|--------|
| Intel | 39 | All <5% |
| Motorola | 32 | All <5% |
| MOS/WDC | 6 | All <5% |
| Zilog | 14 | All <5% |
| NEC | 18 | All <5% |
| TI | 21 | All <5% |
| AMD | 12 | All <5% |
| Hitachi | 13 | All <5% |
| Fujitsu | 8 | All <5% |
| AMI | 6 | All <5% |
| Mitsubishi | 6 | All <5% |
| Toshiba | 6 | All <5% |
| ARM | 7 | All <5% |
| Namco | 6 | All <5% |
| Eastern Bloc | 22 | All <5% |
| RCA | 5 | All <5% |
| National | 12 | All <5% |
| Rockwell | 5 | All <5% |
| Other | 184 | All <5% |
| **Total** | **422** | **All <5% CPI error** |

## Historical Discoveries

1. **6502 Transistor Efficiency**: 99.7 IPC per 1000 transistors - exceptional for its era
2. **Z80 vs 8080**: Identical per-clock performance despite enhanced microarchitecture
3. **Berkeley RISC I**: First RISC achieved CPI ~1.3 vs VAX's ~10
4. **TMS1000**: Fixed 6-cycle timing for all instructions (trivially accurate model)
5. **NEC V20**: 15% faster than 8088 via hardware multiply/divide
6. **TMS9900**: Memory-to-memory architecture resulted in CPI ~20 (very slow)
7. **Hitachi 6309**: ~15% faster than 6809 with native mode instructions
8. **Stanford MIPS**: Original academic RISC that led to commercial MIPS R2000
9. **TMS34010**: First programmable GPU (1986) - pixel operations in hardware
10. **Eastern Bloc clones**: U880 (Z80), U808 (8008) were cycle-exact copies
11. **PowerPC 604**: 4-issue superscalar achieving CPI < 1.0
12. **NexGen Nx586**: RISC core with x86 translation, predecessor to AMD K6

## Phases

| Phase | Count | Description | Status |
|-------|-------|-------------|--------|
| Phase 1 | 42 | Pre-1986 high priority | Complete |
| Phase 2 | 77 | Pre-1986 extended coverage | Complete |
| Phase 3 | 55 | Pre-1986 deep cuts | Complete |
| Phase 4 | 73 | Pre-1986 coprocessors, clones, sound/video | Complete |
| Phase 5 | 48 | Instruction timing collection | Pending |
| Phase 6 | 101 | Post-1985 processors (1986-1994) | Complete |

## Author

Grey-Box Performance Modeling Research Project
Validated: January 30, 2026

## License

MIT License - See LICENSE file
