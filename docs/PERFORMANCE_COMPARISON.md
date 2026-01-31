# Performance Comparison Matrix

## Comparative Analysis of Historical Microprocessors (1970-1995)

This document provides side-by-side comparisons of key performance metrics across all processors in the collection, spanning from the first commercial microprocessors through the superscalar RISC era.

---

## Master Comparison Table

### 4-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Power | Notes |
|-----------|------|-------------|-------------|-----|------|-------|-------|
| Intel 4004 | 1971 | 0.74 | 2,300 | 0.05 | 0.037 | 1W | First commercial uP |
| Intel 4040 | 1974 | 0.74 | 3,000 | 0.06 | 0.044 | 1W | +Interrupts, +stack |
| Rockwell PPS-4 | 1972 | 0.20 | 5,000 | 0.03 | 0.006 | 0.5W | **Third** commercial uP |
| PPS-4/1 | 1976 | 0.25 | 6,000 | 0.03 | 0.008 | 0.3W | Single-chip PPS-4 |
| NEC uCOM-4 | 1972 | 1.00 | 2,500 | 0.04 | 0.040 | 0.5W | Japanese 4-bit |
| NEC uPD751 | 1974 | 1.00 | 3,000 | 0.04 | 0.040 | 0.5W | Early 4-bit MCU |
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
| NEC uPD780 | 1976 | 2.50 | 8,500 | 0.12 | 0.300 | 64 KB | Z80 clone |
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
| SC/MP | 1973 | 1.00 | 5,000 | 0.08 | 0.080 | 64 KB | Simple uP |
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
| NEC uPD7720 | 1980 | 8.00 | 20,000 | 0.25 | 2.00 | Speech synthesis |
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

## Post-1985 Processor Comparison Tables

### Post-1985 RISC Workstation Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| MIPS R3000 | 1988 | 33 | 120,000 | 0.70 | 23.1 | SGI Indigo, DECstation |
| MIPS R4000 | 1991 | 100 | 1,350,000 | 0.60 | 60.0 | First 64-bit MIPS, 8-stage pipeline |
| MIPS R4400 | 1993 | 150 | 2,200,000 | 0.62 | 93.0 | Improved R4000, SGI Indy |
| MIPS R4600 | 1993 | 133 | 1,900,000 | 0.55 | 73.2 | Low-cost Orion |
| MIPS R8000 | 1994 | 75 | 2,600,000 | 1.20 | 90.0 | Superscalar FP, 2-way |
| MIPS R10000 | 1996 | 200 | 6,700,000 | 1.80 | 360.0 | Out-of-order, 4-way superscalar |
| SuperSPARC | 1992 | 40 | 3,100,000 | 1.10 | 44.0 | 3-way superscalar |
| MicroSPARC | 1992 | 50 | 800,000 | 0.55 | 27.5 | Low-cost SPARCstation |
| HyperSPARC | 1993 | 125 | 800,000 | 0.60 | 75.0 | Ross Technology |
| UltraSPARC | 1995 | 143 | 3,800,000 | 1.40 | 200.2 | 64-bit VIS extensions |
| HP PA-7100 | 1992 | 100 | 850,000 | 0.80 | 80.0 | Single-issue PA-RISC 1.1 |
| HP PA-7200 | 1994 | 120 | 1,260,000 | 1.20 | 144.0 | 2-way superscalar, Alchemist |
| IBM POWER1 | 1990 | 25 | 1,000,000 | 1.50 | 37.5 | Multi-chip, RS/6000 |
| IBM POWER2 | 1993 | 71 | 23,000,000 | 2.00 | 142.0 | Massive multi-chip module |

### Post-1985 x86 and Competitors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Intel 80486 | 1989 | 25-50 | 1,200,000 | 0.60 | 15-30 | Integrated FPU + cache |
| Intel Pentium | 1993 | 60-66 | 3,100,000 | 1.10 | 66-73 | Dual-issue superscalar |
| AMD Am386 | 1991 | 40 | 275,000 | 0.22 | 8.8 | 386-compatible, clock lead |
| AMD Am486 | 1993 | 40 | 1,200,000 | 0.62 | 24.8 | 486-compatible |
| AMD Am5x86 | 1995 | 133 | 1,600,000 | 0.65 | 86.5 | Clock-quadrupled 486 |
| Cyrix Cx486DLC | 1992 | 33 | 600,000 | 0.40 | 13.2 | 486 ISA in 386 pin-out |
| Cyrix Cx5x86 | 1995 | 120 | 2,000,000 | 0.80 | 96.0 | Pentium-class, 6th-gen arch |
| NexGen Nx586 | 1994 | 93 | 3,500,000 | 0.90 | 83.7 | RISC core, x86 front-end |

