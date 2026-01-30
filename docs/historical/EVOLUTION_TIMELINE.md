# Microprocessor Evolution Timeline (1970-1995)

## The Foundational Era of Computing

This document traces the architectural evolution of microprocessors from the first commercial CPU through the rise of superscalar, 64-bit, and consumer-driven designs -- the complete foundational era that shaped all modern computing.

---

## Visual Timeline

```
1971 ──┬── Intel 4004 ─────────────────── THE FIRST MICROPROCESSOR
       │   (4-bit, 740 kHz, 2300 transistors)
       │
1972 ──┼── Intel 8008 ─────────────────── First 8-bit
       │   Rockwell PPS-4                  Third commercial uP!
       │   NEC uCOM-4
       │
1973 ──┼── National IMP-16 ────────────── Early 16-bit bit-slice
       │   SC/MP
       │
1974 ──┼── Intel 8080 ─────────────────── Industry takes off
       │   Intel 4040                      (Altair, CP/M)
       │   Motorola 6800
       │   TI TMS1000 (first mass MCU)
       │   NEC uPD751
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
       │   NEC uPD780 (Z80 clone)          (TRS-80, MSX)
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
       │   NEC uPD7720 (speech DSP)
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
1985 ──┼── Intel 80386 ─────────────────── 32-bit x86 arrives
       │   ARM1                            (RISC begins)
       │   MIPS R2000
       │   Zilog Z180
       │   Hitachi HD64180 (Z180 equiv)
       │   RCA CDP1806
       │   Harris RTX2000 (stack machine)
       │
1986 ──┼── Motorola 68030              TI TMS34010 (first programmable GPU!)
       │   NEC V60 (Japan's first 32-bit)
       │   MIPS R2000 (commercial)
       │   HP PA-RISC
       │   Motorola DSP56001
       │   ARM2 (first production ARM)
       │
1987 ──┼── Sun SPARC ──────────────────── RISC workstations arrive
       │   INMOS T800 (transputer+FPU)
       │   HuC6280 (TurboGrafx-16)
       │   AMD Am29000
       │   Fujitsu MB86900 (SPARC)
       │
1988 ──┼── MIPS R3000 ─────────────────── SGI workstations
       │   Intel i960 (RISC)
       │   Motorola 88100
       │   Yamaha YM2612 (Genesis)
       │
1989 ──┼── Intel 80486 ────────────────── Pipelined + on-chip FPU & cache
       │   ARM3 (cached)
       │   Tseng ET4000
       │   Ensoniq OTTO
       │   INMOS T414
       │
1990 ──┼── Motorola 68040 ─────────────── On-chip FPU
       │   IBM POWER1
       │   ARM250
       │   Ricoh 5A22 (SNES)
       │   SNK LSPC2
       │
1991 ──┼── MIPS R4000 ─────────────────── 64-bit RISC
       │   ARM6 (32-bit address)
       │   S3 86C911 (Windows accelerator)
       │   SuperSPARC
       │   AMD Am386
       │
1992 ──┼── DEC Alpha 21064 ────────────── Fastest of its era
       │   Hitachi SH-1
       │   MicroSPARC
       │   ATI Mach32
       │   Weitek P9000
       │   Cyrix Cx486DLC
       │   HP PA-7100
       │
1993 ──┼── Intel Pentium ──────────────── First superscalar x86
       │   PowerPC 601 (AIM alliance)
       │   MIPS R4400
       │   ARM610 (cached)
       │   IBM POWER2
       │   HyperSPARC
       │   AMD Am486
       │
1994 ──┼── Motorola 68060 ─────────────── Last 68k, superscalar
       │   ARM7TDMI (most licensed ARM ever)
       │   MIPS R4600, R8000
       │   Sony R3000A (PlayStation!)
       │   Hitachi SH-2 (Saturn/32X)
       │   PowerPC 603, 604
       │   Motorola ColdFire
       │   NexGen Nx586
       │   Cyrix Cx5x86
       │   ATI Mach64
       │   Alpha 21064A
       │   NEC V810 (Virtual Boy)
       │   Toshiba TX39
       │
1995 ──┴── MIPS R10000 ────────────────── Out-of-order RISC
           UltraSPARC I
           AMD Am5x86
           PowerPC 620
           Alpha 21066
           HP PA-7200
```

