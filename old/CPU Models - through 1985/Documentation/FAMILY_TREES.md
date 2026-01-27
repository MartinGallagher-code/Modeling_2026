# Microprocessor Family Trees

## Complete Lineage Diagrams for Major Processor Families

This document shows the evolutionary relationships between processors, including inheritance, compatibility, and architectural influences.

---

## Intel x86 Family

```
                        ┌─────────────────────────────────────────┐
                        │           INTEL x86 FAMILY              │
                        └─────────────────────────────────────────┘

    Intel 4004 (1971)                    Intel 8008 (1972)
    [First CPU]                          [First 8-bit]
         │                                    │
         ▼                                    ▼
    Intel 4040 (1974)                    Intel 8080 (1974)
    [+Interrupts]                        [Industry standard]
         │                                    │
         └─── 4-bit line ends                 ├────────────────────┐
                                              │                    │
                                              ▼                    ▼
                                        Intel 8085 (1976)    Zilog Z80 (1976)
                                        [Single supply]      [8080 compatible]
                                              │                    │
                              ┌───────────────┴───────┐           │
                              │                       │           │
                              ▼                       ▼           ▼
                        Intel 8086 (1978)      Intel 8088 (1979)  Z180, Z280
                        [16-bit]               [8-bit bus]        [Enhanced Z80]
                              │                       │
                              │         ┌─────────────┤
                              │         │             │
                              ▼         ▼             ▼
                        Intel 80186   Intel 80188   IBM PC (1981)
                        [Integrated]  [8-bit bus]   [8088-based]
                              │                       │
                              └───────────┬───────────┘
                                          │
                                          ▼
                                    Intel 80286 (1982)
                                    [Protected mode]
                                          │
                                          ▼
                                    Intel 80386 (1985) ──────► Modern x86/x64
                                    [32-bit, paging]          [Your PC today]

    CLONES & COMPATIBLES:
    ┌─────────────────────────────────────────────────────────────────┐
    │ NEC V20 (1984) ──► 8088 compatible, faster, 8080 mode          │
    │ NEC V30 (1984) ──► 8086 compatible, faster, 8080 mode          │
    │ AMD 8086/8088  ──► Second source                                │
    │ AMD 80286      ──► Second source                                │
    │ AMD 80386      ──► Beginning of AMD vs Intel                    │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Intel MCS-48/51 MCU Family

```
                        ┌─────────────────────────────────────────┐
                        │        INTEL MCU FAMILIES               │
                        └─────────────────────────────────────────┘

                              MCS-48 Family (1976)
                        ┌─────────────┴─────────────┐
                        │                           │
                   ROM versions              ROM-less versions
                        │                           │
              ┌─────────┼─────────┐        ┌───────┼───────┐
              │         │         │        │       │       │
              ▼         ▼         ▼        ▼       ▼       ▼
           8048      8049      8050     8035    8039    8040
           [1K]      [2K]      [4K]    [none]  [none]  [none]
              │
              │ Evolution
              ▼
                              MCS-51 Family (1980)
                        ┌─────────────┴─────────────┐
                        │                           │
                   ROM versions              ROM-less versions
                        │                           │
              ┌─────────┼─────────┐                 │
              │         │         │                 ▼
              ▼         ▼         ▼              8031/8032
           8051      8052      8751             [ROM-less]
           [4K]      [8K]    [EPROM]
              │
              │ Still manufactured today!
              ▼
         Modern 8051 derivatives (2026)
         [Billions in use]


                              MCS-96 Family (1982)
                                    │
                              ┌─────┴─────┐
                              │           │
                              ▼           ▼
                           8096        8097/8098
                        [Flagship]    [Variants]
                              │
                              ▼
                          80196 (1987)
                        [Enhanced]
                              │
                              ▼
                    Automotive Standard
                    [Dominated 1985-2005]
```

---

## Motorola 6800/68000 Families

```
                        ┌─────────────────────────────────────────┐
                        │         MOTOROLA FAMILIES               │
                        └─────────────────────────────────────────┘

                           Motorola 6800 (1974)
                           [First Motorola µP]
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    CPU Variants              MCU Family                Enhanced CPU
           │                        │                        │
    ┌──────┴──────┐         ┌──────┴──────┐                 │
    │             │         │             │                 │
    ▼             ▼         ▼             ▼                 ▼
  6802          6808      6801          6803             6809 (1979)
[+128B RAM]   [4 MHz]   [+ROM+I/O]   [ROM-less]        [Best 8-bit]
                              │                             │
                              ▼                             │
                           6805 (1979)                      │
                        [Low-cost MCU]                      │
                              │                             │
                              ▼                             ▼
                    HC05, HC08, HCS08              Hitachi 6309 (1982)
                    [Modern derivatives]          [Enhanced 6809]


                           Motorola 68000 (1979)
                           [16/32-bit hybrid]
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
        68008                    68010                    68020 (1984)
     [8-bit bus]            [Virtual memory]           [True 32-bit]
                                                            │
    PLATFORMS:                                              ▼
    ┌─────────────────────────────────────┐           68030, 68040
    │ Macintosh (1984)     ──► 68000      │           [Cached, MMU]
    │ Amiga (1985)         ──► 68000      │                │
    │ Atari ST (1985)      ──► 68000      │                ▼
    │ Sun Workstations     ──► 68020+     │           ColdFire
    │ Sega Genesis (1988)  ──► 68000      │           [Modern derivative]
    └─────────────────────────────────────┘
