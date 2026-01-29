# Microprocessor Evolution Timeline (1971-1985)

## The Dawn of the Microprocessor Era

This document traces the architectural evolution of microprocessors from the first commercial CPU through the emergence of 32-bit computing.

---

## Visual Timeline

```
1971 ──┬── Intel 4004 ─────────────────── THE FIRST MICROPROCESSOR
       │   (4-bit, 740 kHz, 2300 transistors)
       │
1972 ──┼── Intel 8008 ─────────────────── First 8-bit
       │   Rockwell PPS-4                  Third commercial µP!
       │   NEC µCOM-4
       │
1973 ──┼── National IMP-16 ────────────── Early 16-bit bit-slice
       │   SC/MP
       │
1974 ──┼── Intel 8080 ─────────────────── Industry takes off
       │   Intel 4040                      (Altair, CP/M)
       │   Motorola 6800
       │   TI TMS1000 (first mass MCU)
       │   NEC µPD751
       │   Intel 3002 (bit-slice)
       │   Intersil 6100
       │
1975 ──┼── MOS 6502 ───────────────────── The $25 revolution
       │   MOS 6507 (Atari 2600)           (Apple II, C64, NES)
       │   Fairchild F8
       │   Signetics 2650
       │   AMD 2901/2903 (bit-slice)
       │   MM6701 (bit-slice ALU)
       │   GI CP1600 (Intellivision)
       │   National PACE
       │   Panafacom MN1610
       │
1976 ──┼── Zilog Z80 ──────────────────── CP/M dominance
       │   NEC µPD780 (Z80 clone)          (TRS-80, MSX)
       │   Intel 8085
       │   Intel 8048/8039 (MCS-48)
       │   RCA 1802
       │   TI TMS9900
       │   TI SN74S481 (bit-slice)
       │   Signetics 8X300
       │   Ferranti F100-L
       │   Rockwell PPS-4/1
       │
1977 ──┼── Motorola 6802
       │   GI PIC1650 (first PIC)
       │   AMD Am9511 (first APU)
       │   Fujitsu MB8861 (6800 clone)
       │   Mostek 3870 (F8 single-chip)
       │   WD WD16 (LSI-11 compatible)
       │   Data General mN601 (microNova)
       │
1978 ──┼── Intel 8086 ─────────────────── x86 is born
       │   Motorola 6801
       │   Synertek SY6502A
       │   AMI S2811 (signal processor)
       │   Harris HM6100 (faster 6100)
       │
1979 ──┼── Intel 8088 ─────────────────── IBM PC chip selected
       │   Motorola 68000                  (Mac, Amiga, Atari ST)
       │   Motorola 6809
       │   Zilog Z8, Z8000
       │   Motorola 6805
       │   AMD Am9512 (floating point APU)
       │
1980 ──┼── Intel 8051 ─────────────────── MCU standard (still made!)
       │   RCA CDP1804
       │   Rockwell R6511 (6502+periph)
       │   MOS 6509 (CBM-II)
       │   NEC µPD7720 (speech DSP)
       │
1981 ──┼── Intel iAPX 432 ─────────────── Famous failure
       │   Sharp LH5801 (pocket CPU)
       │   TI TMS9995
       │
1982 ──┼── Intel 80286 ─────────────────── IBM AT processor
       │   Intel 80186/80188              Berkeley RISC I (first RISC!)
       │   Intel 8096 (automotive MCU)
       │   Motorola 68008, 68010
       │   Hitachi 6309 ("best 8-bit")
       │   NS NS32016, NS32081 (FPU)
       │   TI TMS320C10 (first TI DSP)
       │   WE WE32000
       │
1983 ──┼── WDC 65C02
       │   Rockwell R65C02
       │   Ricoh 2A03 (NES CPU)
       │   Hitachi HD6301
       │   Berkeley RISC II
       │   Stanford MIPS (academic)
       │   Novix NC4016 (Forth stack)
       │
1984 ──┼── Motorola 68020 ─────────────── True 32-bit 68k
       │   Motorola 68HC05               (Apple IIGS, SNES)
       │   WDC 65816
       │   NEC V20, V30
       │   NS NS32032
       │   RCA CDP1805
       │
1985 ──┴── Intel 80386 ─────────────────── 32-bit x86 arrives
           ARM1                            (RISC begins)
           MIPS R2000
           Zilog Z180
           Hitachi HD64180 (Z180 equiv)
           RCA CDP1806
           Harris RTX2000 (stack machine)
```

