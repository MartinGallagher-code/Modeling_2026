# Modeling_2026: Grey-Box Queueing Models for Historical Microprocessors

## Overview

This repository contains validated grey-box queueing models for **117 microprocessors** spanning the foundational era of computing (1971-1994). Each model provides performance analysis using category-based timing approaches and M/M/1 queueing theory.

**All 117 models validated with <10% CPI error (116 with <5% error).**

## Project Statistics

| Family | Count | Era | Highlights |
|--------|-------|-----|------------|
| Intel | 24 | 1971-1993 | 4004 to Pentium, 8096 MCU |
| Motorola | 16 | 1974-1994 | 6800 to 68060, 68HC05 |
| MOS/WDC | 4 | 1975-1984 | 6502 family |
| Zilog | 7 | 1976-1986 | Z80 family |
| Other | 66 | 1972-1992 | ARM, MIPS, SPARC, DSPs, etc. |
| **Total** | **117** | **1971-1994** | |

## Directory Structure

```
Modeling_2026/
├── index.json              # Master index of all processors
├── intel/                  # Intel family (24 processors)
│   ├── i4004/             # First microprocessor (1971)
│   ├── i8080/             # Industry standard 8-bit
│   ├── i8086/             # x86 foundation
│   ├── i8096/             # 16-bit automotive MCU
│   ├── pentium/           # First superscalar x86
│   └── ...
├── motorola/              # Motorola family (16 processors)
│   ├── m6800/             # First Motorola CPU
│   ├── m68000/            # Macintosh/Amiga CPU
│   ├── m68hc05/           # Low-cost MCU
│   ├── m68060/            # Last 68K, superscalar
│   └── ...
├── mos_wdc/               # MOS Technology & WDC (4 processors)
│   ├── mos6502/           # Apple II/C64 CPU
│   ├── wdc65816/          # SNES CPU
│   └── ...
├── zilog/                 # Zilog family (7 processors)
│   ├── z80/               # Most popular 8-bit
│   ├── z8000/             # 16-bit Zilog
│   └── ...
└── other/                 # Other manufacturers (66 processors)
    ├── ricoh_2a03/        # NES CPU
    ├── mos6507/           # Atari 2600 CPU
    ├── arm1/              # First ARM processor
    ├── berkeley_risc1/    # First RISC processor
    ├── stanford_mips/     # Original MIPS
    ├── hitachi_6309/      # "Best 8-bit ever"
    ├── pps4/              # Third microprocessor (1972)
    └── ...
```

## Each Processor Package Contains

```
[processor]/
├── README.md                          # Quick reference
├── current/
│   └── [processor]_validated.py       # ✓ USE THIS - validated model
├── validation/
│   └── [processor]_validation.json    # Validation data & timing tests
├── CHANGELOG.md                       # Full history of model work
├── HANDOFF.md                         # Current state & next steps
└── docs/                              # Additional documentation
```

## Documentation

Historical context and methodology documentation is available in `docs/historical/`:

| Document | Description |
|----------|-------------|
| `METHODOLOGY.md` | Grey-box queueing model methodology and calibration process |
| `FAMILY_TREES.md` | Processor lineages and architectural relationships |
| `EVOLUTION_TIMELINE.md` | Visual timeline of microprocessor evolution 1971-1985 |
| `PERFORMANCE_COMPARISON.md` | Side-by-side performance metrics across all processors |
| `ARCHITECTURAL_GUIDE.md` | Guide to processor architectural concepts |

## Methodology

### Grey-Box Queueing Approach

1. **Category-Based Timing**: 5-15 instruction categories instead of 200+ individual instructions
2. **M/M/1 Queueing Networks**: Models pipeline stages and bottlenecks
3. **Workload Profiles**: Multiple profiles (typical, compute, memory, control)
4. **Cross-Validation**: Per-instruction timing tests against datasheets

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

