# Microprocessor Family Trees

## Processor Lineages and Relationships (1971-1995)

This document traces the evolutionary relationships between all **467 processors** in the collection, showing how architectures developed and influenced each other.

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
                                                   ├──► Hitachi HD64180 (1985) ✓
                                                   │       Z180 equivalent
                                                   │
                                                   └──► Z8S180 (1994) ✓
                                                           Enhanced Z180 (static CMOS)
```

### MCS-48 MCU Line (1976-1980)

```
Intel 8048 (1976) ✓
    │   First successful single-chip MCU
    │
    ├──► Intel 8035/8039 (1976) ✓
    │       ROM-less variants
    │
    ├──► Intel 8748 (1977) ✓
    │       EPROM version for development
    │
    └──► Intel 8044 (1980) ✓
            SDLC/HDLC communications controller MCU
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

Intel 8061 (1980) ✓
    │   Embedded controller
    │
    (Automotive applications)
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
    │       ├──► Intel 80188 (1982) ✓
    │       │       8-bit bus version
    │       │
    │       └──► Intel 80C186 (1988) ✓
    │               CMOS version
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

### FPU / Math Coprocessor Line (1979-1987)

```
Intel 8231 (1979) ✓
    │   Arithmetic Processing Unit (early math chip)
    │
    (Standalone APU for 8-bit systems)

Intel 8087 (1980) ✓
    │   x87 FPU for 8086/8088
    │
    ├──► Intel 8087-2 (1982) ✓
    │       Faster speed grade
    │
    ├──► Intel 80287 (1982) ✓
    │       FPU for 80286
    │
    └──► Intel 80387 (1987) ✓
            FPU for 80386
```

### I/O Coprocessor Line (1979)

```
Intel 8089 (1979) ✓
    │   I/O coprocessor for 8086
    │
    (Offloaded I/O processing from main CPU)
```

### Bit-Slice Line (1974)

```
Intel 3001/3002 (1974) ✓
    │   2-bit slice CPU building blocks
    │   Bipolar Schottky technology
    │
    └──► Intel 3003 (1974) ✓
            Look-ahead carry generator for 3002
```

### i960 RISC Line (1988-1994)

```
Intel i960 (1988) ✓
    │   32-bit RISC, from iAPX 432 team
    │
    ├──► Intel i960CA (1989) ✓
    │       Superscalar variant
    │
    └──► Intel i960CF (1990) ✓
            i960 with integrated FPU
```

### Network / Peripheral Line (1982-1997)

```
Intel 82586 (1982) ✓
    │   16-bit LAN coprocessor (Ethernet)
    │
    └──► Intel 82596 (1986) ✓
            │   32-bit LAN coprocessor
            │
            └──► Intel 82557 (1995) ✓
                    Fast Ethernet controller (PCI)

Intel 82730 (1985) ✓
    │   Text coprocessor / display controller
    │
    (Used in terminals and text display systems)
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
    │       ├──► Motorola 6803 (1981) ✓
    │       │       ROM-less 6801 variant
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
    │       ├──► Motorola 6805R2 (1981) ✓
    │       │       ROM variant
    │       │
    │       ├──► Motorola 6804 (1983) ✓
    │       │       Simplified 6805 variant
    │       │
    │       ├──► Motorola 68HC05 (1984) ✓
    │       │       CMOS version
    │       │
    │       └──► Hitachi HD6305 (1984) ✓
    │               6805-compatible MCU
    │
    ├──► Motorola 6809 (1979) ✓
    │       │   "Best 8-bit ever" - position-independent code
    │       │
    │       └──► Hitachi 6309 (1982) ✓
    │               Enhanced 6809 with extra registers
    │               Native mode 15% faster
    │
    └──► Motorola 68HC11 (1985) ✓
            │   Popular automotive MCU
            │
            ├──► Motorola 68HC11A1 (1986) ✓
            │       68HC11 variant
            │
            └──► Motorola 68HC16 (1991) ✓
                    16-bit MCU bridging 68HC11 and 68k
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
            ├──► Motorola 68851 (1984) ✓
            │       Paged MMU for 68020
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

### Embedded 68k Line (1990-1994)

```
Motorola 68302 (1990) ✓
    │   Integrated comms processor (68k + serial channels)
    │
    └──► Motorola 68360 (1993) ✓
            QUICC (Quad Integrated Communications Controller)

Motorola CPU32 (1990) ✓
    │   68020-based embedded core
    │
    └──► Motorola ColdFire (1994) ✓
            Reduced 68k ISA for embedded, variable-length instructions
```

### 88000 RISC Line (1988-1991)

```
Motorola 88100 (1988) ✓
    │   RISC processor, Harvard architecture
    │
    └──► Motorola 88110 (1991) ✓
            Superscalar, integrated FPU
            (Replaced by PowerPC alliance)
```

### Motorola DSP Line (1986-1989)

```
Motorola DSP56001 (1986) ✓
    │   24-bit fixed-point DSP
    │   Used in NeXT computer, Atari Falcon
    │
    └──► Motorola DSP96002 (1989) ✓
            32-bit IEEE floating-point DSP
```

### Motorola Communications / Other (1978-1979)

```
Motorola 6854 (1978) ✓
    │   ADLC (Advanced Data Link Controller)
    │
    (Communications peripheral)

Motorola MC14500B (1977) ✓
    │   1-bit Industrial Control Unit (ICU)
    │
    (Relay-replacement logic controller)
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
    ├──► MOS 8501 (1984) ✓
    │       C16/Plus/4 variant of 6502
    │
    ├──► MOS 8502 (1985) ✓
    │       C128 variant, 2 MHz capable
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
            ├──► G65SC802 (1986) ✓
            │       65816-compatible in 40-pin package
            │
            ├──► G65SC816 (1986) ✓
            │       65816 second-source
            │
            └──► WDC 65816 (1984) ✓
                    16-bit extension, Apple IIGS, SNES
```

---

## Zilog Family Tree

### Z80 Line (1976-1994)

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
    │       │   Z80 + MMU + DMA + serial
    │       │
    │       └──► Zilog Z8S180 (1994) ✓
    │               Enhanced Z180 (static CMOS, 33 MHz)
    │
    ├──► Zilog Z280 (1985) ✓
    │       Enhanced Z80 with MMU, cache (failed successor - too complex)
    │
    └──► Zilog Z380 (1994) ✓
            32-bit Z80 extension
```

### Z8 MCU Line (1979+)

```
Zilog Z8 (1979) ✓
    │   MCU family (not Z80-related)
    │
    └──► Zilog Super8 (1985) ✓
            Enhanced Z8 MCU, more instructions
```

### Z8000 Line (1979-1986)

```
Zilog Z8000 (1979) ✓
    │   16-bit, segmented memory
    │
    └──► Zilog Z80000 (1986) ✓
            32-bit, limited success
```

### Z80 Peripheral Line

```
Zilog Z80-SIO (1976) ✓
    │   Z80 Serial I/O controller
    │
    └──► Zilog Z8530 (1985) ✓
            SCC (Serial Communications Controller)
            Used in Mac, Sun workstations

Zilog Z8016-DMA (1976) ✓
    │   Z80 DMA controller
    │
    (Used with Z80 systems for block transfers)
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
    ├──► RCA CDP1806 (1985) ✓
    │       Final COSMAC
    │
    └──► RCA CDP1861 (1976) ✓
            Pixie video chip for COSMAC system
```

