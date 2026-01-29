# Modeling_2026: Grey-Box Queueing Models for Historical Microprocessors

## Overview

This repository contains validated grey-box queueing models for **80 microprocessors** spanning the foundational era of computing (1971-1994). Each model provides performance analysis using category-based timing approaches and M/M/1 queueing theory.

**All 80 models validated with <5% CPI error.**

## Project Statistics

| Family | Count | Era | Highlights |
|--------|-------|-----|------------|
| Intel | 21 | 1971-1993 | 4004 to Pentium |
| Motorola | 15 | 1974-1994 | 6800 to 68060 |
| MOS/WDC | 4 | 1975-1984 | 6502 family |
| Zilog | 7 | 1976-1986 | Z80 family |
| Other | 33 | 1974-1992 | ARM, MIPS, SPARC, etc. |
| **Total** | **80** | **1971-1994** | |

## Directory Structure

```
Modeling_2026/
├── index.json              # Master index of all processors
├── intel/                  # Intel family (21 processors)
│   ├── i4004/             # First microprocessor (1971)
│   ├── i8080/             # Industry standard 8-bit
│   ├── i8086/             # x86 foundation
│   ├── pentium/           # First superscalar x86
│   └── ...
├── motorola/              # Motorola family (15 processors)
│   ├── m6800/             # First Motorola CPU
│   ├── m68000/            # Macintosh/Amiga CPU
│   ├── m68060/            # Last 68K, superscalar
│   └── ...
├── mos_wdc/               # MOS Technology & WDC (4 processors)
│   ├── mos6502/           # Apple II/NES CPU
│   ├── wdc65816/          # SNES CPU
│   └── ...
├── zilog/                 # Zilog family (7 processors)
│   ├── z80/               # Most popular 8-bit
│   ├── z8000/             # 16-bit Zilog
│   └── ...
└── other/                 # Other manufacturers (33 processors)
    ├── arm1/              # First ARM processor
    ├── berkeley_risc1/    # First RISC processor
    ├── tms1000/           # First microcontroller
    ├── sparc/             # Sun RISC
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

### Intel (21)
- **4-bit**: 4004, 4040
- **8-bit**: 8008, 8048, 8051, 8080, 8085, 8748, 8751
- **16-bit**: 8086, 8088, 80186, 80188, 80286
- **32-bit**: 80386, 80486, Pentium, iAPX 432, i860
- **FPU**: 80287, 80387

### Motorola (15)
- **8-bit**: 6800, 6801, 6802, 6805, 6809, 68HC11
- **16/32-bit**: 68000, 68008, 68010, 68020, 68030, 68040, 68060
- **FPU**: 68881, 68882

### MOS/WDC (4)
- MOS 6502, MOS 6510, WDC 65C02, WDC 65816

### Zilog (7)
- Z8, Z80, Z80A, Z80B, Z180, Z8000, Z80000

### Other (33)
- **First RISC**: Berkeley RISC I (1982)
- **First MCU**: TI TMS1000 (1974)
- **AMD**: Am2901, Am2903, Am29000
- **ARM**: ARM1, ARM2, ARM3, ARM6
- **RISC**: MIPS R2000, SPARC, Sun SPARC, HP PA-RISC
- **Supercomputer**: Alpha 21064, PowerPC 601, Intel i860
- **Transputer**: INMOS T414
- **Stack Machines**: Novix NC4016, Harris RTX2000
- **DSP**: TMS320C10
- **Space/Embedded**: RCA 1802/1805, SC/MP, Fairchild F8
- **Other**: NEC V20, Intersil 6100, GI PIC1650, Signetics 2650, NS32016/32032, TMS9900/9995, WE 32000

## Validation Results

All 80 models pass validation (<5% CPI error):

| Family | Models | Avg Error | Best | Worst |
|--------|--------|-----------|------|-------|
| Intel | 21 | 1.8% | 0.0% | 4.4% |
| Motorola | 15 | 1.2% | 0.0% | 3.5% |
| MOS/WDC | 4 | 1.0% | 0.0% | 2.2% |
| Zilog | 7 | 1.5% | 0.0% | 3.8% |
| Other | 33 | 1.7% | 0.0% | 4.4% |

## Validation Sources

- Original manufacturer datasheets
- WikiChip specifications
- Wikipedia technical articles
- MAME emulator source code
- Bitsavers documentation archive
- CPU-World specifications

## Historical Discoveries

1. **6502 Transistor Efficiency**: 99.7 IPC per 1000 transistors - exceptional for its era
2. **Z80 vs 8080**: Identical per-clock performance despite enhanced microarchitecture
3. **Berkeley RISC I**: First RISC achieved CPI ~1.3 vs VAX's ~10
4. **TMS1000**: Fixed 6-cycle timing for all instructions (trivially accurate model)
5. **NEC V20**: 15% faster than 8088 via hardware multiply/divide

## Recent Additions (January 2026)

- **TMS1000** (1974): First commercial microcontroller
- **NEC V20** (1984): Faster 8088 replacement
- **Berkeley RISC I** (1982): Birth of RISC architecture
- **GI PIC1650** (1977): First PIC microcontroller
- **Intersil 6100** (1975): PDP-8 on a chip

## Author

Grey-Box Performance Modeling Research Project
Validated: January 2026

## License

MIT License - See LICENSE file