```

---

## MOS 6502 / WDC Family

```
                        ┌─────────────────────────────────────────┐
                        │           6502 FAMILY                   │
                        └─────────────────────────────────────────┘

                        MOS Technology 6502 (1975)
                              [$25 revolution]
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       │                            │                            │
       ▼                            ▼                            ▼
  Second Sources              WDC Evolution                Platform Uses
       │                            │                            │
 ┌─────┴─────┐              ┌──────┴──────┐              ┌──────┴──────┐
 │           │              │             │              │             │
 ▼           ▼              ▼             ▼              ▼             ▼
Rockwell   Synertek     65C02 (1983)  65816 (1984)  Apple II    NES (1983)
  │           │         [CMOS, new    [16-bit]      (1977)      [6502]
  │           │          instructions] [Apple IIGS]  [6502]         │
  ▼           │              │         [SNES]           │           │
R6511      SY6502           │             │             │           │
[+UART]                     │             │             │           │
                            ▼             │             ▼           │
                       65802 (1984)       │        Commodore 64     │
                       [65816 in          │        (1982)           │
                        40-pin!]          │        [6510]           │
                                          │             │           │
                                          ▼             ▼           ▼
                                    Still manufactured      Atari 2600
                                    by WDC today!           (1977)
                                                            [6507]

    INFLUENCE:
    ┌─────────────────────────────────────────────────────────────────┐
    │ The 6502's low price ($25 vs $150 for 8080) enabled:           │
    │   • Apple II (launched Apple Computer)                          │
    │   • Commodore PET, VIC-20, C64 (best-selling computer ever)    │
    │   • Atari 2600, 400/800 (gaming revolution)                    │
    │   • Nintendo NES (saved video game industry)                    │
    │   • BBC Micro (UK computing education)                          │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Zilog Family

```
                        ┌─────────────────────────────────────────┐
                        │           ZILOG FAMILY                  │
                        └─────────────────────────────────────────┘

                        Intel 8080 (1974)
                              │
                              │ Federico Faggin leaves Intel,
                              │ founds Zilog
                              ▼
                        Zilog Z80 (1976)
                        [8080 superset]
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
    Z180 (1985)          Z280 (1985)           NSC800 (1979)
    [Enhanced Z80]       [Failed successor]    [CMOS clone]
    [+MMU, +DMA]         [Not compatible]      [National Semi]
       │                      │
       ▼                      ▼
    eZ80 (2001)          (Discontinued)
    [Still made]


                        Zilog Z8 (1979)
                        [8-bit MCU]
                              │
                              ▼
                        Z8 Encore!
                        [Modern derivative]


                        Zilog Z8000 (1979)
                        [16-bit CPU]
                              │
                              ▼
                        (Limited success)


    PLATFORMS:
    ┌─────────────────────────────────────────────────────────────────┐
    │ CP/M (1977)          ──► Z80 became THE CP/M processor         │
    │ TRS-80 (1977)        ──► First successful Z80 computer         │
    │ MSX (1983)           ──► Japanese standard, Z80-based          │
    │ ZX Spectrum (1982)   ──► UK home computer phenomenon           │
    │ Game Boy (1989)      ──► Sharp Z80 derivative                  │
    │ TI-83/84 (1996+)     ──► Still using Z80 today!                │
    └─────────────────────────────────────────────────────────────────┘
```

---

## RCA COSMAC Family