---

## Texas Instruments Family Tree

### Calculator / 4-bit MCU Line (1974+)

```
TI TMS0800 (1972) ✓
    │   Calculator chip, predecessor to TMS1000
    │
    └──► TI TMS1000 (1974) ✓
            First mass-produced MCU
            Billions shipped (calculators, Speak & Spell)

TI TMS5100 (1978) ✓
    │   Speech synthesis processor (Speak & Spell)
    │
    (Linear predictive coding)
```

### TMS9900 Line (1976-1981)

```
TI TMS9900 (1976) ✓
    │   16-bit, workspace registers in RAM
    │   TI-99/4A home computer (CPI ~20, very slow)
    │
    ├──► TI TMS9980 (1978) ✓
    │       8-bit bus TMS9900
    │
    ├──► TI TMS9985 (1979) ✓
    │       Enhanced TMS9900 with on-chip RAM
    │
    └──► TI TMS9995 (1981) ✓
            On-chip RAM, faster
```

### TMS MCU Lines (1980s)

```
TI TMS7000 (1981) ✓
    │   8-bit MCU family
    │
    (Industrial and automotive applications)

TI TMS370 (1988) ✓
    │   8-bit MCU family, 8-channel A/D
    │
    (Automotive and industrial)
```

### TMS320 DSP Dynasty (1982-1994)

```
TI TMS320C10 (1982) ✓
    │   First TI DSP, fixed-point
    │
    ├──► TI TMS320C25 (1986) ✓
    │       │   2nd gen fixed-point DSP
    │       │
    │       └──► TI TMS320C50 (1991) ✓
    │               Enhanced fixed-point
    │
    ├──► TI TMS320C30 (1988) ✓
    │       │   First TI floating-point DSP
    │       │
    │       └──► TI TMS320C40 (1994) ✓
    │               Multi-processor capable DSP
    │
    └──► TI TMS320C80 (1994) ✓
            MVP (Multimedia Video Processor)
            Master RISC + 4 DSP cores
```

### TMS Graphics Line (1986-1988)

```
TI TMS34010 (1986) ✓
    │   First programmable graphics processor
    │
    └──► TI TMS34020 (1988) ✓
            Enhanced GPU, 32-bit
```

### TI Bit-Slice Line (1975-1977)

```
TI SBP0400 (1975) ✓
    │   4-bit slice processor (I2L technology)
    │
    └──► TI SBP0401 (1977) ✓
            Enhanced bit-slice

TI SN74181 (1970) ✓
    │   First single-chip ALU (4-bit)
    │   TTL, used in countless minicomputers
    │
    └──► TI SN74S481 (1976) ✓
            4-bit slice ALU (Schottky)
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
            ├──► ARM250 (1990) ✓
            │       ARM2 + MEMC + VIDC + IOC in one package
            │
            └──► ARM3 (1989) ✓
                    │   First cached ARM (4KB)
                    │
                    └──► ARM6 (1991) ✓
                            │   32-bit address space
                            │
                            ├──► ARM610 (1993) ✓
                            │       ARM6-based with 4KB cache
                            │
                            └──► ARM7TDMI (1994) ✓
                                    Thumb + Debug + Multiplier + ICE
                                    Most licensed ARM core ever
```

---

## AMD Family Tree

### Bit-Slice Line (1975-1988)

```
AMD Am2901 (1975) ✓
    │   4-bit slice ALU, industry standard
    │
    ├──► AMD Am2903 (1976) ✓
    │       Enhanced version with hardware multiply
    │
    ├──► AMD Am2910 (1977) ✓
    │       Microsequencer (companion to Am2901)
    │
    ├──► AMD Am29116 (1983) ✓
    │       16-bit microprocessor slice
    │
    └──► AMD Am29C101 (1988) ✓
            CMOS bit-slice (last generation)
```

### AMD RISC Line (1988)

```
AMD Am29000 (1988) ✓
    │   32-bit RISC, popular in laser printers
    │
    (Large register file, branch target cache)
```

### AMD x86 Clone Line (1991-1995)

```
AMD Am386 (1991) ✓
    │   Intel 80386 clone, 40 MHz
    │
    └──► AMD Am486 (1993) ✓
            │   Intel 80486 clone
            │
            └──► AMD Am5x86 (1995) ✓
                    486-class with clock multiplication (133 MHz)
```

### Math Coprocessor Line (1977-1979)

```
AMD Am9511 (1977) ✓
    │   First math coprocessor for 8-bit systems
    │   Stack-based, 32-bit floating point
    │
    └──► AMD Am9512 (1979) ✓
            Enhanced, 64-bit double precision
```

### AMD Network Line (1993)

```
AMD Am79C970 (1993) ✓
    │   PCnet-PCI Ethernet controller
    │
    (Single-chip Ethernet, widely emulated in VMs)
```

---

## NEC Family Tree

### 4-Bit Line (1972-1980)

```
NEC μCOM-4 (1972) ✓
    │   TMS1000 competitor
    │
    ├──► NEC μPD751 (1974) ✓
    │       Enhanced 4-bit MCU
    │
    ├──► NEC μPD546 (1975) ✓
    │       4-bit calculator/controller
    │
    └──► NEC μPD1007C (1980) ✓
            4-bit MCU (advanced series)
```

### 8-Bit MCU Line (1980s)

```
NEC μPD7801 (1982) ✓
    │   8-bit MCU
    │
    └──► NEC μPD7810 (1984) ✓
            Enhanced 8-bit MCU with more features
```

### Z80 / 8-Bit Compatible Line (1976+)

```
NEC μPD780 (1976) ✓
    │   Z80 clone for Japanese market
    │
    (Basis for NEC's 8-bit expertise)
```

### V-Series x86-Compatible Line (1984-1989)

```
NEC V20 (1984) ✓
    │   8088-compatible, 15% faster, 8080 mode
    │
    └──► NEC V30 (1984) ✓
            16-bit bus version of V20
```

### V-Series RISC Line (1986-1994)

```
NEC V60 (1986) ✓
    │   32-bit CISC/RISC hybrid
    │
    └──► NEC V70 (1987) ✓
            │   Enhanced V60, 64-bit data bus
            │
            ├──► NEC V810 (1994) ✓
            │       32-bit RISC (Virtual Boy)
            │
            └──► NEC V850 (1994) ✓
                    32-bit embedded RISC
```

### NEC DSP / Display Line (1980-1985)

```
NEC μPD7720 (1980) ✓
    │   Early DSP, speech synthesis
    │   Used in Super Nintendo audio
    │
    └──► NEC μPD7725 (1985) ✓
            Enhanced DSP (faster, more memory)

NEC μPD7759 (1985) ✓
    │   ADPCM speech synthesis processor
    │
    (Arcade machines, consumer products)

NEC μPD7220 (1982) ✓
    │   Graphics display controller
    │
    (First GDC chip - industry standard)

NEC μPD612x (1980) ✓
    │   Serial interface / peripheral
    │
    (Communications controller)
```

