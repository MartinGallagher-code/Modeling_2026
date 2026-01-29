# Performance Comparison Matrix

## Comparative Analysis of Pre-1986 Microprocessors

This document provides side-by-side comparisons of key performance metrics across all processors in the collection.

---

## Master Comparison Table

### 4-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Power | Notes |
|-----------|------|-------------|-------------|-----|------|-------|-------|
| Intel 4004 | 1971 | 0.74 | 2,300 | 0.05 | 0.037 | 1W | First commercial µP |
| Intel 4040 | 1974 | 0.74 | 3,000 | 0.06 | 0.044 | 1W | +Interrupts, +stack |
| Rockwell PPS-4 | 1972 | 0.20 | 5,000 | 0.03 | 0.006 | 0.5W | **Third** commercial µP |
| PPS-4/1 | 1976 | 0.25 | 6,000 | 0.03 | 0.008 | 0.3W | Single-chip PPS-4 |
| NEC µCOM-4 | 1972 | 1.00 | 2,500 | 0.04 | 0.040 | 0.5W | Japanese 4-bit |
| NEC µPD751 | 1974 | 1.00 | 3,000 | 0.04 | 0.040 | 0.5W | Early 4-bit MCU |
| TI TMS1000 | 1974 | 0.40 | 8,000 | 0.17 | 0.067 | <0.5W | First mass MCU |

### 8-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| Intel 8008 | 1972 | 0.50 | 3,500 | 0.04 | 0.020 | 16 KB | First 8-bit |
| Intel 8080 | 1974 | 2.00 | 4,500 | 0.10 | 0.200 | 64 KB | Industry standard |
| Intel 8085 | 1976 | 3.00 | 6,500 | 0.11 | 0.330 | 64 KB | Single +5V |
| MOS 6502 | 1975 | 1.00 | 3,510 | 0.33 | 0.330 | 64 KB | $25 revolution |
| MOS 6507 | 1975 | 1.00 | 3,510 | 0.33 | 0.330 | 8 KB | Atari 2600 CPU |
| MOS 6509 | 1980 | 2.00 | 4,000 | 0.32 | 0.640 | 1 MB | CBM-II bank switch |
| Ricoh 2A03 | 1983 | 1.79 | 3,510 | 0.33 | 0.591 | 64 KB | NES CPU (no BCD) |
| WDC 65C02 | 1983 | 2.00 | 10,000 | 0.35 | 0.700 | 64 KB | CMOS 6502 |
| Rockwell R65C02 | 1983 | 2.00 | 10,000 | 0.35 | 0.700 | 64 KB | CMOS 6502 + ext |
| Synertek SY6502A | 1978 | 2.00 | 3,510 | 0.33 | 0.660 | 64 KB | Licensed 6502 |
| Zilog Z80 | 1976 | 2.50 | 8,500 | 0.12 | 0.300 | 64 KB | CP/M standard |
| NEC µPD780 | 1976 | 2.50 | 8,500 | 0.12 | 0.300 | 64 KB | Z80 clone |
| Hitachi HD64180 | 1985 | 6.00 | 15,000 | 0.12 | 0.720 | 512 KB | Z180 equivalent |
| Zilog Z180 | 1985 | 6.00 | 15,000 | 0.12 | 0.720 | 512 KB | Z80 + MMU |
| Motorola 6800 | 1974 | 1.00 | 4,100 | 0.10 | 0.100 | 64 KB | First Motorola |
| Motorola 6809 | 1979 | 1.00 | 9,000 | 0.14 | 0.140 | 64 KB | Best 8-bit arch |
| Hitachi 6309 | 1982 | 2.00 | 10,000 | 0.18 | 0.360 | 64 KB | Best 8-bit ever |
| Hitachi HD6301 | 1983 | 1.00 | 9,000 | 0.13 | 0.130 | 64 KB | Enhanced 6801 |
| Fujitsu MB8861 | 1977 | 1.00 | 4,100 | 0.10 | 0.100 | 64 KB | 6800 clone |
| RCA 1802 | 1976 | 2.00 | 5,000 | 0.05 | 0.100 | 64 KB | Rad-hard, space |
| RCA CDP1804 | 1980 | 4.00 | 6,000 | 0.06 | 0.240 | 64 KB | +Timer |
| RCA CDP1805 | 1984 | 4.00 | 6,500 | 0.07 | 0.280 | 64 KB | +Counter/timer |
| RCA CDP1806 | 1985 | 4.00 | 6,500 | 0.07 | 0.280 | 64 KB | Final COSMAC |
| Fairchild F8 | 1975 | 2.00 | 5,000 | 0.08 | 0.160 | 64 KB | Two-chip design |
| Mostek 3870 | 1977 | 4.00 | 5,500 | 0.08 | 0.320 | 64 KB | F8 single-chip |
| Signetics 2650 | 1975 | 1.00 | 6,000 | 0.09 | 0.090 | 32 KB | Unique ISA |
| SC/MP | 1973 | 1.00 | 5,000 | 0.08 | 0.080 | 64 KB | Simple µP |
| Sharp LH5801 | 1981 | 1.30 | 8,000 | 0.10 | 0.130 | 64 KB | Pocket computer |
| Intersil 6100 | 1974 | 4.00 | 4,000 | 0.08 | 0.320 | 4 KW | PDP-8 on chip |
| Harris HM6100 | 1978 | 4.00 | 4,000 | 0.09 | 0.360 | 4 KW | Faster 6100 |