---

## Era 1: The Pioneers (1971-1974)

### The First Microprocessors

| Year | Processor | Bits | Transistors | Clock | Significance |
|------|-----------|------|-------------|-------|--------------|
| 1971 | Intel 4004 | 4 | 2,300 | 740 kHz | **THE FIRST** |
| 1972 | Intel 8008 | 8 | 3,500 | 500 kHz | First 8-bit |
| 1972 | Rockwell PPS-4 | 4 | 5,000 | 200 kHz | **THIRD** commercial uP |
| 1972 | NEC uCOM-4 | 4 | 2,500 | 1 MHz | Japanese 4-bit |
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
| 1976 | NEC uPD780 | 8,500 | 2.5 MHz | Z80 clone |
| 1976 | Intel 8085 | 6,500 | 3 MHz | Single +5V supply |
| 1976 | Intel 8048/8039 | 4,500 | 6 MHz | First widely-used MCU |
| 1976 | RCA 1802 | 5,000 | 2 MHz | Radiation-hard CMOS |
| 1976 | TI TMS9900 | 8,000 | 3 MHz | Workspace registers |
| 1977 | Mostek 3870 | 5,500 | 4 MHz | F8 single-chip |
| 1977 | Fujitsu MB8861 | 4,100 | 1 MHz | 6800 clone |

### Platform Wars Begin

```
+---------------------------------------------------------------------+
|                    1977: THREE PLATFORMS                              |
+---------------------+---------------------+-------------------------+
|     Apple II        |    TRS-80           |   Commodore PET         |
|     (6502)          |    (Z80)            |   (6502)                |
|                     |                     |                         |
|   Open bus          |   Integrated        |   Business focus        |
|   Color graphics    |   CP/M capable      |   Built-in monitor      |
+---------------------+---------------------+-------------------------+
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

Option A: Intel 8086        Option B: Intel 8088 <-- CHOSEN
+---------------------+     +---------------------+
| 16-bit bus          |     | 8-bit bus           |
| Faster              |     | Cheaper components  |
| More expensive      |     | Existing PC boards  |
+---------------------+     +---------------------+

This decision shaped the next 40+ years of computing.
```

### The 68000: A Different Philosophy

