# Microprocessor Family Trees

## Processor Lineages and Relationships (1971-1994)

This document traces the evolutionary relationships between all **117 processors** in the collection, showing how architectures developed and influenced each other.

---

## Intel Family Tree

### 4-Bit Line (1971-1974)

```
Intel 4004 (1971) ✓
    │   First microprocessor, 4-bit, calculator-focused
    │
    └──► Intel 4040 (1974) ✓
            Enhanced: interrupts, larger stack, more instructions
```

### 8-Bit Line (1972-1980)

```
Intel 8008 (1972) ✓
    │   First 8-bit, derived from Datapoint 2200 design
    │
    └──► Intel 8080 (1974) ✓
            │   Industry standard, Altair computer
            │
            ├──► Intel 8085 (1976) ✓
            │       Single +5V supply, serial I/O, same ISA
            │
            ├──► Zilog Z80 (1976) ✓ ─────────────────────────────┐
            │       8080 superset, index registers, by ex-Intel   │
            │                                                      │
            └──► NEC μPD780 (1976) ✓                              │
                    Z80 clone for Japanese market                  │
                                                                   │
    ┌──────────────────────────────────────────────────────────────┘
    │
    └──► Z80A (1976) ✓ ──► Z80B (1978) ✓ ──► Z180 (1985) ✓
            4 MHz            6 MHz            Enhanced + MMU
                                                   │
                                                   └──► Hitachi HD64180 (1985) ✓
                                                           Z180 equivalent
```

### MCS-48 MCU Line (1976-1980)

```
Intel 8048 (1976) ✓
    │   First successful single-chip MCU
    │
    ├──► Intel 8035/8039 (1976) ✓
    │       ROM-less variants
    │
    └──► Intel 8748 (1977) ✓
            EPROM version for development
```

### MCS-51 MCU Line (1980+)

```
Intel 8051 (1980) ✓
    │   Most successful MCU ever - still manufactured!
    │
    └──► Intel 8751 (1980) ✓
            EPROM version
```

### 16-bit MCU Line (1982+)

```
Intel 8096 (1982) ✓
    │   16-bit MCU, dominated automotive 1985-2005
    │   Register file architecture, hardware multiply/divide
    │
    └──► 80196, 80296...
            Enhanced versions
```

### x86 Line (1978-1993)

```
Intel 8086 (1978) ✓
    │   16-bit, segmented memory, x86 origin
    │
    ├──► Intel 8088 (1979) ✓
    │       │   8-bit bus version, IBM PC
    │       │
    │       ├──► NEC V20 (1984) ✓
    │       │       Pin-compatible, 15% faster, 8080 mode
    │       │
    │       └──► NEC V30 (1984) ✓
    │               16-bit bus version of V20
    │
    ├──► Intel 80186 (1982) ✓
    │       │   Integrated peripherals
    │       │
    │       └──► Intel 80188 (1982) ✓
    │               8-bit bus version
    │
    └──► Intel 80286 (1982) ✓
            │   Protected mode, 16 MB virtual
            │
            └──► Intel 80386 (1985) ✓
                    │   32-bit, paging, modern x86
                    │
                    └──► Intel 80486 (1989) ✓
                            │   On-chip cache + FPU
                            │
                            └──► Intel Pentium (1993) ✓
                                    Superscalar, dual pipeline
```

### FPU Line (1980-1987)

```
Intel 8087 (1980)
    │   x87 FPU for 8086/8088
    │
    ├──► Intel 80287 (1982) ✓
    │       FPU for 80286
    │
    └──► Intel 80387 (1987) ✓
            FPU for 80386
```

### Bit-Slice Line (1974)

```
Intel 3001/3002 (1974) ✓
    │   2-bit slice CPU building blocks
    │   Bipolar Schottky technology
    │
    └──► (Used to build custom processors)
```

### Experimental (1981, 1989)

```
Intel iAPX 432 (1981) ✓
    │   Object-oriented architecture
    │   Famous failure: 10x slower than expected
    │
    (Dead end)

Intel i860 (1989) ✓
    │   "Cray on a chip" - VLIW/vector
    │
    (Limited success in graphics cards)
```

---

## Motorola Family Tree

### 6800 Line (1974-1985)