---

## Era 1: The Pioneers (1971-1974)

### The First Microprocessors

| Year | Processor | Bits | Transistors | Clock | Significance |
|------|-----------|------|-------------|-------|--------------|
| 1971 | Intel 4004 | 4 | 2,300 | 740 kHz | **THE FIRST** |
| 1972 | Intel 8008 | 8 | 3,500 | 500 kHz | First 8-bit |
| 1972 | Rockwell PPS-4 | 4 | 5,000 | 200 kHz | **THIRD** commercial µP |
| 1972 | NEC µCOM-4 | 4 | 2,500 | 1 MHz | Japanese 4-bit |
| 1974 | Intel 8080 | 8 | 4,500 | 2 MHz | Enabled Altair |
| 1974 | Motorola 6800 | 8 | 4,100 | 1 MHz | Motorola enters |
| 1974 | Intel 4040 | 4 | 3,000 | 740 kHz | 4004 + interrupts |
| 1974 | TI TMS1000 | 4 | 8,000 | 400 kHz | First mass MCU |
| 1974 | Intersil 6100 | 12 | 4,000 | 4 MHz | PDP-8 on chip! |

### Key Architectural Features
- **4004**: Harvard architecture, 4-bit ALU, 46 instructions
- **8008**: 8-bit, but still slow and limited
- **PPS-4**: Calculator-focused, parallel 4-bit bus
- **8080**: Full 8-bit, 78 instructions, usable for real computing
- **6800**: Clean dual-accumulator design
- **6100**: Minicomputer ISA (PDP-8) in microprocessor form

---

## Era 2: The 8-Bit Revolution (1975-1978)

### The Explosion of Choice

| Year | Processor | Transistors | Clock | Key Innovation |
|------|-----------|-------------|-------|----------------|
| 1975 | MOS 6502 | 3,510 | 1 MHz | **$25 price point** |
| 1975 | MOS 6507 | 3,510 | 1 MHz | 6502 in 28-pin (Atari 2600) |
| 1975 | Fairchild F8 | 5,000 | 2 MHz | Multi-chip architecture |
| 1975 | Signetics 2650 | 6,000 | 1 MHz | Unique addressing modes |
| 1975 | GI CP1600 | 10,000 | 1 MHz | Intellivision CPU |
| 1976 | Zilog Z80 | 8,500 | 2.5 MHz | 8080 compatible + extensions |
| 1976 | NEC µPD780 | 8,500 | 2.5 MHz | Z80 clone |
| 1976 | Intel 8085 | 6,500 | 3 MHz | Single +5V supply |
| 1976 | Intel 8048/8039 | 4,500 | 6 MHz | First widely-used MCU |
| 1976 | RCA 1802 | 5,000 | 2 MHz | Radiation-hard CMOS |
| 1976 | TI TMS9900 | 8,000 | 3 MHz | Workspace registers |
| 1977 | Mostek 3870 | 5,500 | 4 MHz | F8 single-chip |
| 1977 | Fujitsu MB8861 | 4,100 | 1 MHz | 6800 clone |

### Platform Wars Begin