### 8-Bit MCUs

| Processor | Year | Clock (MHz) | ROM | RAM | IPC | Notes |
|-----------|------|-------------|-----|-----|-----|-------|
| Intel 8048 | 1976 | 6.00 | 1 KB | 64 B | 0.08 | MCS-48 flagship |
| Intel 8039 | 1976 | 6.00 | ext | 128 B | 0.08 | MCS-48 ROM-less |
| Intel 8051 | 1980 | 12.0 | 4 KB | 128 B | 0.09 | Still manufactured! |
| Intel 8096 | 1982 | 12.0 | 8 KB | 232 B | 0.12 | Automotive standard |
| Motorola 6805 | 1979 | 4.00 | 1 KB | 64 B | 0.08 | Low-cost MCU |
| Motorola 68HC05 | 1984 | 4.00 | 4 KB | 128 B | 0.08 | CMOS 6805 |
| Motorola 68HC11 | 1985 | 2.00 | 8 KB | 256 B | 0.09 | Enhanced 6801 |
| Rockwell R6511 | 1980 | 2.00 | 4 KB | 192 B | 0.33 | 6502 + peripherals |
| GI PIC1650 | 1977 | 4.00 | 0.5KB | 32 B | 0.06 | First PIC |
| Zilog Z8 | 1979 | 8.00 | 2 KB | 144 B | 0.09 | Zilog MCU |