### Motorola 68k Late Family

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Motorola 68030 | 1987 | 25 | 273,000 | 0.28 | 7.0 | On-chip MMU + caches |
| Motorola 68040 | 1990 | 25 | 1,200,000 | 0.60 | 15.0 | Integrated FPU, 6-stage |
| Motorola 68060 | 1994 | 50 | 2,500,000 | 1.10 | 55.0 | Superscalar, final 68k |

### PowerPC Family

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| PowerPC 601 | 1993 | 80 | 2,800,000 | 1.20 | 96.0 | POWER/PowerPC bridge |
| PowerPC 603 | 1993 | 80 | 1,600,000 | 0.90 | 72.0 | Low-power, 3-issue |
| PowerPC 604 | 1994 | 100 | 3,600,000 | 1.50 | 150.0 | 4-issue superscalar |
| PowerPC 620 | 1996 | 133 | 7,000,000 | 1.60 | 212.8 | First 64-bit PowerPC |

### DEC Alpha

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Alpha 21064 | 1992 | 150 | 1,680,000 | 1.20 | 180.0 | Fastest chip at launch |
| Alpha 21064A | 1993 | 275 | 2,850,000 | 1.20 | 330.0 | Die-shrink speed demon |
| Alpha 21066 | 1993 | 166 | 1,750,000 | 0.90 | 149.4 | Low-cost with I/O |

### Post-1985 ARM Family

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| ARM250 | 1990 | 12 | 35,000 | 0.68 | 8.2 | ARM2 + MMU + cache ctrl |
| ARM610 | 1993 | 33 | 68,000 | 0.65 | 21.5 | ARM6 core, cached |
| ARM7TDMI | 1994 | 40 | 73,000 | 0.60 | 24.0 | Thumb mode, 3-stage |

### Post-1985 Embedded RISC

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Hitachi SH-1 | 1992 | 20 | 400,000 | 0.70 | 14.0 | 16-bit fixed-length ISA |
| Hitachi SH-2 | 1994 | 28 | 500,000 | 0.80 | 22.4 | Sega Saturn, 32x |
| NEC V810 | 1991 | 20 | 380,000 | 0.60 | 12.0 | Virtual Boy CPU |
| NEC V850 | 1993 | 17 | 350,000 | 0.65 | 11.1 | Automotive embedded |
| Motorola ColdFire | 1994 | 33 | 350,000 | 0.55 | 18.2 | 68k-derived embedded |
| Toshiba TX39 | 1994 | 40 | 600,000 | 0.60 | 24.0 | MIPS R3000A core |

### Advanced DSPs

| Processor | Year | Clock (MHz) | Transistors | IPC | MMACS | Notes |
|-----------|------|-------------|-------------|-----|-------|-------|
| TI TMS320C25 | 1986 | 40 | 80,000 | 0.50 | 10.0 | 100ns cycle, DARAM |
| TI TMS320C30 | 1988 | 33 | 500,000 | 0.80 | 16.5 | 32-bit floating-point |
| TI TMS320C40 | 1991 | 50 | 1,000,000 | 0.90 | 25.0 | Multi-processor links |
| TI TMS320C50 | 1991 | 57 | 400,000 | 0.60 | 28.5 | Fixed-point, low power |
| TI TMS320C80 | 1995 | 50 | 4,000,000 | 4.00 | 200.0 | MVP: RISC master + 4 DSPs |
| ADSP-2100 | 1986 | 12.5 | 50,000 | 0.80 | 12.5 | Analog Devices fixed-point |
| ADSP-21020 | 1991 | 33 | 500,000 | 0.90 | 33.0 | 32-bit floating-point |
| AT&T DSP32C | 1988 | 50 | 300,000 | 0.80 | 25.0 | IEEE 754 floating-point |