---

## Hitachi Family Tree

### 6800-Compatible Line (1982-1985)

```
Hitachi HD6301 (1983) ✓
    │   Enhanced 6801 clone, 8% faster
    │
    (Sega Master System, various embedded)

Hitachi 6309 (1982) ✓
    │   Enhanced 6809, extra registers, native mode
    │
    (TRS-80 Color Computer, embedded)

Hitachi HD6305 (1984) ✓
    │   6805-compatible MCU
    │
    (Low-cost embedded applications)
```

### Z180-Compatible Line (1985)

```
Hitachi HD64180 (1985) ✓
    │   Z180 equivalent, widely used in embedded
    │
    (Industrial controllers, communications)
```

### Display Controller Line (1985)

```
Hitachi HD63484 (1985) ✓
    │   ACRTC (Advanced CRT Controller)
    │
    └──► Hitachi HD63484-2 (1987) ✓
            ACRTC variant (faster/enhanced)
```

### Sega Custom / Encryption Line (1986-1990)

```
Hitachi FD1089 (1986) ✓
    │   Sega encryption MCU (68k game protection)
    │
    └──► Hitachi FD1094 (1987) ✓
            Enhanced encryption MCU
```

### 4-Bit MCU Line (1980)

```
Hitachi HMCS40 (1980) ✓
    │   4-bit MCU family
    │
    (Handheld games, consumer electronics)
```

### H8 MCU Line (1990-1992)

```
Hitachi H8/300 (1990) ✓
    │   8/16-bit MCU, large register file
    │
    └──► Hitachi H8/500 (1992) ✓
            16-bit MCU, enhanced H8
```

### SuperH RISC Line (1992-1994)

```
Hitachi SH-1 (1992) ✓
    │   16-bit fixed-length instructions, RISC
    │   Sega Saturn co-processor
    │
    └──► Hitachi SH-2 (1994) ✓
            Enhanced, dual SH-2 in Sega Saturn
            Also in Sega 32X
```

---

## Fujitsu Family Tree

### MB884x Arcade MCU Line (1977-1983)

```
Fujitsu MB8841 (1977) ✓
    │   4-bit MCU for arcade machines
    │
    ├──► Fujitsu MB8842 (1978) ✓
    │       Variant with different ROM size
    │
    ├──► Fujitsu MB8843 (1979) ✓
    │       Enhanced I/O
    │
    ├──► Fujitsu MB8844 (1980) ✓
    │       More ROM/RAM
    │
    └──► Fujitsu MB8845 (1983) ✓
            Final variant
```

### 6800-Compatible Line (1977)

```
Fujitsu MB8861 (1977) ✓
    │   6800 clone for Japanese market
    │
    (Used in early Japanese arcade games)
```

### Fujitsu SPARC Line (1987-1992)

```
Fujitsu MB86900 (1987) ✓
    │   First SPARC implementation, used in Sun-4
    │
    └──► Fujitsu SPARClite (1992) ✓
            Embedded SPARC variant (reduced area)
```

---

## Toshiba Family Tree

### TLCS 4-Bit Line (1978)

```
Toshiba TLCS-47 (1978) ✓
    │   4-bit MCU family
    │
    (Consumer electronics, calculators)
```

### TLCS 12-Bit Line (1978-1980)

```
Toshiba TLCS-12 (1978) ✓
    │   12-bit processor
    │
    └──► Toshiba TLCS-12A (1980) ✓
            Enhanced 12-bit
```

### TLCS 8-Bit MCU Line (1990)

```
Toshiba TLCS-870 (1990) ✓
    │   8-bit MCU
    │
    (Industrial and consumer applications)
```

### TLCS 16-Bit Line (1988)

```
Toshiba TLCS-90 (1988) ✓
    │   Z80-compatible MCU with enhancements
    │
    (Embedded systems)
```

### Toshiba MIPS Line (1994)

```
Toshiba TX39 (1994) ✓
    │   MIPS R3000-based embedded processor
    │
    (Embedded and portable devices)
```

---

## Eastern Bloc Family Tree

### Soviet 8-Bit Clones

```
KR580VM1 (1977) ✓
    │   Soviet Intel 8080 clone
    │
    ├──► IM1821VM85A (1985) ✓
    │       Soviet 8085 clone (radiation-hardened)
    │
    └──► MCY7880 (1983) ✓
            East German 8080-compatible

Tesla MHB8080A (1978) ✓
    │   Czech 8080 clone
    │
    (COMECON standardization)

U808 (1978) ✓
    │   East German (DDR) 8-bit
    │
    └──► U880 (1980) ✓
            │   East German Z80 clone
            │
            └──► U80701 (1988) ✓
                    East German controller variant

U8001 (1980) ✓
    │   East German Z8000 clone
    │
    (COMECON 16-bit computing)
```

### Soviet 8051 Clone

```
K580IK51 (1986) ✓
    │   Soviet Intel 8051 clone
    │
    (Industrial embedded applications)
```

### Soviet Bit-Slice Line

```
KR581IK1 (1978) ✓
    │   Soviet bit-slice ALU (Am2901 equivalent)
    │
    └──► KR581IK2 (1980) ✓
            Enhanced bit-slice

KR1858VM1 (1985) ✓
    │   Soviet advanced bit-slice
    │
    (Military computing)
```

### Soviet x86 Clones

```
K1810VM86 (1984) ✓
    │   Soviet Intel 8086 clone
    │
    └──► K1810VM88 (1986) ✓
            Soviet Intel 8088 clone
```

### Soviet PDP-11 Clone Line (1980-1991)

```
K1801VM1 (1980) ✓
    │   Soviet PDP-11 clone (LSI-11 equivalent)
    │   Used in Soviet personal computers
    │
    ├──► K1801VM2 (1983) ✓
    │       Enhanced Soviet PDP-11
    │
    └──► K1801VM3 (1985) ✓
            Soviet PDP-11 with FPU

K1839VM1 (1991) ✓
    │   Soviet advanced 16-bit processor
    │
    (Late Soviet-era design)
```

### Soviet CMxxxx Series

```
CM630 (1982) ✓
    │   Soviet custom processor
    │
    (Military applications)
```

### Elbrus Line (1990)

```
Elbrus EL-90 (1990) ✓
    │   Soviet RISC processor
    │   Part of Elbrus supercomputer series
    │
    (Most advanced Soviet processor design)
```

### Other Eastern Bloc

```
MPA1008 (1985) ✓
    │   East German/Czech processor
    │
    (COMECON computing)

TVC CPU (1986) ✓
    │   Hungarian TVC computer CPU
    │
    (Hungarian home computing)
```

---

## National Semiconductor Family Tree

### 16-Bit Pioneer Line (1973-1975)

```
National IMP-16 (1973) ✓
    │   Early 16-bit (bit-slice based)
    │
    └──► National PACE (1975) ✓
            Single-chip 16-bit, p-channel MOS
```

### 8-Bit Line (1974-1982)

```
National SC/MP (1974) ✓
    │   Simple, low-cost 8-bit
    │
    (End of line)

National NSC800 (1980) ✓
    │   Z80-compatible (CMOS, low-power)
    │
    (Military and battery-powered applications)
```