```
Intel 8086:                     Motorola 68000:
+---------------------+         +---------------------+
| Segmented memory    |         | Linear 16 MB space  |
| 4 segment registers |         | 32-bit registers    |
| Complex addressing  |         | Clean orthogonal    |
| 8080 mindset        |         | Mini-computer feel  |
+---------------------+         +---------------------+

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
+---------------------+         +---------------------+
| Many instructions   |         | Few instructions    |
| Variable length     |         | Fixed length        |
| Memory-to-memory    |         | Load/store only     |
| Microcode           |         | Hardwired           |
| Slower clock        |         | Faster clock        |
+---------------------+         +---------------------+

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
| 1980 | NEC uPD7720 | 8 MHz | Speech synthesis |
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

## Era 5: The RISC Wars (1986-1991)

### Workstation Architectures Compete

The late 1980s saw an unprecedented battle between RISC architectures, each backed by major companies seeking to dominate the lucrative workstation and server markets. MIPS powered SGI, SPARC powered Sun, PA-RISC powered HP, and IBM developed POWER -- all pursuing the same insight that simpler instructions could execute faster.

Meanwhile, ARM evolved from a BBC Micro experiment into a production processor family, while Intel pushed x86 forward with pipelining and on-chip caches.

| Year | Processor | Transistors | Clock | IPC | Est. MIPS | Architecture |
|------|-----------|-------------|-------|-----|-----------|--------------|
| 1986 | ARM2 | 25,000 | 8 MHz | 0.56 | 4.5 | ARM (first production) |
| 1986 | MIPS R2000 | 110,000 | 15 MHz | 0.8 | 12 | MIPS I |
| 1986 | HP PA-7000 | 115,000 | 20 MHz | 0.6 | 12 | PA-RISC 1.0 |
| 1986 | Motorola 68030 | 273,000 | 16 MHz | 0.5 | 8 | 68k + MMU on-chip |
| 1986 | NEC V60 | 375,000 | 16 MHz | 0.4 | 6.5 | Japan's first 32-bit |
| 1986 | Motorola DSP56001 | 450,000 | 20 MHz | - | - | Audio/telecom DSP |
| 1986 | TI TMS34010 | 200,000 | 50 MHz | - | - | First programmable GPU |
| 1987 | Sun SPARC | 100,000 | 16 MHz | 0.7 | 11 | Berkeley RISC heritage |
| 1987 | INMOS T800 | 250,000 | 25 MHz | 0.6 | 15 | Transputer + FPU |
| 1987 | AMD Am29000 | 180,000 | 25 MHz | 0.8 | 20 | Branch-target cache |
| 1987 | Fujitsu MB86900 | 100,000 | 16 MHz | 0.7 | 11 | SPARC implementation |
| 1988 | MIPS R3000 | 120,000 | 33 MHz | 0.8 | 26 | MIPS II, SGI Indigo |
| 1988 | Intel i960 | 600,000 | 33 MHz | 0.7 | 23 | Intel RISC (embedded) |
| 1988 | Motorola 88100 | 165,000 | 20 MHz | 0.7 | 14 | Motorola RISC attempt |
| 1989 | Intel 80486 | 1,200,000 | 25 MHz | 0.7 | 18 | Pipelined x86 + FPU |
| 1989 | ARM3 | 310,000 | 25 MHz | 0.55 | 14 | First cached ARM |
| 1990 | Motorola 68040 | 1,200,000 | 25 MHz | 0.6 | 15 | 68k + on-chip FPU |
| 1990 | IBM POWER1 | 800,000 | 25 MHz | 1.2 | 30 | Multi-chip RISC, RS/6000 |
| 1991 | MIPS R4000 | 1,350,000 | 100 MHz | 0.6 | 60 | First 64-bit MIPS |
| 1991 | SuperSPARC | 3,100,000 | 40 MHz | 0.9 | 36 | Superscalar SPARC |
| 1991 | ARM6 | 35,000 | 33 MHz | 0.55 | 18 | 32-bit address space |
| 1991 | AMD Am386 | 275,000 | 40 MHz | 0.35 | 14 | x86 clone arrives |

### ARM: From Experiment to Production

```
ARM Evolution (1985-1991):

ARM1 (1985)    ARM2 (1986)     ARM3 (1989)     ARM6 (1991)
25K trans      25K trans       310K trans       35K trans
6 MHz          8 MHz           25 MHz           33 MHz
No cache       No cache        4 KB cache       Optional cache
Prototype!     Acorn Archimedes  Production      32-bit addressing

Key Insight: ARM used fewer transistors than ANY competitor,
yet delivered competitive performance through elegant design.
```

### The RISC Workstation Landscape

```
+------------------+------------------+------------------+------------------+
|   SGI (MIPS)     |   Sun (SPARC)    |   HP (PA-RISC)   |   IBM (POWER)    |
+------------------+------------------+------------------+------------------+
| R2000 -> R3000   | SPARC -> Super   | PA-7000          | POWER1           |
| 3D Graphics      | Networking       | Engineering      | Scientific       |
| Hollywood VFX    | Internet servers | CAD/CAE          | Supercomputing   |
| IRIX             | SunOS/Solaris    | HP-UX            | AIX              |
+------------------+------------------+------------------+------------------+