```
┌─────────────────────────────────────────────────────────────────┐
│                    1977: THREE PLATFORMS                        │
├─────────────────────┬─────────────────────┬─────────────────────┤
│     Apple II        │    TRS-80           │   Commodore PET     │
│     (6502)          │    (Z80)            │   (6502)            │
│                     │                     │                     │
│   Open bus          │   Integrated        │   Business focus    │
│   Color graphics    │   CP/M capable      │   Built-in monitor  │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

### MCU Revolution
- **Intel 8048/8039** (1976): First widely-used MCU family
- **TI TMS1000** (1974): Billions shipped in calculators
- **PIC1650** (1977): Birth of PIC family
- **Mostek 3870** (1977): F8 in single-chip form

### Bit-Slice Era
- **AMD 2901/2903** (1975): Build-your-own CPU
- **Intel 3002** (1974): Intel's bit-slice entry
- **TI SN74S481** (1976): High-speed ALU slice
- **MM6701** (1975): Monolithic bit-slice ALU

---

## Era 3: 16-Bit Emergence (1978-1982)

### The 16-Bit Transition

| Year | Processor | Transistors | Clock | Address Space | Notes |
|------|-----------|-------------|-------|---------------|-------|
| 1973 | National IMP-16 | - | 750 kHz | 64 KB | Early bit-slice 16-bit |
| 1975 | National PACE | 10,000 | 2 MHz | 64 KB | p-channel MOS 16-bit |
| 1975 | Panafacom MN1610 | 12,000 | 2 MHz | 64 KB | Japanese 16-bit pioneer |
| 1976 | Ferranti F100-L | 8,000 | 1 MHz | 32 KB | British military |
| 1977 | WD WD16 | 10,000 | 4 MHz | 64 KB | LSI-11 compatible |
| 1977 | DG mN601 | 7,000 | 3 MHz | 64 KB | microNova |
| 1978 | Intel 8086 | 29,000 | 5 MHz | 1 MB | x86 origin |
| 1979 | Intel 8088 | 29,000 | 5 MHz | 1 MB (8-bit bus) | IBM PC |
| 1979 | Motorola 68000 | 68,000 | 8 MHz | 16 MB | Mac/Amiga/Atari |
| 1979 | Zilog Z8000 | 17,500 | 4 MHz | 8 MB | Zilog 16-bit |
| 1982 | Intel 80286 | 134,000 | 6 MHz | 16 MB virtual | Protected mode |
| 1982 | Intel 8096 | 55,000 | 12 MHz | 64 KB | Automotive MCU |
| 1984 | WDC 65816 | 22,000 | 2.8 MHz | 16 MB | SNES, Apple IIGS |
| 1984 | NEC V20/V30 | 63,000 | 8-10 MHz | 1 MB | Faster 808x |

### The IBM PC Decision (1981)

```
IBM's Choice:

Option A: Intel 8086        Option B: Intel 8088 ← CHOSEN
┌─────────────────────┐     ┌─────────────────────┐
│ 16-bit bus          │     │ 8-bit bus           │
│ Faster              │     │ Cheaper components  │
│ More expensive      │     │ Existing PC boards  │
└─────────────────────┘     └─────────────────────┘

This decision shaped the next 40+ years of computing.
```

### The 68000: A Different Philosophy

```
Intel 8086:                     Motorola 68000:
┌─────────────────────┐         ┌─────────────────────┐
│ Segmented memory    │         │ Linear 16 MB space  │
│ 4 segment registers │         │ 32-bit registers    │
│ Complex addressing  │         │ Clean orthogonal    │
│ 8080 mindset        │         │ Mini-computer feel  │
└─────────────────────┘         └─────────────────────┘

68000 won in workstations: Mac, Amiga, Atari ST, Sun
8086 won in PCs: IBM PC and clones
```

---

## Era 4: 32-Bit and RISC Dawn (1982-1985)

### The 32-Bit Pioneers

| Year | Processor | Transistors | Clock | Architecture |
|------|-----------|-------------|-------|--------------|
| 1981 | iAPX 432 | 250,000 | 5 MHz | Object-oriented (failed) |
| 1982 | NS32016 | 60,000 | 10 MHz | Traditional CISC |
| 1982 | WE32000 | 125,000 | 14 MHz | Unix workstations |
| 1984 | NS32032 | 70,000 | 10 MHz | Improved NS32016 |
| 1984 | MC68020 | 190,000 | 16 MHz | Full 32-bit 68k |
| 1985 | Intel 80386 | 275,000 | 16 MHz | 32-bit x86 |

### The RISC Revolution Begins

| Year | Processor | Transistors | Clock | Philosophy |
|------|-----------|-------------|-------|------------|
| 1982 | Berkeley RISC I | 44,000 | 1 MHz | First RISC (academic) |
| 1983 | Berkeley RISC II | 41,000 | 3 MHz | Register windows refined |
| 1983 | Stanford MIPS | 25,000 | 2 MHz | Original interlocked pipeline |
| 1985 | ARM1 | 25,000 | 6 MHz | Simple is faster |
| 1985 | MIPS R2000 | 110,000 | 8 MHz | Pipeline everything |
| 1987 | SPARC | 100,000 | 16 MHz | RISC I/II heritage |

```
CISC (Complex):                 RISC (Reduced):
┌─────────────────────┐         ┌─────────────────────┐
│ Many instructions   │         │ Few instructions    │
│ Variable length     │         │ Fixed length        │
│ Memory-to-memory    │         │ Load/store only     │
│ Microcode           │         │ Hardwired           │
│ Slower clock        │         │ Faster clock        │
└─────────────────────┘         └─────────────────────┘