### NS32000 Line (1982-1986)

```
National NS32016 (1982) ✓
    │   Early 32-bit CISC
    │
    └──► National NS32032 (1984) ✓
            │   Improved version, true 32-bit bus
            │
            ├──► NS32081 FPU (1982) ✓
            │       Floating-point unit for NS32000
            │
            ├──► NS32082 MMU (1984) ✓
            │       Paged MMU for NS32000
            │
            └──► NS32381 FPU (1986) ✓
                    Enhanced FPU (successor to NS32081)
```

### COP400 MCU Line (1977-1982)

```
National COP400 (1977) ✓
    │   4-bit MCU family
    │
    ├──► National COP420 (1979) ✓
    │       Enhanced COP400 with more RAM
    │
    └──► National COP444 (1982) ✓
            Extended COP400, more I/O
```

---

## Rockwell Family Tree

```
Rockwell PPS-4 (1972) ✓
    │   Third commercial microprocessor
    │   Serial ALU, used in pinball machines
    │
    └──► Rockwell PPS-4/1 (1976) ✓
            Single-chip variant

Rockwell R6500/1 (1978) ✓
    │   6502-based single-chip MCU
    │
    └──► Rockwell R6511 (1980) ✓
            6502 + on-chip peripherals

Rockwell R65C02 (1983) ✓
    │   CMOS 6502 + bit manipulation instructions
    │
    (Licensed/second-sourced design)
```

---

## AMI Family Tree

### S2000 Calculator Line (1971-1978)

```
AMI S2000 (1971) ✓
    │   Calculator processor
    │
    ├──► AMI S2150 (1973) ✓
    │       Enhanced calculator chip
    │
    ├──► AMI S2200 (1974) ✓
    │       More functions
    │
    └──► AMI S2400 (1975) ✓
            Advanced calculator
```

### Signal Processing Line (1978-1980)

```
AMI S2811 (1978) ✓
    │   Early signal processor
    │   Modems, telecommunications
    │
    └──► AMI S28211 (1980) ✓
            Enhanced signal processor
```

---

## Mitsubishi Family Tree

### MELPS 4-Bit Line (1978-1985)

```
Mitsubishi MELPS-4 (1978) ✓
    │   4-bit MCU family
    │
    ├──► Mitsubishi MELPS-41 (1980) ✓
    │       Enhanced variant
    │
    └──► Mitsubishi MELPS-42 (1982) ✓
            Further enhancements
```

### MELPS 8-Bit / M50740 Line (1983-1985)

```
Mitsubishi MELPS-740 (1983) ✓
    │   8-bit MCU (6502-derived)
    │
    ├──► Mitsubishi M50740 (1984) ✓
    │       MCU with on-chip peripherals
    │
    └──► Mitsubishi M50747 (1985) ✓
            Enhanced variant, more I/O
```

---

## Namco Arcade Custom Family Tree

```
Namco 05xx (1980) ✓
    │   Custom starfield generator
    │
    (Galaga, Bosconian)

Namco 50xx (1981) ✓
    │   Custom score/display processor
    │
    (Galaga)

Namco 51xx (1981) ✓
    │   Custom I/O processor
    │
    (Galaga, Bosconian)

Namco 52xx (1982) ✓
    │   Custom sound processor
    │
    (Rally-X, Bosconian)

Namco 53xx (1982) ✓
    │   Custom I/O multiplexer
    │
    (Pole Position)

Namco 54xx (1982) ✓
    │   Custom noise/sound generator
    │
    (Galaga, Bosconian)
```

---

## MIPS Family Tree

```
Stanford MIPS (1983) ✓
    │   Academic MIPS prototype
    │   5-stage pipeline concept
    │
    └──► MIPS R2000 (1985) ✓
            │   First commercial 5-stage pipeline
            │
            └──► MIPS R3000 (1988) ✓
                    │   Enhanced, widely used (PlayStation, DECstation)
                    │
                    └──► MIPS R4000 (1991) ✓
                            │   First 64-bit MIPS, 8-stage pipeline
                            │
                            ├──► MIPS R4400 (1993) ✓
                            │       R4000 with bug fixes, larger cache
                            │
                            ├──► MIPS R4600 (1994) ✓
                            │       Low-cost embedded R4000
                            │
                            ├──► MIPS R8000 (1994) ✓
                            │       Floating-point superscalar (HPC)
                            │
                            └──► MIPS R10000 (1995) ✓
                                    Out-of-order superscalar

    Derivatives:
    Sony R3000A (1994) ✓ - PlayStation CPU (R3000-based)
    Toshiba TX39 (1994) ✓ - R3000 embedded variant
```

---

## SPARC Family Tree

```
Berkeley RISC I (1982) ✓
    │   First RISC processor (academic)
    │   Register windows, delayed branches
    │
    └──► Berkeley RISC II (1983) ✓
            │   Improved version, 138 registers
            │
            └──► Sun SPARC (1987) ✓
                    │   Commercial RISC from Berkeley research
                    │
                    ├──► Fujitsu MB86900 (1987) ✓
                    │       First SPARC silicon (Sun-4)
                    │
                    ├──► Cypress CY7C601 (1988) ✓
                    │       SPARC implementation (SPARCstation 1)
                    │
                    ├──► Fujitsu SPARClite (1992) ✓
                    │       Embedded SPARC variant
                    │
                    ├──► MicroSPARC (1992) ✓
                    │       │   Low-cost single-chip SPARC
                    │       │
                    │       └──► MicroSPARC II (1994) ✓
                    │               Enhanced, SPARCstation 5
                    │
                    ├──► SuperSPARC (1992) ✓
                    │       Superscalar SPARC (TI-built)
                    │
                    ├──► HyperSPARC (1993) ✓
                    │       Ross Technology SPARC
                    │
                    ├──► HAL SPARC64 (1995) ✓
                    │       64-bit SPARC implementation
                    │
                    └──► UltraSPARC I (1995) ✓
                            64-bit, VIS multimedia extensions
```

---

## HP PA-RISC Family Tree

```
HP PA-RISC (1986) ✓
    │   Precision Architecture RISC
    │   HP workstations and servers
    │
    ├──► HP PA-7100 (1992) ✓
    │       │   Superscalar PA-RISC
    │       │
    │       └──► HP PA-7100LC (1994) ✓
    │               Low-cost integrated version
    │
    └──► HP PA-7200 (1994) ✓
            Enhanced with on-chip L1 cache
```

---

## IBM POWER / PowerPC Family Tree

### IBM POWER Line (1990-1997)

```
IBM POWER1 (1990) ✓
    │   Performance Optimization With Enhanced RISC
    │   RS/6000 workstations
    │
    └──► IBM POWER2 (1993) ✓
            │   Dual FPU, wider issue
            │
            └──► IBM RS64 (1997) ✓
                    64-bit POWER implementation
```

### PowerPC Line (1993-1995)

```
AIM PowerPC 601 (1993) ✓
    │   Apple/IBM/Motorola alliance
    │   First PowerPC, POWER1-compatible
    │
    ├──► PowerPC 603 (1994) ✓
    │       Low-power, 5-stage pipeline
    │
    ├──► PowerPC 604 (1995) ✓
    │       Superscalar, out-of-order
    │
    └──► PowerPC 620 (1995) ✓
            First 64-bit PowerPC
```