### 16-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| National IMP-16 | 1973 | 0.75 | - | 0.06 | 0.045 | 64 KB | Early bit-slice 16-bit |
| National PACE | 1975 | 2.00 | 10,000 | 0.08 | 0.16 | 64 KB | p-channel MOS |
| GI CP1600 | 1975 | 1.00 | 10,000 | 0.11 | 0.11 | 64 KB | Intellivision CPU |
| Panafacom MN1610 | 1975 | 2.00 | 12,000 | 0.10 | 0.20 | 64 KB | Japanese pioneer |
| Ferranti F100-L | 1976 | 1.00 | 8,000 | 0.10 | 0.10 | 32 KB | British military |
| TI TMS9900 | 1976 | 3.00 | 8,000 | 0.05 | 0.15 | 64 KB | Workspace (slow!) |
| TI TMS9995 | 1981 | 12.0 | 20,000 | 0.06 | 0.72 | 64 KB | Improved TMS9900 |
| WD WD16 | 1977 | 4.00 | 10,000 | 0.10 | 0.40 | 64 KB | LSI-11 compatible |
| DG mN601 | 1977 | 3.00 | 7,000 | 0.10 | 0.30 | 64 KB | microNova |
| Intel 8086 | 1978 | 5.00 | 29,000 | 0.12 | 0.60 | 1 MB | x86 origin |
| Intel 8088 | 1979 | 5.00 | 29,000 | 0.10 | 0.50 | 1 MB | IBM PC |
| Intel 80186 | 1982 | 8.00 | 55,000 | 0.12 | 0.96 | 1 MB | Integrated |
| Intel 80286 | 1982 | 6.00 | 134,000 | 0.15 | 0.90 | 16 MB | Protected mode |
| Motorola 68000 | 1979 | 8.00 | 68,000 | 0.14 | 1.12 | 16 MB | Mac/Amiga/Atari |
| Motorola 68010 | 1982 | 10.0 | 84,000 | 0.14 | 1.40 | 16 MB | Virtual memory |
| Zilog Z8000 | 1979 | 4.00 | 17,500 | 0.11 | 0.44 | 8 MB | Zilog 16-bit |
| NEC V20 | 1984 | 8.00 | 63,000 | 0.12 | 0.96 | 1 MB | Faster 8088 |
| NEC V30 | 1984 | 10.0 | 63,000 | 0.14 | 1.40 | 1 MB | Faster 8086 |
| WDC 65816 | 1984 | 2.80 | 22,000 | 0.30 | 0.84 | 16 MB | SNES, Apple IIGS |

### 32-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| Intel 80386 | 1985 | 16.0 | 275,000 | 0.20 | 3.20 | 4 GB | First 32-bit x86 |
| Intel iAPX 432 | 1981 | 5.00 | 250,000 | 0.05 | 0.25 | 16 MB | Famous failure |
| Motorola 68020 | 1984 | 16.0 | 190,000 | 0.22 | 3.52 | 4 GB | Full 32-bit 68k |
| NS NS32016 | 1982 | 10.0 | 60,000 | 0.10 | 1.00 | 16 MB | Early 32-bit |
| NS NS32032 | 1984 | 10.0 | 70,000 | 0.12 | 1.20 | 4 GB | Improved NS |
| WE WE32000 | 1982 | 14.0 | 125,000 | 0.10 | 1.40 | 4 GB | Unix workstations |
| Berkeley RISC I | 1982 | 1.00 | 44,000 | 0.77 | 0.77 | 32-bit | First RISC (academic) |
| Berkeley RISC II | 1983 | 3.00 | 41,000 | 0.77 | 2.31 | 32-bit | Improved RISC I |
| Stanford MIPS | 1983 | 2.00 | 25,000 | 0.80 | 1.60 | 32-bit | Original academic MIPS |
| ARM1 | 1985 | 6.00 | 25,000 | 0.70 | 4.20 | 26-bit | RISC pioneer |
| ARM2 | 1986 | 8.00 | 30,000 | 0.70 | 5.60 | 26-bit | First production ARM |
| ARM3 | 1989 | 25.0 | 310,000 | 0.75 | 18.75 | 26-bit | First cached ARM |
| ARM6 | 1991 | 33.0 | 35,000 | 0.65 | 21.45 | 32-bit | Foundation of modern |
| MIPS R2000 | 1985 | 8.00 | 110,000 | 0.60 | 4.80 | 4 GB | RISC pioneer |
| SPARC | 1987 | 16.0 | 100,000 | 0.65 | 10.40 | 4 GB | RISC I heritage |
| HP PA-RISC | 1986 | 8.00 | 115,000 | 0.60 | 4.80 | 4 GB | HP workstations |

### Stack Machines (Forth)

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Novix NC4016 | 1983 | 8.00 | 16,000 | 0.80 | 6.40 | Native Forth |
| Harris RTX2000 | 1985 | 10.0 | 25,000 | 0.85 | 8.50 | Improved NC4016 |