```
Motorola 6800 (1974) ✓
    │   First Motorola microprocessor
    │
    ├──► Motorola 6802 (1977) ✓
    │       6800 + 128B RAM + clock generator
    │
    ├──► Motorola 6801 (1978) ✓
    │       │   6800 + ROM + RAM + I/O = MCU
    │       │
    │       └──► Hitachi HD6301 (1983) ✓
    │               Enhanced clone, 8% faster
    │
    ├──► Fujitsu MB8861 (1977) ✓
    │       6800 clone for Japanese market
    │
    ├──► Motorola 6805 (1979) ✓
    │       │   Low-cost MCU, simplified ISA
    │       │
    │       └──► Motorola 68HC05 (1984) ✓
    │               CMOS version
    │
    ├──► Motorola 6809 (1979) ✓
    │       │   "Best 8-bit ever" - position-independent code
    │       │
    │       └──► Hitachi 6309 (1982) ✓
    │               Enhanced 6809 with extra registers
    │               Native mode 15% faster
    │
    └──► Motorola 68HC11 (1985) ✓
            Popular automotive MCU
```

### 68000 Line (1979-1994)

```
Motorola 68000 (1979) ✓
    │   16/32-bit, Mac/Amiga/Atari ST/Genesis
    │
    ├──► Motorola 68008 (1982) ✓
    │       8-bit bus version (cost reduction)
    │
    ├──► Motorola 68010 (1982) ✓
    │       Virtual memory support
    │
    └──► Motorola 68020 (1984) ✓
            │   Full 32-bit, on-chip cache
            │
            └──► Motorola 68030 (1987) ✓
                    │   On-chip MMU
                    │
                    └──► Motorola 68040 (1990) ✓
                            │   On-chip FPU
                            │
                            └──► Motorola 68060 (1994) ✓
                                    Superscalar, last 68k
```

### 68k FPU Line (1984-1988)

```
Motorola 68881 (1984) ✓
    │   FPU for 68020
    │
    └──► Motorola 68882 (1988) ✓
            Enhanced FPU
```

---

## MOS Technology / WDC Family Tree

```
MOS 6502 (1975) ✓
    │   "$25 revolution" - Apple II, C64, NES, Atari
    │   Designed by ex-Motorola team
    │
    ├──► MOS 6507 (1975) ✓
    │       Reduced pins (28), Atari 2600
    │
    ├──► MOS 6509 (1980) ✓
    │       Bank switching, CBM-II
    │
    ├──► MOS 6510 (1982) ✓
    │       6502 + I/O port, Commodore 64
    │
    ├──► Ricoh 2A03 (1983) ✓
    │       6502 + audio, no BCD, NES/Famicom
    │
    ├──► Synertek SY6502A (1978) ✓
    │       Licensed 6502, speed-binned to 2 MHz
    │
    ├──► Rockwell R6511 (1980) ✓
    │       6502 + on-chip peripherals
    │
    ├──► Rockwell R65C02 (1983) ✓
    │       CMOS 6502 + bit manipulation instructions
    │
    └──► WDC 65C02 (1983) ✓
            │   CMOS, new instructions, bug fixes
            │
            └──► WDC 65816 (1984) ✓
                    16-bit extension, Apple IIGS, SNES
```

---

## Zilog Family Tree

```
Zilog Z80 (1976) ✓
    │   8080 superset, CP/M standard
    │   Founded by ex-Intel engineers
    │
    ├──► Zilog Z80A (1976) ✓
    │       4 MHz speed grade
    │
    ├──► Zilog Z80B (1978) ✓
    │       6 MHz speed grade
    │
    ├──► Zilog Z180 (1985) ✓
    │       Z80 + MMU + DMA + serial
    │
    └──► Zilog Z280 (1985)
            Failed Z80 successor (too complex)

Zilog Z8 (1979) ✓
    │   MCU family (not Z80-related)
    │
    (Separate architecture)

Zilog Z8000 (1979) ✓
    │   16-bit, segmented memory
    │
    └──► Zilog Z80000 (1986) ✓
            32-bit, limited success
```

---

## RCA COSMAC Family Tree

```
RCA 1802 (1976) ✓
    │   First CMOS microprocessor
    │   Radiation-hardened, used in Voyager
    │
    ├──► RCA CDP1804 (1980) ✓
    │       On-chip RAM, timer
    │
    ├──► RCA CDP1805 (1984) ✓
    │       Enhanced, New Horizons mission
    │
    └──► RCA CDP1806 (1985) ✓
            Final COSMAC
```

---

## Texas Instruments Family Tree

```
TI TMS1000 (1974) ✓
    │   First mass-produced MCU
    │   Billions shipped (calculators, Speak & Spell)
    │
    └──► TMS1100, TMS1300, etc.
            ROM/RAM variants

TI TMS9900 (1976) ✓
    │   16-bit, workspace registers in RAM
    │   TI-99/4A home computer (CPI ~20, very slow)
    │
    └──► TI TMS9995 (1981) ✓
            On-chip RAM, faster

TI TMS320C10 (1982) ✓
    │   First TI DSP
    │
    └──► TMS320 family (DSP dynasty)
```