```
                        ┌─────────────────────────────────────────┐
                        │         RCA COSMAC FAMILY               │
                        │      (Radiation-Hardened)               │
                        └─────────────────────────────────────────┘

                        CDP1802 (1976)
                        [Original COSMAC]
                        [Voyager 1 & 2]
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
      CDP1804 (1980)    CDP1805 (1984)    CDP1806 (1985)
      [+64B RAM]        [+Instructions]   [128B RAM]
      [+Timer]          [New Horizons]    [Final COSMAC]
                              │
                              │
    CORPORATE OWNERSHIP:      │
    ┌─────────────────────────┴─────────────────────────────────────┐
    │ RCA (1976) ► GE (1986) ► Harris (1988) ► Intersil ► Renesas   │
    │                                                                │
    │ COSMAC chips are STILL MANUFACTURED for space/military!       │
    └────────────────────────────────────────────────────────────────┘

    SPACE HERITAGE:
    ┌─────────────────────────────────────────────────────────────────┐
    │ Voyager 1 (1977)    ──► CDP1802, still running at 15B+ miles!  │
    │ Voyager 2 (1977)    ──► CDP1802, still running at 12B+ miles!  │
    │ Galileo (1989)      ──► CDP1802, Jupiter mission               │
    │ Hubble (1990)       ──► COSMAC derivatives                     │
    │ New Horizons (2006) ──► CDP1805, Pluto flyby, 8B+ km away      │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Texas Instruments Family

```
                        ┌─────────────────────────────────────────┐
                        │      TEXAS INSTRUMENTS FAMILY           │
                        └─────────────────────────────────────────┘

                    TMS1000 (1974)                TMS9900 (1976)
                    [First mass MCU]              [16-bit CPU]
                    [Billions shipped]            [Workspace arch]
                          │                             │
          ┌───────────────┤                             │
          │               │                             │
          ▼               ▼                             ▼
       TMS1100         TMS1200                    TMS9995 (1981)
       [2K ROM]        [Better I/O]               [Enhanced]
          │                                             │
          │                                             │
    PRODUCTS:                                     TI-99/4A (1981)
    ┌──────────────────────────┐                 [Home computer]
    │ Speak & Spell (1978)     │
    │ TI-30 Calculator         │
    │ Simon game               │                 TMS7000 (1981)
    │ Countless appliances     │                 [8-bit MCU]
    └──────────────────────────┘                 [Competed with 8051]
                                                       │
                                                       ▼
                                                 TMS370
                                                 [Continued line]

    LESSON LEARNED:
    ┌─────────────────────────────────────────────────────────────────┐
    │ TMS7000 had better architecture than 8051                       │
    │ But 8051 had better ecosystem (tools, community, second sources)│
    │ ECOSYSTEM > ARCHITECTURE                                        │
    └─────────────────────────────────────────────────────────────────┘
```

---

## RISC Pioneers

```
                        ┌─────────────────────────────────────────┐
                        │         RISC PIONEERS (1985)            │
                        └─────────────────────────────────────────┘

                    Berkeley RISC               Stanford MIPS
                    Research (1980)             Research (1981)
                          │                           │
                          ▼                           ▼
                    ARM1 (1985)               MIPS R2000 (1985)
                    [Acorn RISC Machine]      [Commercial MIPS]
                    [25,000 transistors]      [110,000 transistors]
                          │                           │
                          │                           │
                          ▼                           ▼
                    ARM2, ARM3...             R3000, R4000...
                          │                           │
                          ▼                           ▼
                    ARM Cortex (2004+)        (Acquired by various)
                          │                           │
                          ▼                           │
                    200+ BILLION               PlayStation, N64,
                    chips shipped              Networking equipment


    THE RISC INSIGHT:
    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │  CISC approach: Complex instructions, slow clock                │
    │  RISC approach: Simple instructions, fast clock, pipeline      │
    │                                                                 │
    │  ARM1 (1985): 25,000 transistors, outperformed 80286!          │
    │               Simple = Fast = Low Power                         │
    │                                                                 │
    │  Today: ARM dominates mobile/embedded                           │
    │         RISC-V emerging as open alternative                     │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
```

---

## Cross-Family Influences

```
    ARCHITECTURAL INFLUENCES:
    
    PDP-11 (1970) ────────────────────┐
    [DEC minicomputer]                │
           │                          │
           │ Influenced               │
           ▼                          ▼
    Motorola 68000              Intersil 6100
    [Linear address space]      [PDP-8 on chip]
    [Orthogonal instruction set]


    IBM System/360 (1964) ────────────┐
    [Mainframe]                       │
           │                          │
           │ Influenced               │
           ▼                          ▼
    Intel iAPX 432              TI TMS9900
    [Capability-based]          [Workspace concept]


    6800 (1974) ──────────────────────┐
           │                          │
           │ Designers left to MOS    │
           ▼                          │
    6502 (1975) ◄─────────────────────┘
    [Simplified 6800 concepts]
    [Added zero-page, cheaper]
```

---

## Compatibility Relationships

```
    BINARY COMPATIBLE:
    ┌─────────────────────────────────────────────────────────────────┐
    │ 8080 ──► Z80 (Z80 runs all 8080 code)                          │
    │ 8086 ──► 80286 ──► 80386 (x86 compatibility chain)             │
    │ 6502 ──► 65C02 ──► 65816 (in emulation mode)                   │
    │ 68000 ──► 68010 ──► 68020 (68k family)                         │
    │ 1802 ──► 1804 ──► 1805 ──► 1806 (COSMAC family)                │
    └─────────────────────────────────────────────────────────────────┘

    PIN COMPATIBLE (Drop-in replacements):
    ┌─────────────────────────────────────────────────────────────────┐
    │ 8088 ◄──► V20 (faster, same socket)                            │
    │ 8086 ◄──► V30 (faster, same socket)                            │
    │ 6502 ◄──► 65802 (16-bit in 8-bit socket!)                      │
    │ Z80 ◄──► NSC800 (CMOS version)                                 │
    └─────────────────────────────────────────────────────────────────┘

    INSTRUCTION SET EMULATION:
    ┌─────────────────────────────────────────────────────────────────┐
    │ V20/V30 can switch to 8080 mode                                │
    │ 65816 can switch to 6502 emulation mode                        │
    │ 80386 can run 8086 code in virtual 8086 mode                   │
    └─────────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0  
**Last Updated:** January 25, 2026