### DSPs (Digital Signal Processors)

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| AMI S2811 | 1978 | 8.00 | 10,000 | 0.10 | 0.80 | Early signal processor |
| Signetics 8X300 | 1976 | 8.00 | 6,000 | 0.50 | 4.00 | Bipolar signal proc |
| NEC µPD7720 | 1980 | 8.00 | 20,000 | 0.25 | 2.00 | Speech synthesis |
| TI TMS320C10 | 1982 | 20.0 | 40,000 | 0.25 | 5.00 | First TI DSP |

### Bit-Slice ALUs

| Processor | Year | Bits | Clock (MHz) | Transistors | Notes |
|-----------|------|------|-------------|-------------|-------|
| AMD Am2901 | 1975 | 4 | 10 | 1,200 | Industry standard |
| AMD Am2903 | 1976 | 4 | 12 | 1,500 | Enhanced 2901 |
| Intel 3002 | 1974 | 2 | 5 | 800 | Intel's bit-slice |
| TI SN74S481 | 1976 | 4 | 15 | 1,000 | High-speed ALU |
| MM6701 | 1975 | 4 | 8 | 1,000 | Monolithic bit-slice |

### Math Coprocessors

| Processor | Year | Clock (MHz) | Precision | FLOPS | Notes |
|-----------|------|-------------|-----------|-------|-------|
| AMD Am9511 | 1977 | 3.00 | 32-bit | 8K | First APU |
| AMD Am9512 | 1979 | 4.00 | 64-bit | 15K | Floating-point APU |
| Intel 80287 | 1980 | 8.00 | 80-bit | 50K | 80286 FPU |
| Intel 80387 | 1985 | 16.0 | 80-bit | 200K | 80386 FPU |
| NS NS32081 | 1982 | 10.0 | 64-bit | 30K | NS32000 FPU |
| MC68881 | 1984 | 16.0 | 80-bit | 150K | 68020 FPU |

---

## Performance Rankings

### By Raw MIPS (Higher is Better)

```
MIPS Performance (Relative to Era)

RTX2000 (1985)  █████████████████████████████████████████████████████████ 8.50
NC4016 (1983)   ████████████████████████████████████████████████ 6.40
ARM2 (1986)     ████████████████████████████████████████████ 5.60
TMS320C10       ██████████████████████████████████████ 5.00
MIPS R2000      █████████████████████████████████████ 4.80
ARM1            ████████████████████████████████ 4.20
Signetics 8X300 ██████████████████████████████ 4.00
Motorola 68020  ██████████████████████████ 3.52
Intel 80386     █████████████████████████ 3.20
Berkeley RISC II ██████████████████ 2.31
NEC µPD7720     ███████████████ 2.00
Stanford MIPS   ████████████ 1.60
NEC V30         ███████████ 1.40
Motorola 68010  ███████████ 1.40
WE32000         ███████████ 1.40
NS32032         █████████ 1.20
Motorola 68000  █████████ 1.12
NS32016         ████████ 1.00
NEC V20         ████████ 0.96
Intel 80186     ████████ 0.96
Intel 80286     ███████ 0.90
65816           ██████ 0.84
Berkeley RISC I █████ 0.77
TMS9995         █████ 0.72
WDC 65C02       █████ 0.70
Intel 8086      █████ 0.60
Ricoh 2A03      █████ 0.59
Intel 8088      ████ 0.50
Z8000           ████ 0.44
Hitachi 6309    ███ 0.36
Z80             ███ 0.30
8085            ███ 0.33
6502            ███ 0.33
8080            ██ 0.20
TMS9900         █ 0.15
6809            █ 0.14
```

### By IPC Efficiency (Higher is Better)