---

## ARM Family Tree

```
Acorn ARM1 (1985) ✓
    │   First ARM, RISC pioneer
    │   26-bit address, 3-stage pipeline
    │
    └──► ARM2 (1986) ✓
            │   First production ARM, Archimedes
            │
            └──► ARM3 (1989) ✓
                    │   First cached ARM
                    │
                    └──► ARM6 (1991) ✓
                            32-bit address
                            │
                            └──► (ARM7, ARM9, Cortex...)
                                    Mobile dominance
```

---

## RISC Pioneers

```
Berkeley RISC I (1982) ✓
    │   First RISC processor (academic)
    │   Register windows, delayed branches
    │
    └──► Berkeley RISC II (1983) ✓
            │   Improved version, 138 registers
            │
            └──► Sun SPARC (1987) ✓
                    Commercial RISC from Berkeley research

Stanford MIPS (1983) ✓
    │   Academic MIPS prototype
    │   5-stage pipeline concept
    │
    └──► MIPS R2000 (1985) ✓
            │   Commercial 5-stage pipeline
            │
            └──► (R3000, R4000, R10000...)

HP PA-RISC (1986) ✓
    │   HP workstation RISC
    │
    └──► (PA-7000, PA-8000...)

DEC Alpha 21064 (1992) ✓
    │   64-bit, fastest of its era (IPC 1.3)
    │
    └──► (21164, 21264...)

AIM PowerPC 601 (1993) ✓
    │   Apple/IBM/Motorola alliance
    │
    └──► (603, 604, G3, G4, G5...)
```

---

## 4-Bit Processor Family Tree

```
Intel 4004 (1971) ✓
    │   First microprocessor
    │
    └──► Intel 4040 (1974) ✓
            Enhanced version

Rockwell PPS-4 (1972) ✓
    │   Third commercial microprocessor
    │   Serial ALU, used in pinball machines
    │
    └──► Rockwell PPS-4/1 (1976) ✓
            Single-chip variant

NEC μCOM-4 (1972) ✓
    │   TMS1000 competitor
    │
    └──► NEC μPD751 (1974) ✓
            Enhanced 4-bit MCU

TI TMS1000 (1974) ✓
    │   First mass-produced MCU
    │
    └──► (Billions shipped)
```

---

## Bit-Slice and ALU Family Tree

```
AMD Am2901 (1975) ✓
    │   4-bit slice ALU, industry standard
    │
    └──► AMD Am2903 (1976) ✓
            Enhanced version

Intel 3001/3002 (1974) ✓
    │   2-bit slice, Intel's bit-slice family
    │
    (Used in custom CPU designs)

TI SN74S481 (1976) ✓
    │   4-bit slice ALU
    │
    (Used in minicomputers)

Monolithic Memories 6701 (1975) ✓
    │   4-bit slice ALU competitor
    │
    (Am2901 alternative)
```

---

## Math Coprocessor / APU Family Tree

```
AMD Am9511 (1977) ✓
    │   First math coprocessor for 8-bit systems
    │   Stack-based, 32-bit floating point
    │
    └──► AMD Am9512 (1979) ✓
            Enhanced, 64-bit double precision

Intel 8087 (1980)
    │
    ├──► Intel 80287 (1982) ✓
    │
    └──► Intel 80387 (1987) ✓

Motorola 68881 (1984) ✓
    │
    └──► Motorola 68882 (1988) ✓

National NS32081 (1982) ✓
    │   FPU for NS32000 family
    │
    (IEEE 754 compliant)
```

---

## DSP / Signal Processor Family Tree

```
NEC μPD7720 (1980) ✓
    │   Early DSP, speech synthesis
    │   Used in Super Nintendo audio
    │
    └──► (μPD7725, μPD77C25...)

TI TMS320C10 (1982) ✓
    │   First TI DSP
    │
    └──► TMS320 dynasty

AMI S2811 (1978) ✓
    │   Early signal processor
    │
    (Modems, telecommunications)

Signetics 8X300 (1976) ✓
    │   Bipolar signal processor
    │   Single-cycle execution
    │
    (High-speed I/O controllers)
```

---

## 16-Bit Pioneer Family Tree

```
National IMP-16 (1973) ✓
    │   Early 16-bit (bit-slice based)
    │
    └──► National PACE (1975) ✓
            Single-chip 16-bit, p-channel MOS

Data General mN601 (1977) ✓
    │   microNova - Nova architecture on a chip
    │
    (Eclipse replacement)

Western Digital WD16 (1977) ✓
    │   LSI-11 (PDP-11) compatible
    │
    (DEC minicomputer replacement)

Ferranti F100-L (1976) ✓
    │   British military 16-bit
    │
    (Defense applications)

GI CP1600 (1975) ✓
    │   Intellivision game console CPU
    │   16-bit with 10-bit opcodes
    │
    (Gaming)

Panafacom MN1610 (1975) ✓
    │   Early Japanese 16-bit
    │
    (Japanese computing)
```