Every major Unix vendor had its own RISC architecture.
This fragmentation ultimately helped x86 win the volume game.
```

---

## Era 6: Superscalar and 64-Bit (1992-1995)

### The Performance Explosion

The early 1990s brought superscalar execution (multiple instructions per clock), 64-bit addressing, and out-of-order execution. Clock speeds jumped from tens of MHz to hundreds. DEC's Alpha was the raw speed champion, Intel's Pentium brought superscalar to the masses, and the AIM alliance (Apple-IBM-Motorola) created PowerPC to challenge x86 dominance.

| Year | Processor | Transistors | Clock | IPC | Est. MIPS | Architecture |
|------|-----------|-------------|-------|-----|-----------|--------------|
| 1992 | DEC Alpha 21064 | 1,680,000 | 150 MHz | 1.2 | 180 | 64-bit, fastest of era |
| 1992 | HP PA-7100 | 850,000 | 100 MHz | 0.9 | 90 | Superscalar PA-RISC |
| 1992 | MicroSPARC | 800,000 | 50 MHz | 0.6 | 30 | Low-cost SPARC |
| 1992 | Hitachi SH-1 | 400,000 | 20 MHz | 0.7 | 14 | Compact RISC |
| 1992 | Cyrix Cx486DLC | 600,000 | 33 MHz | 0.5 | 17 | x86 clone in 386 socket |
| 1993 | Intel Pentium | 3,100,000 | 60 MHz | 1.1 | 66 | First superscalar x86 |
| 1993 | PowerPC 601 | 2,800,000 | 66 MHz | 1.2 | 80 | AIM alliance |
| 1993 | MIPS R4400 | 2,300,000 | 150 MHz | 0.7 | 105 | 64-bit, improved R4000 |
| 1993 | ARM610 | 70,000 | 33 MHz | 0.55 | 18 | Cached ARM for Newton |
| 1993 | IBM POWER2 | 23,000,000 | 71 MHz | 2.0 | 142 | Multi-chip monster |
| 1993 | HyperSPARC | 1,800,000 | 100 MHz | 0.8 | 80 | Ross Technology SPARC |
| 1993 | AMD Am486 | 1,200,000 | 40 MHz | 0.6 | 24 | x86 clone, late but cheap |
| 1994 | Motorola 68060 | 2,500,000 | 50 MHz | 1.1 | 55 | Last 68k, superscalar |
| 1994 | ARM7TDMI | 75,000 | 40 MHz | 0.55 | 22 | Most licensed ARM ever |
| 1994 | MIPS R4600 | 1,900,000 | 100 MHz | 0.7 | 70 | Low-cost 64-bit |
| 1994 | MIPS R8000 | 3,000,000 | 75 MHz | 1.5 | 112 | Superscalar, FP monster |
| 1994 | Sony R3000A | 120,000 | 33 MHz | 0.8 | 26 | PlayStation CPU |
| 1994 | Hitachi SH-2 | 500,000 | 28 MHz | 0.8 | 22 | Saturn / 32X |
| 1994 | PowerPC 603 | 1,600,000 | 80 MHz | 1.0 | 80 | Low-power PPC |
| 1994 | PowerPC 604 | 3,600,000 | 100 MHz | 1.3 | 130 | High-perf PPC |
| 1994 | NexGen Nx586 | 3,500,000 | 93 MHz | 0.9 | 84 | x86 via RISC core |
| 1994 | Cyrix Cx5x86 | 2,000,000 | 100 MHz | 0.7 | 70 | Superscalar x86 clone |
| 1994 | Alpha 21064A | 2,850,000 | 300 MHz | 1.2 | 360 | Fastest chip, period |
| 1994 | NEC V810 | 380,000 | 20 MHz | 0.6 | 12 | Virtual Boy CPU |
| 1994 | Toshiba TX39 | 350,000 | 33 MHz | 0.7 | 23 | MIPS embedded |
| 1994 | Motorola ColdFire | 800,000 | 16 MHz | 0.6 | 10 | 68k replacement MCU |
| 1995 | MIPS R10000 | 6,700,000 | 200 MHz | 1.8 | 360 | Out-of-order RISC |
| 1995 | UltraSPARC I | 5,200,000 | 167 MHz | 1.3 | 217 | 64-bit SPARC |
| 1995 | AMD Am5x86 | 1,600,000 | 133 MHz | 0.6 | 80 | 486-class, Pentium perf |
| 1995 | PowerPC 620 | 7,000,000 | 133 MHz | 1.5 | 200 | 64-bit PPC |
| 1995 | Alpha 21066 | 1,750,000 | 233 MHz | 1.0 | 233 | Low-cost Alpha w/ PCI |
| 1995 | HP PA-7200 | 1,260,000 | 120 MHz | 1.2 | 144 | Superscalar PA-RISC |

### The Superscalar Race

```
Superscalar: Issue multiple instructions per clock cycle

                    Issue Width    Pipeline Stages    Peak IPC
  Pentium (1993)       2              5                 2.0
  PowerPC 601          3              4                 3.0
  Alpha 21064          2              7                 2.0
  MIPS R10000          4              5                 4.0
  PowerPC 604          4              6                 4.0