```
IPC (Instructions Per Cycle)

RTX2000         █████████████████████████████████████████████████████████████████████████████████████ 0.85
NC4016          ████████████████████████████████████████████████████████████████████████████████ 0.80
Stanford MIPS   ████████████████████████████████████████████████████████████████████████████████ 0.80
Berkeley RISC   █████████████████████████████████████████████████████████████████████████████ 0.77
ARM3            ███████████████████████████████████████████████████████████████████████████ 0.75
ARM1/ARM2       ██████████████████████████████████████████████████████████████████████ 0.70
SPARC           █████████████████████████████████████████████████████████████████ 0.65
ARM6            █████████████████████████████████████████████████████████████████ 0.65
MIPS R2000      ████████████████████████████████████████████████████████████ 0.60
HP PA-RISC      ████████████████████████████████████████████████████████████ 0.60
Signetics 8X300 ██████████████████████████████████████████████████ 0.50
WDC 65C02       ███████████████████████████████████ 0.35
MOS 6502/2A03   █████████████████████████████████ 0.33
R6511           █████████████████████████████████ 0.33
65816           ██████████████████████████████ 0.30
Motorola 68020  ██████████████████████ 0.22
Intel 80386     ████████████████████ 0.20
Hitachi 6309    ██████████████████ 0.18
Intel 80286     ███████████████ 0.15
NEC V30         ██████████████ 0.14
Motorola 68000  ██████████████ 0.14
Motorola 6809   ██████████████ 0.14
NEC V20         ████████████ 0.12
Intel 8086      ████████████ 0.12
Z80/µPD780      ████████████ 0.12
8085            ███████████ 0.11
CP1600          ███████████ 0.11
Intel 8080      ██████████ 0.10
8051            █████████ 0.09
8088            ██████████ 0.10
TMS9995         ██████ 0.06
RCA 1802        █████ 0.05
TMS9900         █████ 0.05
iAPX 432        █████ 0.05 ← OOP overhead!
```

### By Transistor Efficiency (MIPS per 1000 Transistors)

```
MIPS per 1000 Transistors (Higher = More Efficient Design)

ARM2            █████████████████████████████████████████████████████████████████████████████████████████████ 0.187
ARM1            ████████████████████████████████████████████████████████████████████████████████████ 0.168
6502/2A03       █████████████████████████████████████████████████████████████████████████████████ 0.094
NC4016          ████████████████████████████████████████████████████████████████████████████████ 0.400
Stanford MIPS   ████████████████████████████████████████████████████████████████ 0.064
RTX2000         █████████████████████████████████████████████████████████████████████ 0.340
Berkeley RISC II ██████████████████████████████████████████████████████████ 0.056
6507            ████████████████████████████████████████████████████████████████████████████████ 0.094
ARM6            ███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████ 0.613
SPARC           ████████████████████████████████████████████████████████████████████████████████████████████████████████ 0.104
MIPS R2000      ████████████████████████████████████████████ 0.044
8080            ███████████████████████████████████████████ 0.044
Z80             ███████████████████████████████████████ 0.035
6809            ███████████████ 0.016
Motorola 68000  ████████████████ 0.016
Intel 8086      ████████████████████ 0.021
Intel 80386     ████████████ 0.012
Motorola 68020  ██████████████████ 0.019
Intel 80286     ███████ 0.007
iAPX 432        █ 0.001 ← Bloated!
```

