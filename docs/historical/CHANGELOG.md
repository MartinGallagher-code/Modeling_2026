# Changelog

All notable changes to the Modeling_2026 project are documented here.

---

## [5.0.0] - January 30, 2026

### Major Release: Full Historical Coverage (422 Models)

#### Added - 101 New Post-1985 Processor Models (Phase 6)

**Major RISC Workstations (15):**
- MIPS R3000/R4000/R4400/R4600/R8000/R10000 (1988-1995) - SGI/DEC
- SuperSPARC/MicroSPARC/MicroSPARC II/HyperSPARC/UltraSPARC I (1992-1995) - Sun
- HP PA-7100/PA-7100LC/PA-7200 (1992-1994) - HP workstations
- IBM POWER1/POWER2 (1990-1993) - RS/6000

**PowerPC (3):**
- PowerPC 603/604/620 (1994-1995) - AIM alliance

**DEC Alpha (2):**
- Alpha 21064A/21066 (1993-1994)

**x86 Competitors (6):**
- Cyrix Cx486DLC/Cx486SLC/Cx5x86 (1992-1995)
- NexGen Nx586 (1994) - RISC core with x86 translation
- AMD Am386/Am486/Am5x86 (1991-1995)

**Embedded RISC & MCUs (15):**
- ARM250/ARM610/ARM7TDMI (1990-1994)
- NEC V810/V850 (1994)
- Hitachi SH-1/SH-2 (1992-1994) - Sega Saturn
- Motorola ColdFire (1994), CPU32, 68HC16
- Toshiba TX39 (1994) - MIPS-based embedded

**Advanced DSPs (15):**
- TI TMS320C25/C30/C40/C50/C80 (1986-1994)
- Analog Devices ADSP-2100/2105/21020 (1986-1991)
- AT&T DSP-16/DSP-32C (1987-1988)
- Lucent DSP1600, Motorola DSP56001/DSP96002
- Zoran ZR34161, SGS D950

**Gaming & Consumer (12):**
- Sony R3000A (1994) - PlayStation
- Ricoh 5A22 (1990) - SNES
- HuC6280 (1987) - TurboGrafx-16
- Sega SVP/VDP chips
- SNK LSPC2
- Yamaha FM sound chips (YM2151/2610/2612/3526/3812, YMF262)
- Ensoniq OTTO, ES5503

**Graphics/Video (8):**
- S3 86C911 (1991) - First single-chip Windows accelerator
- Tseng ET4000 (1989), ATI Mach32/Mach64 (1992-1994)
- Weitek P9000 (1992), C&T 65545
- IIT AGX

**Other (25):**
- Transputers (T212/T424/T800)
- LISP machines (Symbolics CADR, LMI Lambda, TI Explorer)
- Stack machines (WISC CPU/16, WISC CPU/32)
- Network processors (AMD PCnet, Intel 82596)
- Various clones, Eastern Bloc additions, and specialty processors

#### Added - System Identification API
- All 422 models now expose full sysid API: get_corrections(), set_corrections(), compute_residuals(), compute_loss(), get_parameters(), set_parameters(), get_parameter_bounds()
- BaseProcessorModel class with complete API available as both inherited and fallback implementation

#### Added - 125 Extended Pre-1986 Models (Phases 3-4)
- Phase 3 (55 models): Deep cuts including Japanese, Eastern Bloc, gaming, sound, DSP
- Phase 4 (73 models): Coprocessors, clones, sound/video, peripherals, more Eastern Bloc

#### Validation
- **422 models total** (was 196)
- **100% pass rate** (422/422 at <5%)
- **100% sysid API coverage** (422/422)

---

## [4.0.0] - January 29, 2026

### Major Release: Extended Pre-1986 Coverage (196 Models)

#### Added - 79 New Processor Models (Phase 2 Pre-1986)

**Tier 1 - Landmark Processors (10):**
- TI SN74181 (1970) - First single-chip ALU
- Motorola MC14500B (1976) - 1-bit industrial controller
- Intel 2920 (1979) - First Intel DSP with ADC/DAC
- Toshiba TLCS-12 (1973) - First Japanese microprocessor
- Fujitsu MB8841 (1977) - Arcade gaming icon (Galaga, Xevious)
- WD9000 Pascal MicroEngine (1979) - Direct p-code execution
- NEC μPD7220 (1981) - First LSI graphics processor
- Mitsubishi MELPS 740 (1984) - Enhanced 6502, 600+ variants
- East German U880 (1980) - Most-used Eastern Bloc CPU (Z80 clone)
- Fairchild 9440 MICROFLAME (1979) - Data General Nova on a chip