The Alpha 21064A at 300 MHz was the fastest single chip in 1994.
MIPS R10000 introduced out-of-order execution to RISC in 1995.
Intel would not achieve out-of-order until Pentium Pro (1995).
```

### 64-Bit Timeline

```
First 64-bit processors by architecture:

1991 ── MIPS R4000 ──────── First 64-bit commercial CPU
1992 ── DEC Alpha 21064 ─── Designed 64-bit from scratch
1993 ── IBM POWER2 ──────── 64-bit supercomputing
1995 ── UltraSPARC I ────── 64-bit SPARC
1995 ── PowerPC 620 ─────── 64-bit PowerPC

x86 would not go 64-bit until AMD64/x86-64 in 2003!
```

---

## Era 7: The Consumer Revolution (1986-1995)

### Gaming Processors

The consumer electronics industry became a major driver of processor innovation. Game consoles and arcade machines pushed graphics, sound, and real-time performance far beyond what business computing demanded.

| Year | Processor | Platform | Clock | Significance |
|------|-----------|----------|-------|--------------|
| 1986 | TI TMS34010 | Arcade | 50 MHz | First programmable graphics processor |
| 1987 | HuC6280 | TurboGrafx-16 | 7.16 MHz | Enhanced 65C02, fast for 8-bit |
| 1988 | Motorola 68000 | Sega Genesis | 7.67 MHz | Arcade power at home |
| 1988 | Yamaha YM2612 | Sega Genesis | 7.67 MHz | FM synthesis sound chip |
| 1990 | Ricoh 5A22 | SNES | 3.58 MHz | 65816-based, DMA, HDMA |
| 1990 | SNK LSPC2 | Neo Geo | - | Sprite/tile engine |
| 1993 | ARM610 | 3DO | 12.5 MHz | First ARM in a console |
| 1994 | Sony R3000A | PlayStation | 33 MHz | MIPS in living rooms |
| 1994 | Hitachi SH-2 | Sega Saturn | 28 MHz | Dual-CPU architecture |
| 1994 | NEC V810 | Virtual Boy | 20 MHz | Portable 32-bit RISC |

```
Console CPU Evolution:

1985: NES         Ricoh 2A03     (6502)     1.79 MHz   8-bit
1988: Genesis     Motorola 68000            7.67 MHz  16-bit
1989: Game Boy    Sharp LR35902  (Z80-like) 4.19 MHz   8-bit
1990: SNES        Ricoh 5A22     (65816)    3.58 MHz  16-bit
1993: 3DO         ARM60          (ARM)     12.5  MHz  32-bit
1994: PlayStation Sony R3000A    (MIPS)    33.87 MHz  32-bit
1994: Saturn      Hitachi SH-2 x2          28.6  MHz  32-bit

