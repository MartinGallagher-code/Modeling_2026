# Changelog

All notable changes to the Modeling_2026 project are documented here.

---

## [2.0.0] - January 24, 2026

### Major Release: Comprehensive Historical Coverage

#### Added - New Processor Models (47 new models)

**Intel Family:**
- Intel 4004 (1971) - First microprocessor
- Intel 8008 (1972) - First 8-bit
- Intel 8085/8085A (1976) - System-friendly 8080
- Intel 8048 (1976) - First successful MCU
- Intel 8051 (1980) - Billions shipped
- Intel 80186/80188 (1982) - Integrated 8086
- Intel 80286 (1982) - Protected mode
- Intel 80386 (1985) - Full 32-bit
- Intel 80486 (1989) - Pipelined, cached
- Intel Pentium (1993) - First superscalar x86
- Intel i860 (1989) - "Cray on a chip"

**Motorola Family:**
- Motorola 6800 (1974) - Clean 8-bit
- Motorola 6805 (1979) - MCU, billions shipped
- Motorola 6809 (1978) - Best 8-bit ever
- Motorola 68010 (1982) - Virtual memory
- Motorola 68020 (1984) - On-chip cache
- Motorola 68030 (1987) - On-chip MMU
- Motorola 68040 (1990) - On-chip FPU
- Motorola 68060 (1994) - Last 68k, superscalar

**MOS/WDC Family:**
- WDC 65C02 (1983) - CMOS 6502
- WDC 65816 (1984) - 16-bit, SNES

**Zilog Family:**
- Zilog Z180 (1985) - Z80 + MMU
- Zilog Z8 (1979) - MCU
- Zilog Z8000 (1979) - Failed 16-bit

**ARM Family:**
- ARM1 (1985) - Birth of ARM
- ARM2 (1986) - First production ARM
- ARM3 (1989) - First cached ARM
- ARM6 (1991) - Foundation of modern ARM

**Other Architectures:**
- RCA 1802 (1974) - Space processor
- RCA CDP1805 (1984) - Enhanced space processor
- Fairchild F8 (1974) - Multi-chip
- Signetics 2650 (1975) - Unique architecture
- Intersil 6100 (1974) - PDP-8 on chip
- TI TMS9900 (1976) - Registers in RAM
- NS 32016 (1982) - First 32-bit
- NS 32032 (1984) - Improved 32-bit
- MIPS R2000 (1985) - Textbook RISC
- Sun SPARC (1987) - Register windows
- AMD Am29000 (1987) - Laser printer CPU
- Transputer (1987) - Parallel pioneer
- HP PA-RISC (1986) - HP workstations
- DEC Alpha 21064 (1992) - Fastest of era
- PowerPC 601 (1993) - AIM alliance

#### Added - Documentation
- `README.md` - Comprehensive project overview
- `PROJECT_STATUS.md` - Status and roadmap
- `METHODOLOGY.md` - Technical methodology guide
- `CONTRIBUTING.md` - Contribution guidelines
- `CHANGELOG.md` - This file
- `PROCESSOR_EVOLUTION_1971-1985.md` - Historical analysis

#### Changed
- Reorganized repository structure
- Split processors into "through 1985" and "after 1985" directories
- Updated all model documentation for consistency

---

## [1.5.0] - January 23, 2026

### Expanded Coverage

#### Added
- 27 additional processor models
- Cross-family comparisons
- Improved calibration framework

---

## [1.0.0] - January 22, 2026

### Initial Release

#### Added
- Core queueing model framework
- M/M/1 queue implementation
- Initial processor models:
  - Intel 8080
  - Intel 8086
  - Intel 8088
  - MOS 6502
  - Zilog Z80
  - Motorola 68000
  - Intel 80286
  - Intel 80386
- Basic documentation
- Calibration methodology

---

## Version Numbering

This project uses semantic versioning:
- **Major** (X.0.0): Significant new features or breaking changes
- **Minor** (0.X.0): New processor models or features
- **Patch** (0.0.X): Bug fixes and documentation updates

---

## Roadmap

### [3.0.0] - Planned Q2 2026
- Modern x86 (Pentium Pro through Athlon 64)
- Out-of-order execution modeling

### [4.0.0] - Planned Q3 2026
- Modern ARM (ARM7 through Cortex)
- Apple A-series preliminary models

### [5.0.0] - Planned Q4 2026
- Specialized processors (consoles, DSP)
- Multi-core modeling framework