---

## DEC Alpha Family Tree

```
DEC Alpha 21064 (1992) ✓
    │   64-bit, fastest of its era (200 MHz)
    │
    ├──► DEC Alpha 21064A (1994) ✓
    │       Die shrink, 275 MHz
    │
    └──► DEC Alpha 21066 (1993) ✓
            Low-cost Alpha with integrated PCI
```

---

## DEC PDP-11 / VAX Chip Line

```
DEC J-11 (1979) ✓
    │   PDP-11 on a chip (PDP-11/84)
    │
    (DEC minicomputer replacement)

DEC T-11 (1982) ✓
    │   Low-cost PDP-11 on a chip
    │
    (Embedded PDP-11 applications)

MicroVAX 78032 (1985) ✓
    │   VAX on a chip
    │
    (MicroVAX II desktop)
```

---

## x86 Clone Family Tree

```
Intel 80386 (1985)
    │
    └──► AMD Am386 (1991) ✓
            Pin-compatible clone, 40 MHz

Intel 80486 (1989)
    │
    ├──► AMD Am486 (1993) ✓
    │       │   Pin-compatible clone
    │       │
    │       └──► AMD Am5x86 (1995) ✓
    │               486-class, 133 MHz clock multiplication
    │
    ├──► Cyrix Cx486DLC (1992) ✓
    │       386-pin-compatible with 486 core features
    │
    ├──► Cyrix Cx486SLC (1992) ✓
    │       386SX-pin-compatible with 486 core features
    │
    ├──► IBM 486SLC2 (1992) ✓
    │       IBM-enhanced Cyrix design, clock-doubled
    │
    ├──► UMC U5S (1994) ✓
    │       Taiwanese 486 clone
    │
    └──► Hyundai 486 (1994) ✓
            Korean 486 clone

Intel Pentium (1993)
    │
    ├──► Cyrix Cx5x86 (1995) ✓
    │       Pentium-class from 486 socket
    │
    └──► NexGen Nx586 (1994) ✓
            RISC core with x86 translation layer
```

---

## Transputer Family Tree

```
INMOS T212 (1985) ✓
    │   16-bit transputer, 4 serial links
    │
    (Parallel computing building block)

INMOS T414 (1985) ✓
    │   32-bit transputer
    │
    ├──► INMOS T424 (1989) ✓
    │       Enhanced T414
    │
    └──► INMOS T800 (1987) ✓
            T414 + on-chip FPU
            (Parallel supercomputing)
```

---

## DSP Family Tree (Expanded)

### TI DSP Line

```
TI TMS320C10 (1982) ✓
    │   First TI DSP
    │
    ├──► TI TMS320C25 (1986) ✓ ──► TI TMS320C50 (1991) ✓
    │       2nd gen fixed-point        Enhanced fixed-point
    │
    ├──► TI TMS320C30 (1988) ✓ ──► TI TMS320C40 (1994) ✓
    │       Floating-point DSP         Multi-processor DSP
    │
    └──► TI TMS320C80 (1994) ✓
            MVP: Master RISC + 4 DSP cores
```

### Motorola DSP Line

```
Motorola DSP56001 (1986) ✓
    │   24-bit fixed-point DSP
    │
    └──► Motorola DSP96002 (1989) ✓
            32-bit IEEE floating-point DSP
```

### AT&T / Lucent DSP Line

```
AT&T DSP-1 (1980) ✓
    │   First AT&T DSP (Bell Labs)
    │
    └──► AT&T DSP-16 (1987) ✓
            │   16-bit fixed-point
            │
            ├──► AT&T DSP-20 (1988) ✓
            │       Enhanced version
            │
            └──► AT&T DSP-32C (1988) ✓
                    │   32-bit floating-point
                    │
                    └──► Lucent DSP1600 (1992) ✓
                            Successor (AT&T → Lucent)
```

### Analog Devices DSP Line

```
ADSP-2100 (1986) ✓
    │   16-bit fixed-point DSP
    │
    ├──► ADSP-2105 (1989) ✓
    │       Cost-reduced variant
    │
    └──► ADSP-21020 (1991) ✓
            32-bit floating-point SHARC predecessor
```

### NEC DSP Line

```
NEC μPD7720 (1980) ✓
    │   Early DSP, speech synthesis
    │
    └──► NEC μPD7725 (1985) ✓
            Enhanced DSP
```

### Other DSPs

```
Zoran ZR34161 (1987) ✓
    │   Vector DSP for image processing
    │
    (JPEG/MPEG acceleration)

SGS D950 (1982) ✓
    │   European DSP
    │
    (Telecommunications)

DSP56000 (1986) ✓
    │   Motorola DSP variant
    │
    (Audio processing)
```

---

## Gaming / Sound / Graphics Family Trees

### Yamaha FM Sound Line

```
Yamaha YM3526/OPL (1984) ✓
    │   FM synthesis sound chip
    │
    └──► Yamaha YM3812/OPL2 (1985) ✓
            │   Enhanced OPL, AdLib/Sound Blaster
            │
            └──► Yamaha YMF262/OPL3 (1990) ✓
                    4-operator, stereo FM

Yamaha YM2151/OPM (1984) ✓
    │   8-channel FM, arcade standard
    │
    (Capcom CPS, Sega, Konami, Namco arcade)

Yamaha YM2610 (1987) ✓
    │   FM + ADPCM, Neo Geo sound
    │
    (SNK Neo Geo arcade/console)

Yamaha YM2612 (1988) ✓
    │   6-channel FM, Sega Genesis/Mega Drive
    │
    (Iconic Genesis sound)
```

### Console CPU Line

```
Ricoh 2A03 (1983) ✓ - NES (6502 + audio, no BCD)
Ricoh 5A22 (1990) ✓ - SNES (65C816-based + DMA)
HuC6280 (1987) ✓ - TurboGrafx-16 (65C02 derivative)
Sony R3000A (1994) ✓ - PlayStation (MIPS R3000-based)
```

### Sega Custom Line

```
Sega 315-5124/VDP (1985) ✓
    │   Video Display Processor (Master System)
    │
    └──► Sega 315-5313/VDP (1988) ✓
            │   Enhanced VDP (Genesis/Mega Drive)
            │
            └──► Sega SVP (1994) ✓
                    Samsung DSP in Virtua Racing cart

SNK LSPC2 (1990) ✓
    │   Neo Geo line sprite controller
    │
    (Arcade and AES home system)
```

### Video / Graphics Controller Line

```
NEC μPD7220 (1982) ✓
    │   First graphics display controller
    │
    └──► V9938 (1985) ✓
            Yamaha MSX2 video chip

TI TMS9918A (1979) ✓
    │   Video Display Processor (MSX, ColecoVision, TI-99)
    │
    (Foundational home computer/console VDP)

Hitachi HD63484 (1985) ✓ - ACRTC
    └──► HD63484-2 (1987) ✓

TI TMS34010 (1986) ✓ ──► TMS34020 (1988) ✓
    Programmable graphics processors
```

### PC Graphics Accelerator Line