---

## Other Notable Lines

### Fairchild F8 (1975)

```
Fairchild F8 (1975) ✓
    │   Two-chip architecture (CPU + PSU)
    │
    └──► Mostek 3870 (1977) ✓
            Single-chip F8 derivative
```

### National Semiconductor

```
National SC/MP (1974) ✓
    │   Simple, low-cost 8-bit
    │
    (End of line)

National NS32016 (1982) ✓
    │   Early 32-bit CISC
    │
    └──► National NS32032 (1984) ✓
            │   Improved version
            │
            └──► NS32081 FPU (1982) ✓
```

### PIC Microcontrollers

```
GI PIC1650 (1977) ✓
    │   First PIC (Peripheral Interface Controller)
    │
    └──► (PIC16, PIC18, PIC24, dsPIC...)
            Billions shipped
```

### Intersil / Harris 6100

```
Intersil 6100 (1975) ✓
    │   CMOS PDP-8 on a chip
    │   12-bit word size
    │
    └──► Harris HM6100 (1978) ✓
            Faster CMOS version
```

### Japanese Processors

```
Sharp LH5801 (1981) ✓
    │   Sharp pocket computer CPU
    │
    (Calculator/pocket computer market)

Panafacom MN1610 (1975) ✓
    │   Early Japanese 16-bit
    │
    (One of Japan's first 16-bit processors)
```

### Stack Machines

```
Novix NC4016 (1985) ✓
    │   Forth stack processor
    │
    └──► Harris RTX2000 (1988) ✓
            Enhanced Forth processor
```

### Other

```
Signetics 2650 (1975) ✓
    │   Unique 8-bit architecture
    │
    (Limited success)

WE 32000 (1984) ✓
    │   AT&T UNIX processor
    │
    (UNIX workstations)
```

---

## Cross-Pollination and Influence

```
                    ┌─────────────────────────────────────┐
                    │         INFLUENCE MAP               │
                    └─────────────────────────────────────┘

Intel 8080 ──────────────────────────► Zilog Z80 ──────► NEC μPD780
     │                                      │
     └──────────► NEC V20/V30 ◄────────────┘

Motorola 6800 ───────────────────────► MOS 6502 ──────► Ricoh 2A03
     │                                      │              (NES)
     │                                      ├──► MOS 6507 (Atari 2600)
     └──► 6809 ──► Hitachi 6309            └──► WDC 65816 (SNES)

Berkeley RISC I ──► RISC II ────────────► Sun SPARC
                                               │
                    ARM1 ◄─────────────────────┘
                      │
                      └──────────────► (Mobile revolution)

Stanford MIPS ───────────────────────► MIPS R2000
                                           │
                                           └──► (PlayStation, N64, routers)

Rockwell PPS-4 ──────────────────────► PPS-4/1
     │
     └──► (Third microprocessor lineage)

AMD Am2901 ──────────────────────────► Am2903, TI SN74S481, MM6701
     │
     └──► (Bit-slice computing era)
```

---

## Summary Statistics

| Family | Models in Collection | Year Range |
|--------|---------------------|------------|
| Intel x86 | 12 | 1978-1993 |
| Intel 8-bit | 5 | 1972-1976 |
| Intel MCU | 5 | 1976-1982 |
| Intel Other | 2 | 1974-1989 |
| Motorola 68k | 7 | 1979-1994 |
| Motorola 8-bit | 9 | 1974-1985 |
| MOS/WDC 6502 | 10 | 1975-1984 |
| Zilog | 7 | 1976-1986 |
| ARM | 4 | 1985-1991 |
| RISC Pioneers | 7 | 1982-1993 |
| 4-bit | 6 | 1971-1976 |
| Bit-slice/ALU | 5 | 1974-1976 |
| Math Coprocessors | 5 | 1977-1988 |
| DSP | 4 | 1976-1982 |
| 16-bit Pioneers | 6 | 1973-1977 |
| Japanese | 7 | 1975-1985 |
| RCA COSMAC | 4 | 1976-1985 |
| TI | 4 | 1974-1982 |
| Other | 8 | 1974-1988 |
| **Total** | **117** | **1971-1994** |

---

**Document Version:** 2.0
**Last Updated:** January 29, 2026
**Processors Covered:** 117

✓ = Model included in collection