**4-Bit Processors (14):**
- Fujitsu MB8842-MB8845 (1977) - MB8841 arcade variants
- Mitsubishi MELPS 4/41/42 (1978-1980s) - 4-bit MCU family
- OKI MSM5840 (1980s) - 4-bit with LCD controller
- AMI S2000/S2150/S2200/S2400 (1970-1970s) - Early calculator chips
- NEC μPD612xA (1980s) - Extended μCOM-4 with LCD
- Samsung KS57 (1980s) - Korean 4-bit MCU entry

**8-Bit Processors (6):**
- Mitsubishi M50740/M50747 (1984) - MELPS 740 family
- HP Nanoprocessor (1977) - HP's proprietary calculator MCU
- Rockwell R6500/1 (1978) - Single-chip 6502
- GTE G65SC802/G65SC816 (1985) - WDC 65C816 second-source

**16-Bit Processors (4):**
- Toshiba TLCS-12A (1975) - Improved TLCS-12
- Panafacom MN1613 (1980s) - Improved MN1610
- Plessey MIPROC (1975) - PDP-11 compatible, NATO crypto

**32-Bit Processors (2):**
- NEC V60 (1986) - Japan's first major 32-bit
- NEC V70 (1987) - V60 variant

**Bit-Slice Processors (5):**
- TI SBP0400/SBP0401 (1975) - I2L bit-slice
- Motorola MC10800 (1979) - ECL bit-slice
- AMD Am29C101 (1980s) - Four Am2901s in one chip
- Raytheon RP-16 (1970s) - Military-grade 16-bit

**DSP / Signal Processors (4):**
- Motorola DSP56000 (1986) - 24-bit audio DSP
- AT&T DSP-1 (1980) - Bell Labs early DSP
- AT&T DSP-20 (1980s) - Bell Labs DSP
- AMI S28211 (1979) - DSP peripheral for 6800

**Japanese Processors (6):**
- Hitachi HD63484 (1984) - Advanced CRT controller
- Toshiba TLCS-47 (1980s) - 4-bit MCU family
- Toshiba TLCS-870/TLCS-90 (1980s) - 8-bit MCU family
- Sanyo LC87/LC88 (1980s) - 8-bit and 16-bit MCU

**Eastern Bloc Processors (11):**
- U808 (DDR, 1978) - First East German μP (8008 clone)
- U8001 (DDR, 1984) - First 16-bit in Eastern Bloc (Z8000 clone)
- KR580VM1 (Soviet) - Unique 8080 extension with 128KB addressing
- KR1858VM1 (Soviet) - Z80 clone from U880 masks
- IM1821VM85A (Soviet) - 8085 clone
- K1810VM86 (Soviet) - 8086 clone
- KR581IK1/KR581IK2 (Soviet) - MCP-1600 clones
- Tesla MHB8080A (Czechoslovak, 1982) - 8080 clone
- CM630 (Bulgarian) - CMOS 6502 clone (Pravetz)

**Gaming / Arcade Processors (9):**
- Namco 05xx/50xx/51xx/52xx/53xx/54xx - Pac-Man era custom chips
- Hitachi FD1089/FD1094 - Encrypted 68000 (Sega)
- Harris HC-55516 - CVSD sound decoder (Williams pinball)

**Stack Machines (2):**
- WISC CPU/16 (1986) - Writable Instruction Set Computer
- WISC CPU/32 (1980s) - 32-bit WISC

**Other Notable (4):**
- TI TMS34010 (1986) - First programmable GPU
- Bell Labs MAC-4 (1980s) - Telecommunications MCU
- Sharp SM83/LR35902 (1989) - Game Boy CPU

#### Validation
- **196 models total** (was 117)
- **100% pass rate** (196/196 at <10%)
- **195 fully validated** (<5% error)
- **1 passed** (<10% error)

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

### [6.0.0] - Planned
- Instruction timing collection and refinement (Phase 5)