```
S3 86C911 (1991) ✓
    │   First single-chip GUI accelerator
    │
    (Defined the Windows accelerator category)

Tseng ET4000 (1989) ✓
    │   Popular VGA accelerator
    │
    (Fast, widely compatible)

ATI Mach32 (1992) ✓
    │   GUI accelerator
    │
    └──► ATI Mach64 (1994) ✓
            Video playback acceleration

Weitek P9000 (1992) ✓
    │   High-end graphics coprocessor
    │
    (CAD/workstation graphics)

Chips & Technologies 65545 (1993) ✓
    │   Laptop graphics controller
    │
    (Mobile/embedded graphics)

IIT AGX (1993) ✓
    │   Graphics accelerator
    │
    (Budget PC graphics)
```

### Sound / Audio Chip Line

```
TI SN76489 (1980) ✓
    │   Programmable Sound Generator (PSG)
    │   Master System, Genesis, BBC Micro, ColecoVision
    │
    (Foundational PSG)

Atari POKEY (1979) ✓
    │   4-channel sound + I/O + keyboard scan
    │   Atari 400/800, arcade games
    │
    (Atari ecosystem standard)

GI SP0256 (1981) ✓
    │   Speech synthesis chip (allophone)
    │   Intellivision, arcade games
    │
    (Consumer speech synthesis)

Ensoniq OTTO (1989) ✓
    │   32-voice wavetable sound engine
    │   Ensoniq sound cards
    │
    (Wavetable synthesis)

Ensoniq ES5503 (1986) ✓
    │   DOC (Digital Oscillator Chip)
    │   Apple IIGS, Ensoniq synths
    │
    (32-voice wavetable)

NEC μPD7759 (1985) ✓
    │   ADPCM speech synthesis
    │
    (Arcade machines)

Harris HC55516 (1980) ✓
    │   CVSD speech codec
    │
    (Williams arcade: Robotron, Joust, Defender)
```

### Video Chips (Atari / Commodore)

```
Atari ANTIC (1979) ✓
    │   Alphanumeric Television Interface Controller
    │   Atari 400/800 display list processor
    │
    (Programmable display hardware)

Atari TED (1984) ✓
    │   Text Editing Device (Commodore Plus/4, C16)
    │   Combined video + sound
    │
    (Cost-reduced C64 replacement)

MOS VIC 6560 (1980) ✓
    │   Video Interface Chip (VIC-20)
    │
    └──► MOS VIC-II 6569 (1982) ✓
            Enhanced VIC for Commodore 64
            Sprites, bitmap modes, raster IRQ

Ricoh 2C02 (1983) ✓ - NES PPU (NTSC)
    └──► Ricoh 2C07 (1986) ✓ - NES PPU (PAL)

MOS 6581 SID (1982) ✓ - Sound Interface Device (C64)
    └──► MOS 8580 SID (1986) ✓ - Revised SID (C64C, C128)
```

### Signetics PVI (1977)

```
Signetics 2636 PVI (1977) ✓
    │   Programmable Video Interface
    │
    (Early dedicated game hardware)
```

### GI / Atari Game Hardware

```
GI AY-3-8500 (1976) ✓
    │   Pong-on-a-chip
    │
    (Dozens of Pong clones)

GI AY-3-8900 (1978) ✓
    │   Advanced game chip
    │
    (Later game consoles)

GI AY-3-8910 (1978) ✓
    │   Programmable Sound Generator
    │   Vectrex, MSX, Amstrad CPC, ZX Spectrum 128
    │
    (Widely used PSG)
```

---

## LISP Machine Family Tree

```
Symbolics CADR (1981) ✓
    │   MIT AI Lab LISP machine
    │
    (Symbolics 3600 series)

LMI Lambda (1984) ✓
    │   LISP Machine Inc. processor
    │
    (CADR-derived architecture)

TI Explorer (1987) ✓
    │   TI's LISP machine processor
    │
    (Commercial LISP workstation)
```

---

## Transputer / Parallel Processing Line

```
INMOS T212 (1985) ✓ - 16-bit transputer
INMOS T414 (1985) ✓ - 32-bit transputer
    ├──► INMOS T424 (1989) ✓ - Enhanced T414
    └──► INMOS T800 (1987) ✓ - T414 + FPU

Intel iWarp (1989) ✓
    │   Systolic array processor (CMU/Intel)
    │
    (Parallel computing research)

ICL DAP (1980) ✓
    │   Distributed Array Processor
    │   SIMD parallel architecture
    │
    (Massively parallel computing)

Staran (1972) ✓
    │   Goodyear associative array processor
    │
    (Early SIMD / content-addressable)
```

---

## Stack Machine Family Tree

```
Novix NC4000 (1985) ✓
    │   Forth-in-silicon prototype
    │
    └──► Novix NC4016 (1985) ✓
            │   Production Forth stack processor
            │
            └──► Harris RTX2000 (1988) ✓
                    │   Enhanced Forth processor (rad-hard)
                    │
                    └──► Harris RTX32P (1992) ✓
                            32-bit Forth processor

MuP21 (1994) ✓
    │   Chuck Moore's minimal Forth chip
    │
    (21 instructions, extreme minimalism)
```

---

## 4-Bit Processor Family Tree

```
Intel 4004 (1971) ✓
    │   First microprocessor
    │
    └──► Intel 4040 (1974) ✓

Rockwell PPS-4 (1972) ✓
    │   Third commercial microprocessor
    │   Serial ALU, used in pinball machines
    │
    └──► Rockwell PPS-4/1 (1976) ✓
            Single-chip variant

NEC μCOM-4 (1972) ✓ ──► μPD751 (1974) ✓ ──► μPD546 (1975) ✓
                                              μPD1007C (1980) ✓

TI TMS0800 (1972) ✓ ──► TI TMS1000 (1974) ✓
    Calculator chip        First mass-produced MCU

AMI S2000 (1971) ✓ ──► S2150 ✓ ──► S2200 ✓ ──► S2400 ✓
    Calculator processors

Mitsubishi MELPS-4 (1978) ✓ ──► MELPS-41 ✓ ──► MELPS-42 ✓

Hitachi HMCS40 (1980) ✓ - Handheld games

Fujitsu MB8841 (1977) ✓ ──► MB8842 ✓ ──► MB8843 ✓ ──► MB8844 ✓ ──► MB8845 ✓
    Arcade MCU family

Toshiba TLCS-47 (1978) ✓ - 4-bit MCU

National COP400 (1977) ✓ ──► COP420 ✓ ──► COP444 ✓

Samsung SM4 (1983) ✓ - 4-bit MCU
    └──► Samsung SM5 (1985) ✓ - Enhanced 4-bit

Sanyo LC87 (1982) ✓ - 4-bit MCU
```

---

## Bit-Slice and ALU Family Tree