# Run validation
validation = model.validate()
print(f"Tests passed: {validation['passed']}/{validation['total']}")
```

## Processor Coverage

### Intel (24)
- **4-bit**: 4004, 4040
- **8-bit**: 8008, 8048, 8051, 8080, 8085, 8748, 8751
- **8-bit MCU**: 8035/8039
- **16-bit**: 8086, 8088, 80186, 80188, 80286
- **16-bit MCU**: 8096
- **32-bit**: 80386, 80486, Pentium, iAPX 432, i860
- **FPU**: 80287, 80387
- **Bit-slice**: 3002

### Motorola (16)
- **8-bit**: 6800, 6801, 6802, 6805, 6809, 68HC05, 68HC11
- **16/32-bit**: 68000, 68008, 68010, 68020, 68030, 68040, 68060
- **FPU**: 68881, 68882

### MOS/WDC (4)
- MOS 6502, MOS 6510, WDC 65C02, WDC 65816

### Zilog (7)
- Z8, Z80, Z80A, Z80B, Z180, Z8000, Z80000

### Other (66)
- **6502 Family**: Ricoh 2A03 (NES), MOS 6507 (Atari 2600), MOS 6509, R65C02, SY6502A, R6511
- **6800 Clones**: Hitachi 6309, HD6301, Fujitsu MB8861
- **Z80 Clones**: NEC μPD780, Hitachi HD64180
- **4-bit**: PPS-4, PPS-4/1, μCOM-4, μPD751, TMS1000
- **Academic RISC**: Berkeley RISC I/II, Stanford MIPS
- **Commercial RISC**: MIPS R2000, SPARC, Sun SPARC, HP PA-RISC
- **ARM**: ARM1, ARM2, ARM3, ARM6
- **Supercomputers**: Alpha 21064, PowerPC 601, Intel i860
- **Transputer**: INMOS T414
- **Stack Machines**: Novix NC4016, Harris RTX2000
- **DSP**: TMS320C10, NEC μPD7720, AMI S2811, Signetics 8X300
- **Bit-slice**: Am2901, Am2903, TI SN74S481, MM6701
- **Math Coprocessors**: Am9511, Am9512, NS32081
- **16-bit Pioneers**: IMP-16, PACE, mN601, WD16, F100-L, CP1600, MN1610
- **COSMAC**: RCA 1802, 1804, 1805, 1806
- **Other**: NEC V20, V30, Intersil 6100, Harris HM6100, GI PIC1650, Signetics 2650, NS32016/32032, TMS9900/9995, WE32000, SC/MP, F8, Mostek 3870, Sharp LH5801

## Validation Results

All 117 models pass validation:

| Family | Models | Fully Validated (<5%) | Passed (<10%) |
|--------|--------|----------------------|---------------|
| Intel | 24 | 24 | 0 |
| Motorola | 16 | 16 | 0 |
| MOS/WDC | 4 | 4 | 0 |
| Zilog | 7 | 7 | 0 |
| Other | 66 | 65 | 1 |
| **Total** | **117** | **116** | **1** |

## Validation Sources

- Original manufacturer datasheets
- WikiChip specifications
- Wikipedia technical articles
- MAME emulator source code
- Bitsavers documentation archive
- CPU-World specifications
- NESDev Wiki (for Ricoh 2A03)

## Historical Discoveries

1. **6502 Transistor Efficiency**: 99.7 IPC per 1000 transistors - exceptional for its era
2. **Z80 vs 8080**: Identical per-clock performance despite enhanced microarchitecture
3. **Berkeley RISC I**: First RISC achieved CPI ~1.3 vs VAX's ~10
4. **TMS1000**: Fixed 6-cycle timing for all instructions (trivially accurate model)
5. **NEC V20**: 15% faster than 8088 via hardware multiply/divide
6. **TMS9900**: Memory-to-memory architecture resulted in CPI ~20 (very slow)
7. **Hitachi 6309**: ~15% faster than 6809 with native mode instructions
8. **Stanford MIPS**: Original academic RISC that led to commercial MIPS R2000

## Recent Additions (January 2026)

### Tier 1 - High Priority (5)
- **Ricoh 2A03** (1983): NES/Famicom CPU - 6502 without BCD
- **MOS 6507** (1975): Atari 2600 CPU - 6502 in 28-pin package
- **Rockwell PPS-4** (1972): Third commercial microprocessor
- **NEC V30** (1984): 16-bit companion to V20
- **Hitachi 6309** (1982): Enhanced 6809 - "best 8-bit ever"

### Tier 2 - Historically Interesting (5)
- **GI CP1600** (1975): Intellivision game console CPU
- **Berkeley RISC II** (1983): Improved RISC I, influenced SPARC
- **Intel 8096** (1982): 16-bit MCU, dominated automotive
- **AMD Am9511** (1977): Early Arithmetic Processing Unit
- **NEC μPD7720** (1980): Early DSP for speech synthesis

### Additional Models (27)
- 6502 variants, Japanese clones, 4-bit processors, embedded MCUs
- Bit-slice ALUs, math coprocessors, DSPs, 16-bit pioneers
- COSMAC variants, and more

## Author

Grey-Box Performance Modeling Research Project
Validated: January 29, 2026

## License

MIT License - See LICENSE file
