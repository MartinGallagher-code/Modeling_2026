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
| TMS1000 | 1974 | 0.40 | 8,000 | 0.04 | 0.016 | <0.5W | First mass MCU |

### 8-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| Intel 8008 | 1972 | 0.50 | 3,500 | 0.04 | 0.020 | 16 KB | First 8-bit |
| Intel 8080 | 1974 | 2.00 | 4,500 | 0.10 | 0.200 | 64 KB | Industry standard |
| Intel 8085 | 1976 | 3.00 | 6,500 | 0.11 | 0.330 | 64 KB | Single +5V |
| MOS 6502 | 1975 | 1.00 | 3,510 | 0.10 | 0.100 | 64 KB | $25 revolution |
| Zilog Z80 | 1976 | 2.50 | 8,500 | 0.12 | 0.300 | 64 KB | CP/M standard |
| Motorola 6800 | 1974 | 1.00 | 4,100 | 0.10 | 0.100 | 64 KB | First Motorola |
| Motorola 6809 | 1979 | 1.00 | 9,000 | 0.14 | 0.140 | 64 KB | Best 8-bit arch |
| Hitachi 6309 | 1982 | 2.00 | 10,000 | 0.18 | 0.360 | 64 KB | Best 8-bit ever |
| RCA 1802 | 1976 | 2.00 | 5,000 | 0.05 | 0.100 | 64 KB | Rad-hard, space |
| Fairchild F8 | 1975 | 2.00 | 5,000 | 0.08 | 0.160 | 64 KB | Two-chip design |

### 8-Bit MCUs

| Processor | Year | Clock (MHz) | ROM | RAM | IPC | Notes |
|-----------|------|-------------|-----|-----|-----|-------|
| Intel 8048 | 1976 | 6.00 | 1 KB | 64 B | 0.08 | MCS-48 flagship |
| Intel 8051 | 1980 | 12.0 | 4 KB | 128 B | 0.09 | Still manufactured! |
| Intel 8096 | 1982 | 12.0 | 8 KB | 232 B | 0.12 | Automotive standard |
| Motorola 6805 | 1979 | 4.00 | 1 KB | 64 B | 0.08 | Low-cost MCU |
| TI TMS7000 | 1981 | 10.0 | 4 KB | 128 B | 0.09 | Register file arch |
| GI PIC1650 | 1977 | 4.00 | 0.5KB | 32 B | 0.06 | First PIC |
| Zilog Z8 | 1979 | 8.00 | 2 KB | 144 B | 0.09 | Zilog MCU |

### 16-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| Intel 8086 | 1978 | 5.00 | 29,000 | 0.12 | 0.60 | 1 MB | x86 origin |
| Intel 8088 | 1979 | 5.00 | 29,000 | 0.10 | 0.50 | 1 MB | IBM PC |
| Intel 80186 | 1982 | 8.00 | 55,000 | 0.12 | 0.96 | 1 MB | Integrated |
| Intel 80286 | 1982 | 6.00 | 134,000 | 0.15 | 0.90 | 16 MB | Protected mode |
| Motorola 68000 | 1979 | 8.00 | 68,000 | 0.14 | 1.12 | 16 MB | Mac/Amiga/Atari |
| Motorola 68010 | 1982 | 10.0 | 84,000 | 0.14 | 1.40 | 16 MB | Virtual memory |
| Zilog Z8000 | 1979 | 4.00 | 17,500 | 0.11 | 0.44 | 8 MB | Zilog 16-bit |
| TI TMS9900 | 1976 | 3.00 | 8,000 | 0.08 | 0.24 | 64 KB | Workspace arch |
| NEC V20 | 1984 | 8.00 | 63,000 | 0.12 | 0.96 | 1 MB | Faster 8088 |
| NEC V30 | 1984 | 10.0 | 63,000 | 0.14 | 1.40 | 1 MB | Faster 8086 |
| WDC 65816 | 1984 | 2.80 | 22,000 | 0.12 | 0.34 | 16 MB | SNES, Apple IIGS |

### 32-Bit Processors

| Processor | Year | Clock (MHz) | Transistors | IPC | MIPS | Addr Space | Notes |
|-----------|------|-------------|-------------|-----|------|------------|-------|
| Intel 80386 | 1985 | 16.0 | 275,000 | 0.20 | 3.20 | 4 GB | First 32-bit x86 |
| Intel iAPX 432 | 1981 | 5.00 | 250,000 | 0.05 | 0.25 | 16 MB | Famous failure |
| Motorola 68020 | 1984 | 16.0 | 190,000 | 0.22 | 3.52 | 4 GB | Full 32-bit 68k |
| NS NS32016 | 1982 | 10.0 | 60,000 | 0.10 | 1.00 | 16 MB | Early 32-bit |
| NS NS32032 | 1984 | 10.0 | 70,000 | 0.12 | 1.20 | 4 GB | Improved NS |
| Berkeley RISC I | 1982 | 1.00 | 44,000 | 0.58 | 0.58 | 32-bit | First RISC (academic) |
| ARM1 | 1985 | 6.00 | 25,000 | 0.50 | 3.00 | 26-bit | RISC pioneer |
| MIPS R2000 | 1985 | 8.00 | 110,000 | 0.60 | 4.80 | 4 GB | RISC pioneer |