```
TI SN74181 (1970) ✓
    │   First single-chip ALU (4-bit, TTL)
    │
    └──► TI SN74S481 (1976) ✓
            4-bit slice ALU (Schottky)

AMD Am2901 (1975) ✓
    │   4-bit slice ALU, industry standard
    │
    ├──► AMD Am2903 (1976) ✓
    │       Hardware multiply
    │
    ├──► AMD Am2910 (1977) ✓
    │       Microsequencer companion
    │
    ├──► AMD Am29116 (1983) ✓
    │       16-bit microprocessor slice
    │
    └──► AMD Am29C101 (1988) ✓
            CMOS bit-slice

Intel 3001/3002 (1974) ✓
    │   2-bit slice, Intel's bit-slice family
    │
    └──► Intel 3003 (1974) ✓
            Look-ahead carry generator

TI SBP0400 (1975) ✓ ──► SBP0401 (1977) ✓
    I2L bit-slice family

Monolithic Memories 6701 (1975) ✓
    │   4-bit slice ALU competitor
    │
    └──► MMI 67110 (1978) ✓
            Enhanced bit-slice

Motorola MC10800 (1977) ✓
    │   ECL 4-bit slice ALU
    │
    (Fastest bit-slice of its era)

KR581IK1 (1978) ✓ ──► KR581IK2 (1980) ✓
    Soviet Am2901 equivalents

KR1858VM1 (1985) ✓ - Soviet advanced bit-slice

WD9000 (1979) ✓
    │   Western Digital bit-slice Pascal MicroEngine
    │
    (UCSD Pascal hardware support)
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

Intel 8231 (1979) ✓
    │   Arithmetic Processing Unit
    │
    (Standalone APU for 8-bit systems)

Intel 8087 (1980) ✓
    │
    ├──► Intel 8087-2 (1982) ✓
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
    └──► National NS32381 (1986) ✓
            Enhanced FPU

Weitek 1064 (1982) ✓
    │   High-speed FPU coprocessor
    │
    (Used in workstations)
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
    └──► Data General mN602 (1980) ✓
            Enhanced microNova

Western Digital WD16 (1977) ✓
    │   LSI-11 (PDP-11) compatible
    │
    (DEC minicomputer replacement)

Ferranti F100-L (1976) ✓
    │   British military 16-bit
    │
    (Defense applications)

Ferranti ULA (1981) ✓
    │   Uncommitted Logic Array (ZX Spectrum)
    │
    (Custom gate array)

GI CP1600 (1975) ✓
    │   Intellivision game console CPU
    │   16-bit with 10-bit opcodes
    │
    (Gaming)

Panafacom MN1610 (1975) ✓
    │   First Japanese single-chip 16-bit
    │
    └──► Panafacom MN1613 (1977) ✓
            Enhanced with floating-point support
```

---

## Other Notable Lines

### Fairchild F8 (1975)

```
Fairchild F8 (1975) ✓
    │   Two-chip architecture (CPU + PSU)
    │
    ├──► Mostek 3870 (1977) ✓
    │       Single-chip F8 derivative
    │
    └──► Fairchild 9440 (1981) ✓
            16-bit processor (F8 team)
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

### Signetics Family

```
Signetics 2650 (1975) ✓
    │   Unique 8-bit architecture
    │
    (Limited success)

Signetics 8X300 (1976) ✓
    │   Bipolar signal processor
    │   Single-cycle execution
    │
    └──► Signetics 8X305 (1980) ✓
            Enhanced version
```

### WE / AT&T

```
WE 32000 (1984) ✓
    │   AT&T UNIX processor
    │
    (UNIX workstations)
```

### Clipper / Ridge / Apollo

```
Clipper C100 (1986) ✓
    │   Fairchild/Intergraph RISC
    │
    (Intergraph workstations)

Ridge 32 (1982) ✓
    │   Early RISC workstation processor
    │
    (Pre-dated commercial RISC)

Apollo DN300 (1988) ✓
    │   Apollo Computer workstation processor
    │
    (High-end CAD workstations)
```

### Xerox Alto (1973)

```
Xerox Alto (1973) ✓
    │   GUI pioneer, bit-slice construction
    │
    (Inspired Apple Macintosh, Windows)
```

### HP Calculator / Nano Line

```
HP Saturn (1984) ✓
    │   HP calculator processor (HP-48, HP-28)
    │   4-bit nibble architecture, 64-bit registers
    │
    (Scientific calculators)

HP Nano (1977) ✓
    │   HP calculator processor
    │
    (HP-01 wristwatch calculator)
```

### Sharp / Sanyo / Samsung

```
Sharp LH5801 (1981) ✓
    │   Sharp pocket computer CPU
    │
    (Calculator/pocket computer market)

Sharp SC61860 (1981) ✓
    │   Sharp pocket computer CPU (PC-1500)
    │
    (Programmable pocket computers)

Sanyo LC87 (1982) ✓
    │   4-bit MCU
    │
    └──► Sanyo LC88 (1984) ✓
            8-bit MCU

Samsung SM4 (1983) ✓
    │   4-bit MCU
    │
    └──► Samsung SM5 (1985) ✓
            Enhanced 4-bit

Samsung SM83 (1989) ✓
    │   8-bit MCU (Game Boy-like architecture)
    │
    (Nintendo Game Boy uses Sharp variant)

Samsung KS57 (1986) ✓
    │   4-bit MCU family
    │
    (Consumer electronics)

Samsung KS86C4004 (1990) ✓
    │   8-bit MCU
    │
    (Industrial / consumer)

Sharp LH0080 (1977) ✓
    │   Z80 clone (Sharp-manufactured)
    │
    (Second-source for Z80)
```

### OKI Sound/Speech/MCU

```
OKI MSM5205 (1983) ✓
    │   ADPCM speech synthesis
    │
    (Arcade and consumer)

OKI MSM5840 (1978) ✓
    │   4-bit MCU
    │
    (Consumer electronics)
```

### Intel Analog / Signal

```
Intel 2920 (1979) ✓
    │   Analog signal processor (earliest DSP concept)
    │
    (Signal processing pioneer)
```

### Japanese 16-Bit / Misc

```
Panafacom MN1800 (1982) ✓
    │   32-bit processor
    │
    (Japanese computing)

Matsushita/Panasonic MN1400 (1976) ✓
    │   4-bit MCU
    │
    (Consumer electronics)

Matsushita MN10200 (1993) ✓
    │   16/32-bit MCU
    │
    (Embedded systems)
```

### Siemens Family

```
Siemens SAB8080A (1976) ✓
    │   Licensed 8080 clone
    │
    └──► Siemens SAB8085 (1978) ✓
            Licensed 8085 clone

Siemens SAB80515 (1985) ✓
    │   Enhanced 8051 derivative
    │
    (Automotive and industrial)

Siemens SAB80C166 (1990) ✓
    │   16-bit MCU (C166 family)
    │
    (Automotive engine control)
```

### OKI 8085 Clones

```
OKI MSM80C85 (1981) ✓
    │   CMOS 8085 clone
    │
    └──► OKI MSM80C85AH (1983) ✓
            Enhanced CMOS 8085
```

### NEC 8080 Clone

```
NEC μPD8080AF (1976) ✓
    │   8080 clone
    │
    (Japanese second-source)
```

### AMD 8085 Clone

```
AMD AM8085A (1978) ✓
    │   AMD-manufactured 8085
    │
    (Second-source)
```

### WD Controller Line

```
WD2010 (1983) ✓
    │   Western Digital hard disk controller
    │
    (IDE/AT interface standard)
```

### Sequoia / Brooktree / LSI Logic / MAS

```
Sequoia S16 (1985) ✓
    │   16-bit processor
    │
    (Embedded systems)