ARM1: Only 25,000 transistors, outperformed 80286!
Berkeley RISC II: Register windows influenced SPARC
Stanford MIPS: Led directly to MIPS R2000
```

### Specialized Processors

#### Stack Machines (Forth)
| Year | Processor | Clock | Notes |
|------|-----------|-------|-------|
| 1983 | Novix NC4016 | 8 MHz | Native Forth execution |
| 1985 | Harris RTX2000 | 10 MHz | Improved NC4016 |

#### DSPs (Digital Signal Processors)
| Year | Processor | Clock | Application |
|------|-----------|-------|-------------|
| 1978 | AMI S2811 | 8 MHz | Early signal processor |
| 1980 | NEC µPD7720 | 8 MHz | Speech synthesis |
| 1982 | TI TMS320C10 | 20 MHz | First commercial TI DSP |

#### Math Coprocessors
| Year | Processor | Notes |
|------|-----------|-------|
| 1977 | AMD Am9511 | First arithmetic processor |
| 1979 | AMD Am9512 | Floating-point APU |
| 1982 | NS32081 | NS32000 family FPU |
| 1980 | Intel 80287 | x86 coprocessor |
| 1985 | Intel 80387 | 80386 coprocessor |

---

## Transistor Count Evolution

```
Transistors (log scale)

1,000,000 ┤                                              ● 80386
          │                                         ● iAPX 432
          │                                    ● 68020
  100,000 ┤                               ● 80286
          │                          ● 68000
          │                     ● R2000
   10,000 ┤                ● Z80
          │           ● 8080
          │      ● 8008
    1,000 ┤ ● 4004
          └──┬────┬────┬────┬────┬────┬────┬────┬────┬
            71   73   75   77   79   81   83   85

Moore's Law in action: ~2× every 18-24 months
```

---

## Clock Speed Evolution

```
Clock Speed (MHz)

20 ┤                                              ● 68020
   │                                         ● 80386
15 ┤                                    
   │                               ● 80286
10 ┤                          ● NS32016
   │                     ● 68000
 5 ┤                ● 8086
   │           ● Z80
   │      ● 8080
 1 ┤ ● 4004
   └──┬────┬────┬────┬────┬────┬────┬────┬────┬
     71   73   75   77   79   81   83   85
```

---

## Key Architectural Innovations

### 1971-1975: Foundations
- **Harvard architecture** (4004)
- **Accumulator-based** (8080, 6800)
- **Zero-page addressing** (6502)

### 1976-1979: Refinements
- **Index registers** (Z80 extensions)
- **Dual accumulators** (6809)
- **Workspace registers** (TMS9900)
- **16 general registers** (68000)

### 1980-1985: Sophisttic
- **Memory management** (80286, 68010)
- **Virtual memory** (80386, 68020)
- **Caches** (80386)
- **Pipelining** (ARM1, R2000)

---

## The Survivors

Processors from this era still in production or active use (2026):

| Processor | Status | Where Used |
|-----------|--------|------------|
| 8051 | **Still manufactured** | Embedded everywhere |
| Z80 | **Still manufactured** | Embedded, calculators |
| 6502 (WDC) | **Still manufactured** | Embedded, hobbyist |
| 68000 | Derivatives active | Automotive, industrial |
| ARM | **Dominant mobile** | 200+ billion shipped |
| COSMAC 1802 | Rad-hard versions | Space missions |

---

## Lessons from the Era

1. **Price matters**: The $25 6502 enabled the personal computer revolution
2. **Compatibility wins**: x86 backward compatibility ensured its survival
3. **Ecosystem beats architecture**: 8051's tools won over better MCUs
4. **Simplicity can win**: ARM1's simple design outperformed complex chips
5. **Timing is everything**: iAPX 432 was too ambitious too soon

---

**Document Version:** 2.0
**Last Updated:** January 29, 2026
**Processors Covered:** 117