### Gaming Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Notes |
|-----------|------|-------------|-------------|-----|------|-------|
| Sony R3000A (PS1) | 1994 | 33 | 120,000 | 0.70 | 23.1 | PlayStation CPU + GTE |
| Ricoh 5A22 (SNES) | 1990 | 3.58 | 30,000 | 0.30 | 1.07 | 65C816 + DMA |
| HuC6280 (TG-16) | 1987 | 7.16 | 15,000 | 0.33 | 2.36 | Enhanced 65C02 |
| Sega SVP | 1993 | 23 | 200,000 | 0.50 | 11.5 | Samsung DSP, Virtua Racing |

### Graphics Processors (1990s)

| Processor | Year | Clock (MHz) | Transistors | Mpixels/s | Notes |
|-----------|------|-------------|-------------|-----------|-------|
| S3 86C911 | 1991 | 25 | 350,000 | 10 | First single-chip 2D accel |
| Tseng ET4000 | 1989 | 25 | 250,000 | 8 | VGA/SVGA standard |
| ATI Mach32 | 1992 | 44 | 500,000 | 16 | Integrated bus mastering |
| ATI Mach64 | 1994 | 50 | 800,000 | 25 | Video overlay + 2D accel |
| Weitek P9000 | 1992 | 40 | 600,000 | 14 | High-end 2D, X11 accel |

---

## Performance Rankings

### By Raw MIPS (Higher is Better) -- Pre-1986 Processors

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
NEC uPD7720     ███████████████ 2.00
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

### Post-1985 MIPS Rankings (Higher is Better)

```
MIPS Performance -- Post-1985 Era (1986-1995)

R10000 (1996)       ████████████████████████████████████████████████████████████████████████████ 360
Alpha 21064A (1993) ████████████████████████████████████████████████████████████████████ 330
PPC 620 (1996)      ████████████████████████████████████████████ 213
UltraSPARC (1995)   █████████████████████████████████████████ 200
Alpha 21064 (1992)  █████████████████████████████████████ 180
PPC 604 (1994)      ███████████████████████████████ 150
Alpha 21066 (1993)  ██████████████████████████████ 149
PA-7200 (1994)      █████████████████████████████ 144
POWER2 (1993)       █████████████████████████████ 142
Cx5x86 (1995)       ████████████████████ 96
PPC 601 (1993)      ████████████████████ 96
R4400 (1993)        ███████████████████ 93
R8000 (1994)        █████████████████ 90
Am5x86 (1995)       ██████████████████ 87
NexGen Nx586 (1994) █████████████████ 84
PA-7100 (1992)      ████████████████ 80
HyperSPARC (1993)   ███████████████ 75
R4600 (1993)        ███████████████ 73
Pentium (1993)      ██████████████ 70
R4000 (1991)        ████████████ 60
68060 (1994)        ███████████ 55
SuperSPARC (1992)   █████████ 44
POWER1 (1990)       ████████ 38
486DX-50 (1989)     ██████ 30
Am486 (1993)        █████ 25
ARM7TDMI (1994)     █████ 24
R3000 (1988)        █████ 23
ARM6 (1991)         ████ 21
ARM3 (1989)         ████ 19
68040 (1990)        ███ 15
Am386 (1991)        ██ 9
68030 (1987)        █ 7
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
Z80/uPD780      ████████████ 0.12
8085            ███████████ 0.11
CP1600          ███████████ 0.11
Intel 8080      ██████████ 0.10
8051            █████████ 0.09
8088            ██████████ 0.10
TMS9995         ██████ 0.06
RCA 1802        █████ 0.05
TMS9900         █████ 0.05
iAPX 432        █████ 0.05 <- OOP overhead!
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
iAPX 432        █ 0.001 <- Bloated!
```

