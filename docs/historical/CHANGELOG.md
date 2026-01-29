# Changelog

All notable changes to the Modeling_2026 project are documented here.

---

## [3.0.0] - January 29, 2026

### Major Release: Complete Pre-1986 Collection (117 Models)

#### Added - 37 New Processor Models

**Tier 1 - Gaming/Consumer Icons:**
- Ricoh 2A03 (1983) - NES/Famicom CPU (6502 without BCD)
- MOS 6507 (1975) - Atari 2600 CPU
- GI CP1600 (1975) - Intellivision game console CPU
- NEC V30 (1984) - 16-bit companion to V20
- Hitachi 6309 (1982) - Enhanced 6809, "best 8-bit ever"

**Tier 2 - Historical Firsts:**
- Rockwell PPS-4 (1972) - Third commercial microprocessor
- Berkeley RISC II (1983) - SPARC predecessor
- Stanford MIPS (1983) - Original academic MIPS
- Intel 8096 (1982) - 16-bit automotive MCU
- AMD Am9511 (1977) - First math coprocessor
- NEC μPD7720 (1980) - Early speech DSP

**6502 Family Variants:**
- MOS 6509 (1980) - CBM-II CPU with bank switching
- Rockwell R65C02 (1983) - CMOS 6502 with extensions
- Synertek SY6502A (1978) - Licensed 6502
- Rockwell R6511 (1980) - 6502 with peripherals

**Japanese Processors:**
- NEC μPD780 (1976) - Z80 clone
- Hitachi HD64180 (1985) - Z180 equivalent
- Hitachi HD6301 (1983) - Enhanced 6801 MCU
- Fujitsu MB8861 (1977) - 6800 clone
- Sharp LH5801 (1981) - Pocket computer CPU
- Panafacom MN1610 (1975) - Early Japanese 16-bit

**4-bit Processors:**
- Rockwell PPS-4/1 (1976) - Single-chip PPS-4
- NEC μCOM-4 (1972) - TMS1000 competitor
- NEC μPD751 (1974) - Early 4-bit MCU

**Bit-slice and Math Coprocessors:**
- Intel 3002 (1974) - Intel's bit-slice
- TI SN74S481 (1976) - TI bit-slice ALU
- Monolithic Memories 6701 (1975) - Bit-slice ALU
- AMD Am9512 (1979) - Floating-point APU
- National NS32081 (1982) - NS32000 FPU

**DSPs and Signal Processors:**
- AMI S2811 (1978) - Early signal processor
- Signetics 8X300 (1976) - Bipolar signal processor

**16-bit Pioneers:**
- National IMP-16 (1973) - Early 16-bit bit-slice based
- National PACE (1975) - p-channel MOS 16-bit
- Data General mN601 (1977) - microNova
- Western Digital WD16 (1977) - LSI-11 compatible
- Ferranti F100-L (1976) - British military 16-bit

**COSMAC and Other:**
- RCA CDP1804 (1980) - COSMAC with timer
- RCA CDP1806 (1985) - Final COSMAC
- Harris HM6100 (1978) - Faster CMOS PDP-8
- Motorola 68HC05 (1984) - Low-cost 6805
- Intel 8039 (1976) - MCS-48 ROM-less
- Mostek 3870 (1977) - F8 single-chip

#### Changed
- Updated all validation with cross-validated CPI targets
- Reorganized expected CPI database with research-based values
- TODO_PRE1986_CPUS.md now shows all 42 items complete

#### Validation
- **117 models total** (was 80)
- **100% pass rate** (117/117)
- **116 fully validated** (<5% error)
- **1 passed** (<10% error): NEC V30 at 5.5%

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