In one decade: 8-bit @ 1.8 MHz --> 32-bit @ 34 MHz (19x clock, 4x width)
```

### Graphics Processors

The emergence of dedicated graphics processors during this era laid the groundwork for the modern GPU industry.

| Year | Processor | Transistors | Focus |
|------|-----------|-------------|-------|
| 1986 | TI TMS34010 | 200,000 | First programmable GPU |
| 1989 | Tseng ET4000 | 300,000 | Fast VGA Windows accelerator |
| 1991 | S3 86C911 | 350,000 | First single-chip Windows accelerator |
| 1992 | ATI Mach32 | 500,000 | GUI acceleration |
| 1992 | Weitek P9000 | 600,000 | High-end 2D/3D |
| 1994 | ATI Mach64 | 1,000,000 | Video playback acceleration |

```
Graphics acceleration timeline:

1986: TMS34010 ── Programmable, but expensive. Arcade/CAD only.
1989: ET4000 ──── Fast VGA for PCs. Windows usable at last.
1991: S3 86C911 ─ Windows accelerator for the masses. $200 cards.
1992: Mach32 ──── ATI enters the mainstream. Competition heats up.
1994: Mach64 ──── Video acceleration. Multimedia era begins.

These chips are the ancestors of modern NVIDIA and AMD GPUs.
```

### Sound Processors

| Year | Processor | Platform | Capability |
|------|-----------|----------|------------|
| 1980 | NEC uPD7720 | Various | Speech DSP |
| 1986 | Motorola DSP56001 | Pro audio | 24-bit DSP |
| 1988 | Yamaha YM2612 | Genesis | FM synthesis, 6 channels |
| 1989 | Ensoniq OTTO | Soundscape | 32-voice wavetable |

### The x86 Clone Wars

By the late 1980s, AMD, Cyrix, and NexGen all challenged Intel's x86 dominance with compatible processors, forcing prices down and accelerating innovation.

| Year | Processor | Strategy | Outcome |
|------|-----------|----------|---------|
| 1991 | AMD Am386 | Pin-compatible clone | Forced Intel to cut 386 prices |
| 1992 | Cyrix Cx486DLC | 486 performance, 386 socket | Budget upgrade path |
| 1993 | AMD Am486 | Full 486 clone | Established AMD in retail |
| 1994 | NexGen Nx586 | RISC core, x86 decode | AMD acquired NexGen (became K6) |
| 1994 | Cyrix Cx5x86 | Superscalar 486-socket | Pentium-class for less |
| 1995 | AMD Am5x86 | 133 MHz 486 | Extended 486 platform life |

```
x86 Clone Impact:

  Intel alone (pre-1991):  Intel sets prices, slow upgrades
  With competition (1991+): Prices drop 40-60%, faster cadence

  NexGen's RISC-core approach (decode x86 into internal RISC ops)
  was adopted by EVERY subsequent x86 processor:
    - AMD K6 (1997) -- direct NexGen heritage
    - Intel Pentium Pro (1995) -- same concept, independent design
    - Every x86 CPU since
```

---

## Transistor Count Evolution

```
Transistors (log scale)

10,000,000 ┤                                                          * R10000
            │                                                     * PPC 620
            │                                              * UltraSPARC
            │                                         * Pentium / PPC 601
            │                                    * Alpha 21064
 1,000,000 ┤                               * 80486 / 68040
            │                          * 80386
            │                     * iAPX 432
            │                * 68020
   100,000 ┤           * 80286
            │      * 68000
            │ * R2000
    10,000 ┤           * Z80
            │      * 8080
            │ * 8008
     1,000 ┤* 4004
            +--+----+----+----+----+----+----+----+----+----+----+----+--
              71   73   75   77   79   81   83   85   87   89   91   93  95