Brooktree BT101 (1987) ✓
    │   Video DAC / pixel processor
    │
    (Display output)

LSI Logic L64801 (1988) ✓
    │   SPARC gate array implementation
    │
    (ASIC SPARC)

MAS281 (1985) ✓
    │   Processor
    │
    (Specialized computing)
```

### WISC Research Processors

```
WISC-16 (1983) ✓
    │   Wisconsin Integrally Synthesized Computer (16-bit)
    │
    └──► WISC-32 (1985) ✓
            32-bit version
```

### Chinese Processor

```
Chinese 863 (1990) ✓
    │   Chinese domestic processor (863 Program)
    │
    (National high-tech development)
```

### Cyrix Custom

```
Cyrix CX-1 (1989) ✓
    │   FPU coprocessor (387 competitor)
    │
    (Cyrix's first product)
```

### Rockwell / Renesas / Other MCU

```
Rockwell R6500/1 (1978) ✓
    │   6502-based single-chip MCU
    │
    (Low-cost embedded)

Renesas RP16 (1990) ✓ / RP32 (1992) ✓
    │   Renesas MCU family
    │
    (Industrial/automotive)
```

### MiPROC / MAC4 / MK5005

```
MiPROC (1984) ✓
    │   Custom/experimental processor
    │
    (Research)

MAC-4 (1985) ✓
    │   4-bit MCU/processor
    │
    (Specialized applications)

MK5005 (1978) ✓
    │   Mostek processor
    │
    (Telecommunications)
```

### Thomson / Williams

```
Thomson 90435 (1985) ✓
    │   French processor (Thomson-CSF)
    │
    (French defense/computing)

Williams SC1 (1988) ✓
    │   Williams arcade custom
    │
    (Narc, Smash TV)
```

---

## Cross-Pollination and Influence

```
                    ┌─────────────────────────────────────┐
                    │         INFLUENCE MAP               │
                    └─────────────────────────────────────┘

Intel 8080 ──────────────────────────► Zilog Z80 ──────► NEC μPD780
     │                                      │              ──► Z280 ──► Z380
     └──────────► NEC V20/V30 ◄────────────┘

Motorola 6800 ───────────────────────► MOS 6502 ──────► Ricoh 2A03
     │                                      │              (NES)
     │                                      ├──► MOS 6507 (Atari 2600)
     │                                      ├──► MOS 8501/8502 (C16/C128)
     └──► 6809 ──► Hitachi 6309            └──► WDC 65816 (SNES)
     └──► 68HC11 ──► 68HC16

Motorola 68000 ──► 68020 ──► 68030 ──► 68040 ──► 68060
     │              │                               (end of line)
     │              └──► CPU32 ──► ColdFire
     └──► 88100 ──► 88110 ──► (replaced by PowerPC)

Berkeley RISC I ──► RISC II ────────────► Sun SPARC ──► SuperSPARC
                                               │        ──► MicroSPARC
                    ARM1 ◄─────────────────────┘        ──► UltraSPARC
                      │
                      └──► ARM2 ──► ARM3 ──► ARM6 ──► ARM7TDMI
                                                        (Mobile revolution)

Stanford MIPS ──► R2000 ──► R3000 ──► R4000 ──► R4400/R4600/R8000/R10000
                                 │
                                 └──► Sony R3000A (PlayStation)
                                 └──► Toshiba TX39

IBM POWER1 ──► POWER2 ──► RS64
     │
     └──► PowerPC 601 ──► 603/604/620

DEC Alpha 21064 ──► 21064A / 21066

AMD Am2901 ──────────────────────────► Am2903, Am2910, Am29116, Am29C101
     │                                  TI SN74S481, MM6701
     └──► (Bit-slice computing era)

Rockwell PPS-4 ──────────────────────► PPS-4/1
     │
     └──► (Third microprocessor lineage)

Soviet Clones:
  8080 ──► KR580VM1, Tesla MHB8080A, U808, MCY7880
  Z80 ──► U880
  8086/8088 ──► K1810VM86/VM88
  PDP-11 ──► K1801VM1/VM2/VM3
  8051 ──► K580IK51
  Am2901 ──► KR581IK1/IK2
```

---

## Summary Statistics

| Family | Models in Collection | Year Range |
|--------|---------------------|------------|
| Intel (4-bit, 8-bit, MCU, x86, FPU, i960, peripheral) | 39 | 1971-1995 |
| Motorola (6800, 68k, 88k, DSP, embedded) | 32 | 1974-1994 |
| MOS/WDC 6502 family | 6 | 1975-1985 |
| Zilog (Z80, Z8, Z8000, peripherals) | 14 | 1976-1994 |
| ARM | 7 | 1985-1994 |
| AMD (bit-slice, RISC, x86, math, network) | 12 | 1975-1995 |
| NEC (4-bit, 8-bit, V-series, DSP) | 18 | 1972-1994 |
| TI (calculator, TMS9900, DSP, graphics, bit-slice) | 21 | 1970-1994 |
| Hitachi (6800-compat, display, SuperH, H8) | 13 | 1980-1994 |
| Fujitsu (arcade MCU, 6800, SPARC) | 8 | 1977-1992 |
| Toshiba (TLCS, MIPS) | 6 | 1978-1994 |
| Eastern Bloc (Soviet, DDR, Czech, Hungarian) | 22 | 1977-1991 |
| RCA COSMAC | 5 | 1976-1985 |
| National Semi (16-bit, 8-bit, NS32000, COP400) | 12 | 1973-1986 |
| Rockwell (PPS-4, 6502) | 5 | 1972-1983 |
| AMI (calculator, signal) | 6 | 1971-1980 |
| Mitsubishi (MELPS) | 6 | 1978-1985 |
| Namco (arcade custom) | 6 | 1980-1982 |
| MIPS (R2000-R10000) | 8 | 1983-1995 |
| SPARC (Sun, Fujitsu, Cypress, Ross, HAL) | 10 | 1982-1995 |
| HP PA-RISC | 4 | 1986-1994 |
| IBM POWER / PowerPC | 7 | 1990-1997 |
| DEC (Alpha, PDP-11 chip, VAX chip) | 6 | 1979-1994 |
| x86 Clones (Cyrix, IBM, UMC, Hyundai, NexGen) | 7 | 1992-1995 |
| Transputer / Parallel | 6 | 1972-1989 |
| DSP (AT&T, Analog Devices, Zoran, SGS, other) | 11 | 1980-1992 |
| Gaming / Sound / Graphics | 38 | 1976-1994 |
| LISP Machines | 3 | 1981-1987 |
| Stack Machines (Forth) | 4 | 1985-1994 |
| 16-Bit Pioneers | 8 | 1973-1981 |
| Japanese (Sharp, Panafacom, OKI, Samsung, Sanyo) | 17 | 1975-1993 |
| Siemens | 4 | 1976-1990 |
| Other (WE, Clipper, Ridge, Xerox, WISC, etc.) | 31 | 1973-1995 |
| **Total** | **467** | **1970-1997** |

---

**Document Version:** 3.0
**Last Updated:** January 30, 2026
**Processors Covered:** 467

✓ = Model included in collection
