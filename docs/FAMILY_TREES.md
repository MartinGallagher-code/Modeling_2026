# Microprocessor Family Trees

## Processor Lineages and Relationships (1971-1994)

This document traces the evolutionary relationships between processors in the collection, showing how architectures developed and influenced each other.

---

## Intel Family Tree

### 4-Bit Line (1971-1974)

```
Intel 4004 (1971)
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
            └──► NEC μPD780 (1976)                                │
                    Z80 clone for Japanese market                  │
                                                                   │
    ┌──────────────────────────────────────────────────────────────┘
    │
    └──► Z80A (1976) ✓ ──► Z80B (1978) ✓ ──► Z180 (1985) ✓
            4 MHz            6 MHz            Enhanced + MMU
```

### MCS-48 MCU Line (1976-1980)

```
Intel 8048 (1976) ✓
    │   First successful single-chip MCU
    │
    ├──► Intel 8035 ──► Intel 8039
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

### x86 Line (1978-1993)

```
Intel 8086 (1978) ✓
    │   16-bit, segmented memory, x86 origin
    │
    ├──► Intel 8088 (1979) ✓
    │       │   8-bit bus version, IBM PC
    │       │
    │       └──► NEC V20 (1984) ✓
    │               Pin-compatible, 15% faster, 8080 mode
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
    │       └──► Hitachi HD6301
    │               Enhanced clone
    │
    ├──► Motorola 6805 (1979) ✓
    │       │   Low-cost MCU, simplified ISA
    │       │
    │       └──► Motorola 68HC05 (1984)
    │               CMOS version
    │
    ├──► Motorola 6809 (1979) ✓
    │       │   "Best 8-bit ever" - position-independent code
    │       │
    │       └──► Hitachi 6309 (1982)
    │               Enhanced 6809 with extra registers
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
    ├──► MOS 6507 (1975)
    │       Reduced pins (28), Atari 2600
    │
    ├──► MOS 6509 (1980)
    │       Bank switching, CBM-II
    │
    ├──► MOS 6510 (1982) ✓
    │       6502 + I/O port, Commodore 64
    │
    ├──► Ricoh 2A03 (1983)
    │       6502 + audio, no BCD, NES/Famicom
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
    ├──► RCA CDP1804 (1980)
    │       On-chip RAM, timer
    │
    ├──► RCA CDP1805 (1984) ✓
    │       Enhanced, New Horizons mission
    │
    └──► RCA CDP1806 (1985)
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
    │   TI-99/4A home computer
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
    └──► Berkeley RISC II (1983)
            │   Improved version
            │
            └──► Sun SPARC (1987) ✓
                    Commercial RISC from Berkeley research

Stanford MIPS (1983)
    │   Academic MIPS prototype
    │
    └──► MIPS R2000 (1985) ✓
            │   Commercial 5-stage pipeline
            │
            └──► (R3000, R4000, R10000...)

HP PA-RISC (1986) ✓
    │   HP workstation RISC
    │
    └──► (PA-7000, PA-8000...)
```

---

## Other Notable Lines

### Fairchild F8 (1975)

```
Fairchild F8 (1975) ✓
    │   Two-chip architecture (CPU + PSU)
    │
    └──► Mostek 3870 (1977)
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
            Improved version
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
    └──► Harris HM6100 (1978)
            Faster version
```

### Workstation/Server

```
DEC Alpha 21064 (1992) ✓
    │   64-bit, fastest of its era
    │
    └──► (21164, 21264...)

AIM PowerPC 601 (1993) ✓
    │   Apple/IBM/Motorola alliance
    │
    └──► (603, 604, G3, G4, G5...)
```

---

## Cross-Pollination and Influence

```
                    ┌─────────────────────────────────────┐
                    │         INFLUENCE MAP               │
                    └─────────────────────────────────────┘

Intel 8080 ──────────────────────────► Zilog Z80
     │                                      │
     └──────────► NEC V20/V30 ◄────────────┘

Motorola 6800 ───────────────────────► MOS 6502
                                           │
                                           └──► WDC 65816

Berkeley RISC I ─────────────────────► Sun SPARC
                                           │
                    ARM1 ◄─────────────────┘
                      │
                      └──────────────► (Mobile revolution)

Stanford MIPS ───────────────────────► MIPS R2000
                                           │
                                           └──► (PS1, N64, routers)
```

---

## Summary Statistics

| Family | Models in Collection | Year Range |
|--------|---------------------|------------|
| Intel x86 | 12 | 1978-1993 |
| Intel 8-bit | 5 | 1972-1976 |
| Intel MCU | 4 | 1976-1980 |
| Motorola 68k | 7 | 1979-1994 |
| Motorola 6800 | 6 | 1974-1985 |
| MOS/WDC 6502 | 4 | 1975-1984 |
| Zilog | 7 | 1976-1986 |
| ARM | 4 | 1985-1991 |
| RISC Pioneers | 5 | 1982-1987 |
| TI | 4 | 1974-1982 |
| Other | 22 | 1974-1993 |
| **Total** | **80** | **1971-1994** |

---

**Document Version:** 1.0
**Last Updated:** January 29, 2026
**Processors Covered:** 80

✓ = Model included in collection