Moore's Law in action: ~2x every 18-24 months
4004 (1971): 2,300 --> R10000 (1995): 6,700,000 = 2,913x in 24 years
```

---

## Clock Speed Evolution

```
Clock Speed (MHz, log scale)

 300 ┤                                                          * Alpha 21064A
     │                                                     * Alpha 21066
 200 ┤                                                * R10000
     │                                           * UltraSPARC
     │                                      * Alpha 21064
 100 ┤                                 * R4000 / Am5x86
     │                            * Pentium
  50 ┤                       * TMS34010
     │                  * 68020 / 80386
  20 ┤             * 68000
     │        * 8086
  10 ┤   * NS32016
     │        * Z80
   5 ┤   * 8080
     │
   1 ┤* 4004
     +--+----+----+----+----+----+----+----+----+----+----+----+--
       71   73   75   77   79   81   83   85   87   89   91   93  95

From 740 kHz (4004) to 300 MHz (Alpha 21064A) = 405x in 23 years
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

### 1980-1985: Sophistication
- **Memory management** (80286, 68010)
- **Virtual memory** (80386, 68020)
- **Caches** (80386)
- **Pipelining** (ARM1, R2000)

### 1986-1991: RISC Maturity
- **Deep pipelining** (R4000: 8 stages)
- **On-chip FPU** (80486, 68040)
- **On-chip cache** (80486: 8 KB unified)
- **Branch prediction** (Am29000: branch-target cache)
- **Register windows** (SPARC)

### 1992-1995: Superscalar Era
- **Superscalar execution** (Pentium: dual issue)
- **Out-of-order execution** (R10000, Pentium Pro)
- **64-bit addressing** (R4000, Alpha)
- **Branch history tables** (Pentium)
- **RISC-core x86 decode** (NexGen Nx586)
- **Speculative execution** (PowerPC 604)

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
| MIPS | **Networking/embedded** | Routers, set-top boxes, IoT |
| PowerPC | **Gaming/automotive** | Wii/Wii U, automotive ECUs |

```
The Three Great Survivors:

x86 (1978):    Dominates desktops, laptops, servers
               Won through compatibility and volume

ARM (1985):    Dominates mobile, embedded, and increasingly servers
               Won through power efficiency and licensing model
               200+ billion chips shipped -- most produced CPU family ever

MIPS (1985):   Dominates networking equipment, embedded
               Won specific niches through clean 64-bit design
               Lives on in routers, set-top boxes, and IoT devices

PowerPC (1993): Gaming consoles (Wii/Wii U), automotive
               AIM alliance dissolved, but architecture endures
               IBM POWER servers carry the lineage forward
```

---

## Lessons from the Era

1. **Price matters**: The $25 6502 enabled the personal computer revolution
2. **Compatibility wins**: x86 backward compatibility ensured its survival
3. **Ecosystem beats architecture**: 8051's tools won over better MCUs
4. **Simplicity can win**: ARM1's simple design outperformed complex chips
5. **Timing is everything**: iAPX 432 was too ambitious too soon
6. **RISC and CISC converged**: By 1995, x86 chips used RISC cores internally (NexGen Nx586, Pentium Pro), while RISC chips grew more complex -- the "war" ended in synthesis, not victory
7. **Gaming drives innovation**: Consoles pushed real-time performance, graphics, and sound processing harder than business computing -- the PlayStation's MIPS R3000A brought workstation CPUs to living rooms
8. **Fragmentation loses to volume**: Four incompatible RISC workstation platforms (MIPS, SPARC, PA-RISC, POWER) split the Unix market, letting x86 PCs win through sheer volume
9. **Licensing can beat manufacturing**: ARM proved that licensing a design to many manufacturers could defeat building chips yourself -- a model now standard in the industry

---

**Document Version:** 3.0
**Last Updated:** January 30, 2026
**Processors Covered:** 422