---

## Performance Rankings

### By Raw MIPS (Higher is Better)

```
MIPS Performance (1985)

MIPS R2000      ████████████████████████████████████████████████ 4.80
Motorola 68020  ███████████████████████████████████ 3.52
Intel 80386     ████████████████████████████████ 3.20
ARM1            ██████████████████████████████ 3.00
NEC V30         ██████████████ 1.40
Motorola 68010  ██████████████ 1.40
NS32032         ████████████ 1.20
Motorola 68000  ███████████ 1.12
NS32016         ██████████ 1.00
NEC V20         █████████ 0.96
Intel 80186     █████████ 0.96
Intel 80286     █████████ 0.90
Intel 8086      ██████ 0.60
Intel 8088      █████ 0.50
Z8000           ████ 0.44
65816           ███ 0.34
Z80             ███ 0.30
8085            ███ 0.33
TMS9900         ██ 0.24
8080            ██ 0.20
6809            █ 0.14
6502            █ 0.10
```

### By IPC Efficiency (Higher is Better)

```
IPC (Instructions Per Cycle)

MIPS R2000      ████████████████████████████████████████████████████████████ 0.60
ARM1            ██████████████████████████████████████████████████ 0.50
Motorola 68020  ██████████████████████ 0.22
Intel 80386     ████████████████████ 0.20
Hitachi 6309    ██████████████████ 0.18
Intel 80286     ███████████████ 0.15
NEC V30         ██████████████ 0.14
Motorola 68000  ██████████████ 0.14
Motorola 6809   ██████████████ 0.14
NEC V20         ████████████ 0.12
Intel 8086      ████████████ 0.12
Intel 80186     ████████████ 0.12
65816           ████████████ 0.12
Z80             ████████████ 0.12
8085            ███████████ 0.11
Intel 8080      ██████████ 0.10
6502            ██████████ 0.10
8051            █████████ 0.09
8088            ██████████ 0.10
iAPX 432        █████ 0.05 ← OOP overhead!
```

### By Transistor Efficiency (MIPS per 1000 Transistors)

```
MIPS per 1000 Transistors (Higher = More Efficient Design)

ARM1            ████████████████████████████████████████████████████████████ 0.120
6502            ████████████████████████████████████████████████ 0.028
Z80             ███████████████████████████████████████████ 0.035
8080            ███████████████████████████████████████████ 0.044
MIPS R2000      ████████████████████████████████████████████ 0.044
6809            ███████████████ 0.016
Motorola 68000  ████████████████ 0.016
Intel 8086      ████████████████████ 0.021
Intel 80386     ████████████ 0.012
Motorola 68020  ██████████████████ 0.019
Intel 80286     ███████ 0.007
iAPX 432        █ 0.001 ← Bloated!
```

**Key Insight:** ARM1's RISC architecture delivered **10× the transistor efficiency** of contemporary CISC designs!

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
| 8008 | First 8-bit |
| 8080 | Practical computing |
| 6502 | $25 price point, zero-page |
| Z80 | 8080 superset, index registers |
| 6809 | Position-independent code, best 8-bit ISA |
| 8086 | Segmented memory, x86 foundation |
| 68000 | 32-bit registers, orthogonal ISA |
| 80286 | Protected mode, privilege levels |
| 80386 | Paging, 32-bit x86 |
| RISC I | Register windows, first RISC |
| ARM1 | RISC simplicity, load/store |
| R2000 | 5-stage pipeline, delay slots |
| 1802 | Radiation hardness |
| 8051 | Integrated peripherals, bit addressing |
| 8096 | HSI/HSO for real-time control |
| TMS320C10 | First successful commercial DSP |

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

1. **RISC Revolution**: ARM1 and MIPS R2000 demonstrated dramatically better efficiency than CISC designs (10-30× better transistor efficiency)

2. **The 6502 Value**: At $25, the 6502 delivered similar IPC to the $150 8080, enabling the personal computer revolution

3. **x86 Won by Compatibility**: Despite architectural compromises, x86's backward compatibility ensured its survival

4. **68000 vs 8086**: The 68000 was architecturally superior but lost the PC market; won in workstations and gaming

5. **iAPX 432 Disaster**: Object-oriented architecture sounded good but resulted in 10× worse performance than expected

6. **Power Efficiency Matters**: ARM1's efficiency advantage in 1985 predicted its dominance in mobile computing 25 years later

---

**Document Version:** 1.1
**Last Updated:** January 29, 2026
**Processors Covered:** 80