**Key Insights:**
- ARM's RISC architecture delivered **10-20× the transistor efficiency** of contemporary CISC designs!
- Stack machines (NC4016, RTX2000) achieved remarkable efficiency through hardware Forth
- The 6502 family (including NES's 2A03) remained among the most efficient designs ever

---

## Feature Comparison Matrix

### Memory Architecture

| Processor | Address Bits | Max Memory | Segments | Virtual | Cache |
|-----------|--------------|------------|----------|---------|-------|
| 8080 | 16 | 64 KB | No | No | No |
| Z80 | 16 | 64 KB | No | No | No |
| 6502 | 16 | 64 KB | No | No | No |
| 8086 | 20 | 1 MB | Yes (4) | No | No |
| 80286 | 24 | 16 MB | Yes | Yes | No |
| 80386 | 32 | 4 GB | Yes | Yes | No* |
| 68000 | 24 | 16 MB | No | No | No |
| 68020 | 32 | 4 GB | No | Yes | 256B IC |
| ARM1 | 26 | 64 MB | No | No | No |

*80386 supported external cache

### Register Architecture

| Processor | GP Regs | Accumulators | Index | Stack | Special |
|-----------|---------|--------------|-------|-------|---------|
| 8080 | 6 | 1 (A) | 2 (HL, DE) | External | Flags |
| Z80 | 14 | 2 (A, A') | 4 | External | I, R |
| 6502 | 0 | 1 (A) | 2 (X, Y) | Hardware | P |
| 6809 | 0 | 2 (A, B/D) | 2 (X, Y) | 2 (U, S) | DP, CC |
| 8086 | 8 | 1 (AX) | 4 | 1 (SP) | Segment |
| 68000 | 8 (D) | Any D reg | 7 (A) | 2 (A7) | CCR, SR |
| ARM1 | 16 | Any | Any | R13 | R15=PC |
| MIPS | 32 | Any | Any | $sp | HI, LO |

### Pipeline Comparison

| Processor | Stages | Prefetch | Branch Penalty |
|-----------|--------|----------|----------------|
| 8080 | 1 | No | 0 |
| Z80 | 1 | No | 0 |
| 6502 | 1 | No | 0 |
| 8086 | 2 | 6 bytes | 4+ cycles |
| 80286 | 3 | 6 bytes | 3+ cycles |
| 80386 | 4 | 16 bytes | 4+ cycles |
| 68000 | 2 | 2 words | 4+ cycles |
| 68020 | 3 | 256B cache | 3+ cycles |
| ARM1 | 3 | - | 2 cycles |
| MIPS R2000 | 5 | - | 1 cycle (delay slot) |

---

## Architectural Innovations by Processor

| Processor | Key Innovation |
|-----------|----------------|
| 4004 | First microprocessor |
| PPS-4 | Third commercial µP, calculator-focused |
| 8008 | First 8-bit |
| 8080 | Practical computing |
| 6502 | $25 price point, zero-page addressing |
| 6507 | 6502 in minimal package (Atari 2600) |
| Ricoh 2A03 | 6502 without BCD + audio (NES) |
| Z80 | 8080 superset, index registers |
| 6809 | Position-independent code, best 8-bit ISA |
| Hitachi 6309 | Native mode, 32-bit operations, best 8-bit ever |
| 8086 | Segmented memory, x86 foundation |
| 68000 | 32-bit registers, orthogonal ISA |
| 80286 | Protected mode, privilege levels |
| 80386 | Paging, 32-bit x86 |
| Berkeley RISC I | Register windows, first RISC |
| Berkeley RISC II | Refined register windows → SPARC |
| Stanford MIPS | Interlocked pipeline → commercial MIPS |
| ARM1 | RISC simplicity, load/store, power efficiency |
| R2000 | 5-stage pipeline, delay slots |
| SPARC | Register windows from RISC I/II heritage |
| 1802 | Radiation hardness, CMOS pioneer |
| 8051 | Integrated peripherals, bit addressing |
| 8096 | HSI/HSO for real-time control |
| TMS9900 | Workspace registers in RAM (innovative but slow) |
| CP1600 | Intellivision CPU, 10-bit opcodes |
| NC4016/RTX2000 | Hardware Forth stack machines |
| TMS320C10 | First successful commercial DSP |
| µPD7720 | Early DSP for speech synthesis |
| Signetics 8X300 | Bipolar signal processor |
| Am2901 | Industry standard bit-slice |
| Am9511 | First arithmetic processing unit |

---

## Cost vs Performance (1985 Prices)

```
                    Price vs Performance (circa 1985)
                    
    $500 ┤
         │                                    ● 80386
    $400 ┤
         │
    $300 ┤                          ● 68020
         │
    $200 ┤              ● 80286
         │
    $100 ┤   ● 68000
         │ ● 8086
     $50 ┤
         │
     $10 ┼── ● Z80  ● 6502
         │
      $0 ┼────┬────┬────┬────┬────┬────┬────┬────┬
             0.5   1    1.5   2    2.5   3   3.5   4
                              MIPS

    Best value: 6502, Z80 (low cost, adequate performance)
    Premium: 80386, 68020 (high performance, high cost)
```

---

## Power Efficiency

| Processor | Power (W) | MIPS | MIPS/Watt |
|-----------|-----------|------|-----------|
| CMOS 6502 | 0.05 | 0.10 | 2.00 |
| CMOS Z80 | 0.10 | 0.30 | 3.00 |
| RCA 1802 | 0.01 | 0.10 | 10.00 |
| ARM1 | 0.10 | 3.00 | **30.00** |
| Intel 8088 | 1.80 | 0.50 | 0.28 |
| Intel 80386 | 3.00 | 3.20 | 1.07 |
| Motorola 68020 | 2.50 | 3.52 | 1.41 |

**Key Insight:** ARM1's power efficiency (30 MIPS/W) was **100× better** than the 8088, foreshadowing ARM's mobile dominance.

---

## Benchmark Comparisons

### Dhrystone Performance (Approximate)

| Processor | Clock | Dhrystones/sec |
|-----------|-------|----------------|
| Intel 8088 @ 4.77 MHz | 4.77 | 330 |
| Intel 80286 @ 6 MHz | 6.00 | 1,250 |
| Intel 80386 @ 16 MHz | 16.0 | 4,500 |
| Motorola 68000 @ 8 MHz | 8.00 | 1,500 |
| Motorola 68020 @ 16 MHz | 16.0 | 5,200 |
| ARM1 @ 6 MHz | 6.00 | 3,600 |

### Whetstone Performance (Floating Point)

| Processor | Notes |
|-----------|-------|
| 8088 | Required 8087 coprocessor |
| 80286 | Required 80287 coprocessor |
| 80386 | Required 80387 coprocessor |
| 68020 | Required 68881 FPU |
| ARM1 | No FPU (software emulation) |

---

## Summary: Key Takeaways

1. **RISC Revolution**: ARM and MIPS demonstrated dramatically better efficiency than CISC designs (10-30× better transistor efficiency). Berkeley RISC I/II and Stanford MIPS proved the concepts that led to SPARC and commercial MIPS.

2. **The 6502 Value**: At $25, the 6502 delivered exceptional IPC for its transistor count. Its variants powered the Apple II, Commodore 64, Atari 2600, and NES - the most influential platforms of the era.

3. **x86 Won by Compatibility**: Despite architectural compromises, x86's backward compatibility ensured its survival. The NEC V20/V30 showed even 15% faster compatible chips couldn't displace Intel.

4. **68000 vs 8086**: The 68000 was architecturally superior but lost the PC market; won in workstations (Sun, HP), gaming (Amiga, Atari ST, Genesis), and early Mac.

5. **iAPX 432 Disaster**: Object-oriented architecture sounded good but resulted in 10× worse performance than expected - a cautionary tale about premature complexity.

6. **Power Efficiency Matters**: ARM1's efficiency advantage in 1985 predicted its dominance in mobile computing 25 years later.

7. **Stack Machines Excel at Forth**: NC4016 and RTX2000 achieved remarkable IPC through hardware stack architecture, though limited to Forth applications.

8. **TMS9900's Memory-to-Memory Penalty**: Keeping registers in RAM seemed clever but resulted in CPI ~20, making it one of the slowest 16-bit processors despite a 3 MHz clock.

9. **Japanese Clones Proved Compatibility**: NEC µPD780 (Z80), Fujitsu MB8861 (6800), and others demonstrated that compatible clones could succeed, presaging the PC clone era.

10. **The DSP Parallel Path**: While general-purpose CPUs evolved toward RISC, DSPs like TMS320C10 and µPD7720 pioneered the specialized, parallel architectures that would eventually merge back into GPUs and AI accelerators.

---

**Document Version:** 2.0
**Last Updated:** January 29, 2026
**Processors Covered:** 117