**Key Insights:**
- ARM's RISC architecture delivered **10-20x the transistor efficiency** of contemporary CISC designs!
- Stack machines (NC4016, RTX2000) achieved remarkable efficiency through hardware Forth
- The 6502 family (including NES's 2A03) remained among the most efficient designs ever

---

## Superscalar Comparison (1993-1995)

The early 1990s saw the transition from scalar to superscalar execution across all architectures.

| Processor | Year | Issue Width | Pipeline Stages | OoO? | Clock (MHz) | SPECint92 | Notes |
|-----------|------|-------------|-----------------|------|-------------|-----------|-------|
| Intel Pentium | 1993 | 2 | 5 | No | 66 | 65 | In-order dual-issue |
| Motorola 68060 | 1994 | 2 | 6 | Partial | 50 | 60 | Superscalar 68k swan song |
| PowerPC 604 | 1994 | 4 | 6 | Yes | 100 | 160 | Full out-of-order |
| Alpha 21064 | 1992 | 2 | 7 | No | 150 | 100 | In-order, clock speed king |
| Alpha 21064A | 1993 | 2 | 7 | No | 275 | 185 | Die-shrink, max frequency |
| MIPS R4400 | 1993 | 1 | 8 | No | 150 | 95 | Scalar, deep pipeline |
| MIPS R8000 | 1994 | 2 | 7 | No | 75 | 75 | FP superscalar (science) |
| MIPS R10000 | 1996 | 4 | 5-7 | Yes | 200 | 300 | Full OoO, register renaming |
| SuperSPARC | 1992 | 3 | 4 | No | 40 | 50 | 3-issue in-order |
| UltraSPARC | 1995 | 4 | 9 | No | 143 | 155 | VIS SIMD extensions |
| HP PA-7200 | 1994 | 2 | 5 | No | 120 | 130 | Superscalar PA-RISC |
| PowerPC 601 | 1993 | 3 | 4 | No | 80 | 85 | POWER bridge chip |
| NexGen Nx586 | 1994 | 2 | 7 | Partial | 93 | 82 | x86 -> RISC translation |

```
SPECint92 Comparison (Higher is Better)

R10000          ████████████████████████████████████████████████████████████████████████████████████████████ 300
Alpha 21064A    █████████████████████████████████████████████████████████ 185
PPC 604         █████████████████████████████████████████████████ 160
UltraSPARC      ███████████████████████████████████████████████ 155
PA-7200         ████████████████████████████████████████ 130
Alpha 21064     ██████████████████████████████████ 100
R4400           █████████████████████████████ 95
PPC 601         ██████████████████████████ 85
NexGen Nx586    █████████████████████████ 82
R8000           ███████████████████████ 75
Pentium (66)    ████████████████████ 65
68060           ██████████████████ 60
SuperSPARC      ███████████████ 50
```

**Key Insight:** By 1993, out-of-order execution separated the leaders. The Alpha 21064A won on raw clock speed, while the PPC 604 and R10000 showed the future with full out-of-order execution.

---

## RISC vs CISC by Era

### First Generation (1985-1988): RISC Proves the Concept

| Architecture | Processor | Year | MIPS | Transistors | Advantage |
|-------------|-----------|------|------|-------------|-----------|
| RISC | MIPS R2000 | 1985 | 4.8 | 110K | Higher IPC |
| RISC | SPARC | 1987 | 10.4 | 100K | Register windows |
| CISC | Intel 80386 | 1985 | 3.2 | 275K | x86 compatibility |
| CISC | Motorola 68020 | 1984 | 3.5 | 190K | Orthogonal ISA |

**Verdict:** RISC delivered comparable or better MIPS with fewer transistors, but CISC had the software base.

### Second Generation (1989-1992): RISC Pulls Ahead

| Architecture | Processor | Year | MIPS | Transistors | Advantage |
|-------------|-----------|------|------|-------------|-----------|
| RISC | MIPS R4000 | 1991 | 60 | 1.35M | 64-bit, deep pipeline |
| RISC | Alpha 21064 | 1992 | 180 | 1.68M | Raw clock speed |
| RISC | SuperSPARC | 1992 | 44 | 3.1M | 3-way superscalar |
| CISC | Intel 80486 | 1989 | 30 | 1.2M | Integrated FPU+cache |
| CISC | Motorola 68040 | 1990 | 15 | 1.2M | Integrated FPU+MMU |

**Verdict:** RISC clearly ahead. Alpha 21064 was 6x faster than the 486 with similar transistor count.

### Third Generation (1993-1995): Convergence Begins

| Architecture | Processor | Year | MIPS | Transistors | Advantage |
|-------------|-----------|------|------|-------------|-----------|
| RISC | R10000 | 1996 | 360 | 6.7M | Full OoO |
| RISC | PPC 604 | 1994 | 150 | 3.6M | 4-issue OoO |
| RISC | Alpha 21064A | 1993 | 330 | 2.85M | Clock speed |
| CISC* | Pentium | 1993 | 70 | 3.1M | Dual-issue |
| CISC | 68060 | 1994 | 55 | 2.5M | Final 68k |

*Intel began internal RISC translation with Pentium Pro (1995), blurring the line.

**Verdict:** RISC dominated on raw performance, but Intel's x86 volume economics and the Pentium Pro's RISC-inside approach signaled the coming CISC/RISC convergence.

---

## Gaming Processor Comparison

### Home Console CPUs (1985-1995)

| Console | CPU | Year | Clock (MHz) | Bits | MIPS | Genre Strength |
|---------|-----|------|-------------|------|------|----------------|
| NES | Ricoh 2A03 | 1983 | 1.79 | 8 | 0.59 | Platformers |
| Master System | Z80 | 1985 | 3.58 | 8 | 0.43 | Arcade ports |
| TurboGrafx-16 | HuC6280 | 1987 | 7.16 | 8 | 2.36 | Shooters, fast scroll |
| SNES | Ricoh 5A22 | 1990 | 3.58 | 16 | 1.07 | RPGs, Mode 7 |
| Genesis | MC68000 | 1988 | 7.67 | 16 | 1.07 | Action, blast proc |
| Neo Geo | MC68000 | 1990 | 12.0 | 16 | 1.68 | 2D fighting |
| PlayStation | R3000A | 1994 | 33.0 | 32 | 23.1 | 3D everything |
| Saturn | 2x SH-2 | 1994 | 28.6 | 32 | 44.8 | 2D king, 3D struggle |

```
Console CPU MIPS (Higher is Better)

Saturn (2xSH-2)   ████████████████████████████████████████████████████████████████████████████████████████████ 44.8
PlayStation (R3000A) █████████████████████████████████████████████████ 23.1
TurboGrafx (HuC6280) █████ 2.36
Neo Geo (68000)    ███ 1.68
SNES (5A22)        ██ 1.07
Genesis (68000)    ██ 1.07
NES (2A03)         █ 0.59
SMS (Z80)          █ 0.43
```

**Key Insight:** The jump from 16-bit to 32-bit consoles represented a 20-40x CPU performance leap -- the largest generational jump in console history. The Saturn's dual SH-2 design had more raw CPU power than the PlayStation, but its parallel architecture was notoriously difficult to program.

---

## Transistor Count Growth (1971-1995)

```
Transistor Count by Year (Millions, Log Scale Approximation)

                     0.001    0.01     0.1      1        10       (millions)
                       |        |        |        |        |
4004 (1971)       ===  0.002K
8080 (1974)       ====  0.005K
6502 (1975)       ====  0.004K
8086 (1978)       ======  0.029K
Z8000 (1979)      =====  0.018K
68000 (1979)      =======  0.068K
80286 (1982)      ==========  0.134K
68020 (1984)      ===========  0.190K
80386 (1985)      =============  0.275K
ARM2 (1986)       ======  0.030K
R2000 (1985)      ==========  0.110K
80486 (1989)      ═══════════════════  1.2M
68040 (1990)      ═══════════════════  1.2M
Alpha 21064 (1992)═════════════════════  1.68M
Pentium (1993)    ══════════════════════════  3.1M
PPC 604 (1994)    ═══════════════════════════  3.6M
R10000 (1996)     ══════════════════════════════════  6.7M
POWER2 (1993)     ═══════════════════════════════════════════════════════  23M
```

**Moore's Law in Action:** From the 4004's 2,300 transistors (1971) to the R10000's 6.7 million (1996), transistor counts increased nearly 3,000x in 25 years -- roughly doubling every 18-20 months as predicted.

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
| PPS-4 | Third commercial uP, calculator-focused |
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
| Berkeley RISC II | Refined register windows -> SPARC |
| Stanford MIPS | Interlocked pipeline -> commercial MIPS |
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
| uPD7720 | Early DSP for speech synthesis |
| Signetics 8X300 | Bipolar signal processor |
| Am2901 | Industry standard bit-slice |
| Am9511 | First arithmetic processing unit |
| 80486 | First x86 with integrated FPU + on-chip cache |
| Pentium | Superscalar x86, dual pipelines (U+V) |
| Alpha 21064 | Highest clock speed at launch, 64-bit |
| R4000 | First 64-bit MIPS, superpipelining (8 stages) |
| R10000 | Full out-of-order MIPS, register renaming |
| PowerPC 601 | Apple-IBM-Motorola alliance, POWER bridge |
| PowerPC 604 | First fully out-of-order PowerPC |
| UltraSPARC | VIS SIMD instructions for multimedia |
| ARM7TDMI | Thumb 16-bit mode, most-licensed ARM core |
| Hitachi SH-2 | Compact 16-bit instructions, Sega Saturn |
| 68060 | Final 68k, superscalar swan song |
| TMS320C80 | MVP: heterogeneous multiprocessor on one chip |

---

## Cost vs Performance (1985 Prices)

```
                    Price vs Performance (circa 1985)

    $500 |
         |                                    * 80386
    $400 |
         |
    $300 |                          * 68020
         |
    $200 |              * 80286
         |
    $100 |   * 68000
         | * 8086
     $50 |
         |
     $10 +-- * Z80  * 6502
         |
      $0 +----+----+----+----+----+----+----+----+
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

**Key Insight:** ARM1's power efficiency (30 MIPS/W) was **100x better** than the 8088, foreshadowing ARM's mobile dominance.

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

1. **RISC Revolution**: ARM and MIPS demonstrated dramatically better efficiency than CISC designs (10-30x better transistor efficiency). Berkeley RISC I/II and Stanford MIPS proved the concepts that led to SPARC and commercial MIPS.

2. **The 6502 Value**: At $25, the 6502 delivered exceptional IPC for its transistor count. Its variants powered the Apple II, Commodore 64, Atari 2600, and NES - the most influential platforms of the era.

3. **x86 Won by Compatibility**: Despite architectural compromises, x86's backward compatibility ensured its survival. The NEC V20/V30 showed even 15% faster compatible chips couldn't displace Intel.

4. **68000 vs 8086**: The 68000 was architecturally superior but lost the PC market; won in workstations (Sun, HP), gaming (Amiga, Atari ST, Genesis), and early Mac.

5. **iAPX 432 Disaster**: Object-oriented architecture sounded good but resulted in 10x worse performance than expected - a cautionary tale about premature complexity.

6. **Power Efficiency Matters**: ARM1's efficiency advantage in 1985 predicted its dominance in mobile computing 25 years later.

7. **Stack Machines Excel at Forth**: NC4016 and RTX2000 achieved remarkable IPC through hardware stack architecture, though limited to Forth applications.

8. **TMS9900's Memory-to-Memory Penalty**: Keeping registers in RAM seemed clever but resulted in CPI ~20, making it one of the slowest 16-bit processors despite a 3 MHz clock.

9. **Japanese Clones Proved Compatibility**: NEC uPD780 (Z80), Fujitsu MB8861 (6800), and others demonstrated that compatible clones could succeed, presaging the PC clone era.

10. **The DSP Parallel Path**: While general-purpose CPUs evolved toward RISC, DSPs like TMS320C10 and uPD7720 pioneered the specialized, parallel architectures that would eventually merge back into GPUs and AI accelerators.

11. **Superscalar Divergence (1993-1995)**: Out-of-order execution separated the performance leaders. The Alpha 21064A led on clock speed, the PPC 604 and R10000 pioneered full OoO, while Intel's Pentium won on volume economics despite simpler in-order dual-issue.

12. **The 32-Bit Console Revolution**: The PlayStation (R3000A) and Saturn (dual SH-2) represented a 20-40x CPU leap over 16-bit consoles -- the largest generational jump in gaming history.

13. **CISC/RISC Convergence**: By 1995, the distinction was blurring. Intel's Pentium Pro decoded x86 into micro-ops (internal RISC), while RISC chips grew more complex with OoO execution. The "RISC vs CISC" debate became moot as implementation details converged.

14. **Alpha: The Speed King**: DEC's Alpha 21064A (275 MHz, 1993) held the clock speed crown for years, demonstrating that aggressive process technology could compensate for simpler microarchitecture. Its legacy lived on in AMD's K7/K8 designs.

15. **PowerPC's Promise and Limits**: The Apple-IBM-Motorola alliance produced excellent chips (PPC 604 outperformed Pentium), but fragmented markets and Intel's manufacturing scale ultimately prevailed.

---

**Document Version:** 3.0
**Last Updated:** January 30, 2026
**Processors Covered:** 467
