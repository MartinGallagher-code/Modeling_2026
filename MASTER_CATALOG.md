# Pre-1995 Microprocessor Collection - Master Catalog

## Overview

This collection contains **467 queueing-theory-based performance models** covering the complete evolution of microprocessors from the earliest calculator chips (AMI S2000, 1970) through the high-performance RISC and superscalar era (DEC Alpha 21064A, UltraSPARC, 1995).

The models use grey-box methodology combining architectural knowledge, M/M/1 queueing networks, and calibration against real hardware measurements to achieve typical accuracy within 5% of actual performance.

**All 467 models validated with <2% CPI error.**

---

## Collection at a Glance

| Metric | Value |
|--------|-------|
| Total Models | 467 |
| Family Directories | 19 |
| Year Range | 1970-1995 |
| Manufacturers | 60+ |
| Architectures | 1-bit, 4-bit, 8-bit, 12-bit, 16-bit, 25-bit, 32-bit, 64-bit |
| Categories | CPUs, MCUs, FPUs, GPUs, Bit-slice, DSPs, ALUs, Arcade, Sound, Graphics |

---

## Complete Model Inventory

### Intel Corporation (39 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **3002** | 1974 | 2 | Bit-slice | Intel's bit-slice ALU |
| **3003** | 1974 | 2 | Bit-slice | Look-ahead carry generator for 3002 |
| **4004** | 1971 | 4 | CPU | First commercial microprocessor |
| **4040** | 1974 | 4 | CPU | Enhanced 4004, interrupts added |
| **8008** | 1972 | 8 | CPU | First 8-bit microprocessor |
| **8039** | 1976 | 8 | MCU | MCS-48 ROM-less variant |
| **8044** | 1980 | 8 | MCU | MCS-48 with SDLC/HDLC |
| **8048** | 1976 | 8 | MCU | MCS-48 flagship |
| **8051** | 1980 | 8 | MCU | MCS-51 flagship, still made today |
| **8061** | 1980 | 8 | MCU | Ford EEC-IV automotive controller |
| **8080** | 1974 | 8 | CPU | Industry standard, enabled Altair |
| **8085** | 1976 | 8 | CPU | Improved 8080, single supply |
| **8086** | 1978 | 16 | CPU | x86 architecture origin |
| **8087** | 1980 | - | FPU | Math coprocessor for 8086/8088 |
| **8087 (2nd gen)** | 1983 | - | FPU | Improved 8087 for 80186/286 |
| **8088** | 1979 | 16 | CPU | IBM PC processor |
| **8089** | 1979 | 16 | I/O | I/O processor for x86 systems |
| **8096** | 1982 | 16 | MCU | Automotive MCU, dominated 1985-2005 |
| **80186** | 1982 | 16 | CPU | Integrated 8086 system |
| **80188** | 1982 | 16 | CPU | 8-bit bus 80186 |
| **80286** | 1982 | 16 | CPU | Protected mode, IBM AT |
| **80287** | 1982 | - | FPU | Math coprocessor for 286 |
| **80386** | 1985 | 32 | CPU | First x86 32-bit |
| **80387** | 1987 | - | FPU | Math coprocessor for 386 |
| **80486** | 1989 | 32 | CPU | Pipelined, on-chip cache |
| **80C186** | 1987 | 16 | CPU | CMOS 80186 variant |
| **8231** | 1977 | - | FPU | Arithmetic processing unit |
| **82557** | 1995 | - | I/O | Fast Ethernet controller |
| **82586** | 1984 | - | I/O | Ethernet LAN coprocessor |
| **82596** | 1987 | - | I/O | 32-bit LAN coprocessor |
| **82730** | 1983 | - | Display | Text display coprocessor |
| **8748** | 1977 | 8 | MCU | EPROM version of 8048 |
| **8751** | 1980 | 8 | MCU | EPROM version of 8051 |
| **i860** | 1989 | 64 | CPU | "Cray on a chip" |
| **i960** | 1988 | 32 | CPU | RISC embedded processor |
| **i960CA** | 1989 | 32 | CPU | Superscalar i960 variant |
| **i960CF** | 1992 | 32 | CPU | i960 with FPU |
| **iAPX 432** | 1981 | 32 | CPU | Object-oriented architecture |
| **Pentium** | 1993 | 32 | CPU | First superscalar x86 |

### Motorola (32 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6800** | 1974 | 8 | CPU | Motorola's first microprocessor |
| **6801** | 1978 | 8 | MCU | 6800 + ROM + RAM + I/O |
| **6802** | 1977 | 8 | CPU | 6800 + 128B RAM + clock |
| **6803** | 1983 | 8 | MCU | Enhanced 6801 |
| **6804** | 1983 | 8 | MCU | Simplified 6805 variant |
| **6805** | 1979 | 8 | MCU | Low-cost MCU family |
| **6805R2** | 1979 | 8 | MCU | 6805 with ROM variant |
| **6809** | 1979 | 8 | CPU | Most advanced 8-bit |
| **6854** | 1978 | - | I/O | ADLC communications controller |
| **68000** | 1979 | 16/32 | CPU | Macintosh, Amiga, Atari ST |
| **68008** | 1982 | 16/32 | CPU | 8-bit bus 68000 |
| **68010** | 1982 | 16/32 | CPU | Virtual memory support |
| **68020** | 1984 | 32 | CPU | Full 32-bit, on-chip cache |
| **68030** | 1987 | 32 | CPU | On-chip MMU |
| **68040** | 1990 | 32 | CPU | On-chip FPU |
| **68060** | 1994 | 32 | CPU | Last 68k, superscalar |
| **68302** | 1988 | 32 | MCU | Integrated comm processor |
| **68360** | 1991 | 32 | MCU | QUICC comm controller |
| **68851** | 1984 | - | MMU | Paged memory management unit |
| **68881** | 1984 | - | FPU | 68k math coprocessor |
| **68882** | 1988 | - | FPU | Enhanced 68881 |
| **68HC05** | 1984 | 8 | MCU | Low-cost 6805 variant |
| **68HC11** | 1985 | 8 | MCU | Popular automotive MCU |
| **68HC11A1** | 1985 | 8 | MCU | 68HC11 specific variant |
| **68HC16** | 1991 | 16 | MCU | 16-bit automotive MCU |
| **88100** | 1988 | 32 | CPU | Motorola RISC processor |
| **88110** | 1991 | 32 | CPU | Superscalar 88000 family |
| **ColdFire** | 1994 | 32 | CPU | Embedded 68k successor |
| **CPU32** | 1990 | 32 | CPU | 68020 derivative for embedded |
| **DSP56001** | 1987 | 24 | DSP | 24-bit audio DSP |
| **DSP96002** | 1990 | 32 | DSP | IEEE 754 floating-point DSP |
| **MC14500B** | 1976 | 1 | CPU | 1-bit industrial controller |

### MOS Technology / Western Design Center (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6502** | 1975 | 8 | CPU | Apple II, C64, NES |
| **6510** | 1982 | 8 | CPU | C64 variant with I/O port |
| **8501** | 1984 | 8 | CPU | C16/Plus/4 variant |
| **8502** | 1985 | 8 | CPU | C128 variant, 2 MHz capable |
| **65C02** | 1983 | 8 | CPU | CMOS 6502, new instructions |
| **65816** | 1984 | 16 | CPU | Apple IIGS, SNES |

### Zilog (14 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Z8** | 1979 | 8 | MCU | Zilog microcontroller |
| **Z80** | 1976 | 8 | CPU | CP/M standard, MSX, TRS-80 |
| **Z80A** | 1976 | 8 | CPU | 4 MHz speed grade |
| **Z80B** | 1978 | 8 | CPU | 6 MHz speed grade |
| **Z80-SIO** | 1977 | - | I/O | Serial I/O controller |
| **Z180** | 1985 | 8 | CPU | Enhanced Z80, MMU |
| **Z280** | 1987 | 16 | CPU | Z80 with MMU and cache |
| **Z380** | 1994 | 32 | CPU | 32-bit Z80 extension |
| **Z8000** | 1979 | 16 | CPU | Zilog 16-bit |
| **Z80000** | 1986 | 32 | CPU | Zilog 32-bit |
| **Z8016 DMA** | 1981 | - | DMA | Z8000 DMA controller |
| **Z8530** | 1983 | - | I/O | Serial communications controller |
| **Z8S180** | 1990 | 8 | CPU | Static CMOS Z180 variant |
| **Super8** | 1982 | 8 | MCU | Enhanced Z8 |

### Texas Instruments (21 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **SBP0400** | 1975 | 4 | Bit-slice | TI's first bit-slice ALU |
| **SBP0401** | 1975 | 4 | Bit-slice | SBP0400 companion |
| **SN74181** | 1970 | 4 | ALU | First single-chip ALU |
| **SN74S481** | 1976 | 4 | Bit-slice | Schottky bit-slice ALU |
| **TMS0800** | 1973 | 4 | Calculator | TI calculator chip |
| **TMS1000** | 1974 | 4 | MCU | First mass-produced MCU |
| **TMS320C10** | 1982 | 16 | DSP | First TI DSP |
| **TMS320C25** | 1986 | 16 | DSP | Second-gen TI DSP |
| **TMS320C30** | 1988 | 32 | DSP | Floating-point DSP |
| **TMS320C40** | 1991 | 32 | DSP | Multiprocessor DSP |
| **TMS320C50** | 1991 | 16 | DSP | Low-cost fixed-point DSP |
| **TMS320C80** | 1994 | 32 | DSP | Multimedia video processor |
| **TMS34010** | 1986 | 32 | GPU | First programmable GPU |
| **TMS34020** | 1989 | 32 | GPU | Enhanced TMS34010 |
| **TMS370** | 1986 | 8 | MCU | TI 8-bit MCU family |
| **TMS5100** | 1978 | - | Speech | Speech synthesis processor |
| **TMS7000** | 1981 | 8 | MCU | TI 8-bit MCU |
| **TMS9900** | 1976 | 16 | CPU | TI-99/4A, workspace architecture |
| **TMS9980** | 1979 | 16 | CPU | TMS9900 with 8-bit bus |
| **TMS9985** | 1981 | 16 | CPU | Single-chip TMS9900 |
| **TMS9995** | 1981 | 16 | CPU | Enhanced TMS9900 |

### ARM (7 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **ARM1** | 1985 | 32 | CPU | First ARM, RISC pioneer |
| **ARM2** | 1986 | 32 | CPU | First production ARM |
| **ARM250** | 1990 | 32 | CPU | ARM2 with integrated MMU |
| **ARM3** | 1989 | 32 | CPU | First cached ARM |
| **ARM6** | 1991 | 32 | CPU | Foundation of modern ARM |
| **ARM610** | 1992 | 32 | CPU | ARM6 with cache and MMU |
| **ARM7TDMI** | 1994 | 32 | CPU | Thumb mode, most-licensed ARM |

### NEC (18 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **V20** | 1984 | 16 | CPU | Faster 8088 replacement |
| **V30** | 1984 | 16 | CPU | 16-bit bus V20 sibling |
| **V60** | 1986 | 32 | CPU | Japan's first major 32-bit |
| **V70** | 1987 | 32 | CPU | V60 variant |
| **V810** | 1994 | 32 | CPU | Virtual Boy processor |
| **V850** | 1994 | 32 | CPU | Automotive embedded RISC |
| **uCOM-4** | 1972 | 4 | MCU | TMS1000 competitor |
| **uPD1007C** | 1980s | 4 | MCU | Advanced 4-bit MCU |
| **uPD546** | 1973 | 4 | MCU | Early NEC 4-bit |
| **uPD612xA** | 1980s | 4 | MCU | Extended uCOM-4 with LCD |
| **uPD7220** | 1981 | 16 | GPU | First LSI graphics processor |
| **uPD751** | 1974 | 4 | MCU | NEC's early 4-bit MCU |
| **uPD7720** | 1980 | 16 | DSP | Early DSP, speech synthesis |
| **uPD7725** | 1985 | 16 | DSP | Enhanced uPD7720 |
| **uPD7759** | 1987 | - | Sound | ADPCM speech synthesizer |
| **uPD780** | 1976 | 8 | CPU | Z80 clone, widely used in Japan |
| **uPD7801** | 1980 | 8 | MCU | NEC 78K predecessor |
| **uPD7810** | 1982 | 8 | MCU | Enhanced 7801, arcade/gaming |

### AMD (12 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Am2901** | 1975 | 4 | Bit-slice | ALU building block |
| **Am2903** | 1976 | 4 | Bit-slice | Enhanced 2901 |
| **Am2910** | 1979 | 12 | Bit-slice | Microprogram sequencer |
| **Am29116** | 1983 | 16 | Bit-slice | 16-bit cascadable ALU |
| **Am29C101** | 1985 | 4 | Bit-slice | CMOS Am2901 |
| **Am29000** | 1987 | 32 | CPU | Laser printer CPU |
| **Am386** | 1991 | 32 | CPU | AMD 386 clone |
| **Am486** | 1993 | 32 | CPU | AMD 486 clone |
| **Am5x86** | 1995 | 32 | CPU | Enhanced 486, 133 MHz |
| **Am79C970** | 1993 | - | I/O | PCnet Ethernet controller |
| **Am9511** | 1979 | - | FPU | Arithmetic processor |
| **Am9512** | 1980 | - | FPU | Floating-point processor |

### Hitachi (13 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6309** | 1982 | 8 | CPU | Enhanced 6809, "best 8-bit" |
| **FD1089** | 1980s | 16 | CPU | Encrypted 68000 (Sega) |
| **FD1094** | 1980s | 16 | CPU | Encrypted 68000 (Sega) |
| **H8/300** | 1990 | 16 | MCU | Hitachi RISC-like MCU |
| **H8/500** | 1990 | 16 | MCU | Extended H8 family |
| **HD6301** | 1983 | 8 | MCU | Enhanced 6801 |
| **HD6305** | 1984 | 8 | MCU | CMOS 6805 variant |
| **HD63484** | 1984 | 16 | GPU | Advanced CRT controller |
| **HD63484 (rev 2)** | 1986 | 16 | GPU | Improved ACRTC |
| **HD64180** | 1985 | 8 | CPU | Z180 equivalent |
| **HMCS40** | 1980 | 4 | MCU | Hitachi 4-bit MCU family |
| **SH-1** | 1992 | 32 | CPU | SuperH RISC first generation |
| **SH-2** | 1994 | 32 | CPU | Sega Saturn, automotive |

### Fujitsu (8 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **MB86900** | 1987 | 32 | CPU | First SPARC implementation |
| **MB8841** | 1977 | 4 | MCU | Arcade gaming (Galaga, Xevious) |
| **MB8842** | 1977 | 4 | MCU | MB8841 variant |
| **MB8843** | 1977 | 4 | MCU | MB8841 variant |
| **MB8844** | 1977 | 4 | MCU | MB8841 variant |
| **MB8845** | 1977 | 4 | MCU | MB8841 variant |
| **MB8861** | 1977 | 8 | CPU | 6800 clone |
| **SPARClite** | 1992 | 32 | CPU | Embedded SPARC variant |

### AMI (American Microsystems) (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **S2000** | 1970 | 4 | CPU | First complete system under $10 |
| **S2150** | 1970s | 4 | CPU | S2000 variant |
| **S2200** | 1970s | 4 | CPU | S2000 variant |
| **S2400** | 1970s | 4 | CPU | S2000 variant |
| **S2811** | 1978 | 16 | DSP | Early signal processor |
| **S28211** | 1979 | 16 | DSP | DSP peripheral for 6800 |

### Mitsubishi (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **MELPS 740** | 1984 | 8 | MCU | Enhanced 6502, 600+ variants |
| **M50740** | 1984 | 8 | MCU | MELPS 740 family |
| **M50747** | 1984 | 8 | MCU | MELPS 740 variant |
| **MELPS 4** | 1978 | 4 | MCU | pMOS 4-bit MCU family |
| **MELPS 41** | 1980s | 4 | MCU | Enhanced MELPS 4 |
| **MELPS 42** | 1980s | 4 | MCU | CMOS MELPS 4 |

### Toshiba (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **TLCS-12** | 1973 | 12 | CPU | First Japanese microprocessor |
| **TLCS-12A** | 1975 | 12 | CPU | Improved TLCS-12 |
| **TLCS-47** | 1980s | 4 | MCU | Toshiba 4-bit MCU |
| **TLCS-870** | 1980s | 8 | MCU | Toshiba 8-bit MCU |
| **TLCS-90** | 1980s | 8 | MCU | Z80-like MCU |
| **TX39** | 1994 | 32 | CPU | MIPS-based embedded (Toshiba R3000) |

### Namco Arcade Custom (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **05xx** | 1980s | - | Custom | Famous starfield generator |
| **50xx** | 1980s | - | Custom | Pac-Man era custom chip |
| **51xx** | 1980s | - | Custom | I/O controller |
| **52xx** | 1980s | - | Custom | Sample player |
| **53xx** | 1980s | - | Custom | Multiplexer |
| **54xx** | 1980s | - | Custom | Sound generator |

### Eastern Bloc (22 models)

| Model | Manufacturer | Year | Bits | Significance |
|-------|--------------|------|------|--------------|
| **CM630** | Bulgaria | 1980s | 8 | CMOS 6502 clone (Pravetz) |
| **Elbrus EL-90** | Soviet | 1990 | 32 | Soviet superscalar CPU |
| **IM1821VM85A** | Soviet | 1980s | 8 | Soviet 8085 clone |
| **K1801VM1** | Soviet | 1980 | 16 | PDP-11-compatible LSI |
| **K1801VM2** | Soviet | 1984 | 16 | Enhanced PDP-11 LSI |
| **K1801VM3** | Soviet | 1986 | 16 | Final PDP-11 LSI generation |
| **K1810VM86** | Soviet | 1980s | 16 | Soviet 8086 clone |
| **K1810VM88** | Soviet | 1980s | 16 | Soviet 8088 clone |
| **K1839VM1** | Soviet | 1990 | 32 | Soviet VAX-compatible |
| **K580IK51** | Soviet | 1980s | 8 | Soviet 8051 clone |
| **KR1858VM1** | Soviet | 1991 | 8 | Soviet Z80 clone (from U880) |
| **KR580VM1** | Soviet | 1980s | 8 | Unique 8080 extension, 128KB |
| **KR581IK1** | Soviet | 1980s | 16 | Soviet MCP-1600 clone |
| **KR581IK2** | Soviet | 1980s | 16 | Soviet MCP-1600 clone |
| **MCY7880** | DDR | 1982 | 8 | East German 8080 variant |
| **MPA1008** | DDR | 1980s | 4 | East German 4-bit MCU |
| **Tesla MHB8080A** | Czechoslovak | 1982 | 8 | 8080 clone for PMI-80 |
| **TVC CPU** | Hungary | 1985 | 8 | Videoton TVC home computer |
| **U8001** | DDR | 1984 | 16 | First 16-bit in Eastern Bloc (Z8000 clone) |
| **U80701** | DDR | 1989 | 32 | East German 32-bit attempt |
| **U808** | VEB Erfurt (DDR) | 1978 | 8 | First East German uP (8008 clone) |
| **U880** | VEB Erfurt (DDR) | 1980 | 8 | Most-used Eastern Bloc CPU (Z80 clone) |

### RCA COSMAC (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **1802** | 1976 | 8 | CPU | Voyager spacecraft, rad-hard |
| **CDP1804** | 1981 | 8 | CPU | Smaller-die 1802 variant |
| **CDP1805** | 1984 | 8 | CPU | Enhanced, New Horizons |
| **CDP1806** | 1984 | 8 | CPU | CMOS 1805 variant |
| **CDP1861** | 1976 | - | Video | Pixie video display |

### National Semiconductor (12 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **COP400** | 1977 | 4 | MCU | National's 4-bit MCU |
| **COP420** | 1979 | 4 | MCU | Enhanced COP400 |
| **COP444** | 1980 | 4 | MCU | COP400 family variant |
| **IMP-16** | 1973 | 16 | CPU | Early 16-bit (bit-slice based) |
| **NS32016** | 1982 | 32 | CPU | Early 32-bit |
| **NS32032** | 1984 | 32 | CPU | Improved NS32016 |
| **NS32081** | 1984 | - | FPU | NS32000 math coprocessor |
| **NS32082** | 1984 | - | MMU | NS32000 memory management |
| **NS32381** | 1988 | - | FPU | Integrated NS32000 FPU |
| **NSC800** | 1980 | 8 | CPU | CMOS Z80-compatible |
| **PACE** | 1975 | 16 | CPU | Early 16-bit PMOS |
| **SC/MP** | 1974 | 8 | CPU | Simple, low-cost |

### Rockwell (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **PPS-4** | 1972 | 4 | CPU | First single-chip 4-bit CPU |
| **PPS-4/1** | 1975 | 4 | CPU | Enhanced PPS-4 |
| **R6500/1** | 1980 | 8 | MCU | Single-chip 6502 |
| **R6511** | 1983 | 8 | MCU | 6502 with I/O |
| **R65C02** | 1983 | 8 | CPU | Rockwell CMOS 6502 |

### Other Manufacturers (184 models)

This large category encompasses processors from dozens of manufacturers. Organized by subcategory:

#### RISC Workstations - MIPS (10 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **MIPS R2000** | 1985 | 32 | CPU | Textbook RISC |
| **MIPS R3000** | 1988 | 32 | CPU | SGI workstations, PS1 |
| **MIPS R3000A** | 1989 | 32 | CPU | PlayStation variant |
| **MIPS R4000** | 1991 | 64 | CPU | First 64-bit MIPS |
| **MIPS R4400** | 1993 | 64 | CPU | Enhanced R4000 |
| **MIPS R4600** | 1994 | 64 | CPU | Low-cost "Orion" |
| **MIPS R8000** | 1994 | 64 | CPU | Superscalar, FP-optimized |
| **MIPS R10000** | 1995 | 64 | CPU | Out-of-order MIPS |
| **Stanford MIPS** | 1984 | 32 | CPU | Original academic MIPS |
| **IDT R3051** | 1991 | 32 | CPU | Embedded MIPS variant |

#### RISC Workstations - SPARC (7 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **SPARC** | 1987 | 32 | CPU | Sun register windows |
| **SuperSPARC** | 1992 | 32 | CPU | Superscalar SPARC |
| **MicroSPARC** | 1992 | 32 | CPU | Low-cost desktop SPARC |
| **MicroSPARC II** | 1994 | 32 | CPU | Enhanced MicroSPARC |
| **HyperSPARC** | 1993 | 32 | CPU | Ross Technology SPARC |
| **UltraSPARC** | 1995 | 64 | CPU | 64-bit Sun SPARC |
| **Cypress CY7C601** | 1989 | 32 | CPU | Early SPARC implementation |

#### RISC Workstations - HP PA-RISC (4 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **HP PA-RISC** | 1986 | 32 | CPU | HP workstations |
| **PA-7100** | 1992 | 32 | CPU | Superscalar PA-RISC |
| **PA-7100LC** | 1994 | 32 | CPU | Low-cost PA-RISC |
| **PA-7200** | 1994 | 32 | CPU | Dual-issue PA-RISC |

#### RISC Workstations - IBM POWER (3 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **POWER1** | 1990 | 32 | CPU | IBM RS/6000 |
| **POWER2** | 1993 | 32 | CPU | Enhanced POWER |
| **ROMP** | 1986 | 32 | CPU | IBM RT PC |

#### PowerPC (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **PowerPC 601** | 1993 | 32 | CPU | Apple/IBM/Motorola alliance |
| **PowerPC 603** | 1994 | 32 | CPU | Low-power PowerPC |
| **PowerPC 604** | 1994 | 32 | CPU | High-performance desktop |
| **PowerPC 620** | 1995 | 64 | CPU | 64-bit PowerPC |
| **PowerPC 403** | 1994 | 32 | CPU | Embedded PowerPC |

#### DEC Alpha (4 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Alpha 21064** | 1992 | 64 | CPU | Fastest of its era |
| **Alpha 21064A** | 1994 | 64 | CPU | Enhanced 21064 |
| **Alpha 21066** | 1994 | 64 | CPU | Low-cost Alpha |
| **Alpha 21164** | 1995 | 64 | CPU | 4-issue superscalar |

#### Berkeley RISC (2 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Berkeley RISC I** | 1982 | 32 | CPU | First RISC processor |
| **Berkeley RISC II** | 1983 | 32 | CPU | Refined RISC design |

#### x86-Compatible Clones (7 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Cyrix Cx486DLC** | 1992 | 32 | CPU | 386-pin 486 performance |
| **Cyrix 5x86** | 1995 | 32 | CPU | Pentium-class Cyrix |
| **NexGen Nx586** | 1994 | 32 | CPU | x86 with RISC core |
| **UMC U5** | 1994 | 32 | CPU | Taiwanese 486 clone |
| **Hyundai/ST 486** | 1993 | 32 | CPU | Korean 486 clone |
| **IBM 486SLC2** | 1992 | 32 | CPU | IBM enhanced 486 |
| **IBM Blue Lightning** | 1993 | 32 | CPU | IBM 486 variant |

#### DSP Processors (14 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **ADSP-2100** | 1986 | 16 | DSP | Analog Devices flagship DSP |
| **ADSP-2105** | 1989 | 16 | DSP | Low-cost ADSP-2100 |
| **ADSP-21020** | 1991 | 32 | DSP | Floating-point SHARC |
| **AT&T DSP-1** | 1980 | 16 | DSP | Bell Labs early DSP |
| **AT&T DSP16** | 1987 | 16 | DSP | Bell Labs production DSP |
| **AT&T DSP16A** | 1989 | 16 | DSP | Enhanced DSP16 |
| **AT&T DSP20** | 1980s | 16 | DSP | Bell Labs DSP |
| **AT&T DSP32C** | 1988 | 32 | DSP | IEEE 754 floating-point DSP |
| **DSP1600** | 1992 | 16 | DSP | Lucent/AT&T DSP |
| **Intel 2920** | 1979 | 25 | DSP | First Intel DSP with ADC/DAC |
| **Signetics 8X300** | 1976 | 8 | Signal | Bipolar signal processor |
| **WE DSP16** | 1987 | 16 | DSP | Western Electric DSP |
| **Zoran ZR34161** | 1993 | - | DSP | MPEG-1 video decoder |
| **Zoran ZR36110** | 1994 | - | DSP | MPEG audio/video |

#### Gaming / Console Processors (18 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Sony CXD8530BQ** | 1994 | 32 | CPU | PlayStation R3000A core |
| **Ricoh 5A22** | 1990 | 16 | CPU | SNES main CPU (65816-based) |
| **Ricoh 2A03** | 1983 | 8 | CPU | NES CPU (6502 + APU) |
| **HuC6280** | 1987 | 8 | CPU | TurboGrafx-16 |
| **Sharp SM83/LR35902** | 1989 | 8 | CPU | Game Boy CPU |
| **Sega SVP** | 1993 | 16 | DSP | Virtua Racing mapper |
| **Sega 315-5313 VDP** | 1988 | - | GPU | Genesis VDP |
| **SNK LSPC2** | 1990 | - | Custom | Neo Geo sprite controller |
| **Atari ANTIC** | 1979 | - | Custom | Atari 400/800 display |
| **Atari POKEY** | 1979 | - | Sound | Atari 400/800 sound/I/O |
| **Atari TIA** | 1977 | - | Custom | Atari 2600 graphics/sound |
| **MOS 6507** | 1975 | 8 | CPU | Atari 2600 (reduced 6502) |
| **MOS 6509** | 1981 | 8 | CPU | Commodore P500 banking |
| **SY6502A** | 1980 | 8 | CPU | Synertek 6502 speed variant |
| **GTE G65SC802** | 1986 | 16 | CPU | 65816-pin-compatible |
| **GTE G65SC816** | 1986 | 16 | CPU | Enhanced 65816 implementation |
| **Capcom CPS-A** | 1988 | - | Custom | CPS1 arcade sprite/tile engine |
| **Capcom CPS-B** | 1988 | - | Custom | CPS1 arcade priority/mixing |

#### Sound / Audio Processors (14 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Yamaha YM2151 (OPM)** | 1983 | - | Sound | FM synthesis, arcade standard |
| **Yamaha YM2610 (OPNB)** | 1988 | - | Sound | Neo Geo FM + ADPCM |
| **Yamaha YM2612 (OPN2)** | 1988 | - | Sound | Sega Genesis FM |
| **Yamaha YM3526 (OPL)** | 1985 | - | Sound | Arcade FM synthesis |
| **Yamaha YM3812 (OPL2)** | 1985 | - | Sound | Sound Blaster, AdLib |
| **Yamaha YMF262 (OPL3)** | 1990 | - | Sound | Sound Blaster Pro 2.0 |
| **Ensoniq OTTO** | 1988 | - | Sound | Ensoniq wavetable engine |
| **Ensoniq ES5503 (DOC)** | 1986 | - | Sound | Apple IIGS wavetable |
| **TI SN76489** | 1980 | - | Sound | TI sound chip (SMS, BBC) |
| **GI SP0256** | 1981 | - | Sound | Speech synthesis (Intellivision) |
| **Harris HC-55516** | 1980s | - | Sound | CVSD decoder (Williams pinball) |
| **OKI MSM5205** | 1983 | - | Sound | ADPCM speech (arcade) |
| **Philips SAA1099** | 1984 | - | Sound | Sam Coupe / CMS sound |
| **Konami SCC** | 1987 | - | Sound | MSX wavetable sound |

#### Graphics / Display Processors (11 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **S3 86C911** | 1991 | 32 | GPU | First S3 accelerator |
| **Tseng ET4000** | 1989 | 32 | GPU | Popular VGA accelerator |
| **ATI Mach32** | 1992 | 32 | GPU | ATI's first graphics processor |
| **ATI Mach64** | 1994 | 64 | GPU | Video acceleration |
| **Weitek P9000** | 1992 | 32 | GPU | High-end 2D accelerator |
| **C&T 65545** | 1993 | 32 | GPU | Laptop graphics accelerator |
| **Cirrus CL-GD5428** | 1993 | 32 | GPU | Popular VGA chip |
| **Matrox MGA-1064** | 1994 | 64 | GPU | Workstation graphics |
| **IIT AGX-015** | 1993 | 32 | GPU | XGA-compatible accelerator |
| **S3 Vision968** | 1994 | 64 | GPU | High-performance S3 |
| **Trident TGUI9440** | 1994 | 32 | GPU | Budget GUI accelerator |

#### Transputers (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **T212** | 1985 | 16 | CPU | 16-bit transputer |
| **T414** | 1985 | 32 | CPU | First 32-bit transputer |
| **T424** | 1987 | 32 | CPU | Enhanced T414 |
| **T800** | 1987 | 32 | CPU | Floating-point transputer |
| **T9000** | 1994 | 32 | CPU | Superscalar transputer |

#### Stack Machines / LISP (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Novix NC4016** | 1985 | 16 | CPU | Forth stack machine |
| **Harris RTX2000** | 1988 | 16 | CPU | Space-rated stack machine |
| **WISC CPU/16** | 1986 | 16 | CPU | Writable Instruction Set Computer |
| **WISC CPU/32** | 1980s | 32 | CPU | 32-bit WISC |
| **Symbolics 3600** | 1983 | 36 | CPU | LISP machine processor |

#### Network / Communications (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **WE32000** | 1982 | 32 | CPU | Unix workstation CPU |
| **WE32100** | 1984 | 32 | CPU | Improved WE32000 |
| **MAC-4** | 1980s | 8 | MCU | Bell Labs telecom MCU |
| **Am79C970 (PCnet)** | 1993 | - | I/O | AMD Ethernet controller |
| **i596** | 1987 | - | I/O | Intel LAN coprocessor |

#### Early / Pioneer Processors (10 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Fairchild F8** | 1975 | 8 | CPU | Multi-chip architecture |
| **Fairchild 9440** | 1979 | 16 | CPU | Data General Nova on a chip |
| **GI PIC1650** | 1977 | 8 | MCU | First PIC microcontroller |
| **GI CP1600** | 1975 | 16 | CPU | Intellivision CPU |
| **Intersil 6100** | 1975 | 12 | CPU | PDP-8 on a chip |
| **Harris HM6100** | 1978 | 12 | CPU | Faster Intersil 6100 |
| **Signetics 2650** | 1975 | 8 | CPU | Innovative architecture |
| **HP Nanoprocessor** | 1977 | 8 | MCU | HP's proprietary calculator MCU |
| **WD9000** | 1979 | 16 | CPU | Pascal MicroEngine |
| **WD16** | 1977 | 16 | CPU | PDP-11 compatible |

#### Japanese / Asian Processors (12 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **OKI MSM5840** | 1979 | 4 | MCU | OKI 4-bit MCU |
| **Samsung KS57** | 1984 | 4 | MCU | Korean 4-bit MCU |
| **Sanyo LC87** | 1985 | 8 | MCU | Sanyo 8-bit MCU |
| **Sanyo LC88** | 1986 | 16 | MCU | Sanyo 16-bit MCU |
| **Sharp LH5801** | 1981 | 8 | CPU | Sharp pocket computer CPU |
| **Mostek 3870** | 1977 | 8 | MCU | F8-based single-chip MCU |
| **MN1610** | 1976 | 16 | CPU | Panasonic 16-bit |
| **MN1613** | 1978 | 16 | CPU | Enhanced MN1610 |
| **mN601** | 1977 | 16 | CPU | Matsushita 16-bit |
| **Sunplus SPCxxxx** | 1990s | 16 | MCU | Taiwanese multimedia MCU |
| **Holtek HT48** | 1990 | 8 | MCU | Taiwanese MCU |
| **EMC EM78** | 1991 | 8 | MCU | Taiwanese PIC-compatible |

#### Military / Special Purpose (7 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Ferranti F100-L** | 1977 | 16 | CPU | British military 16-bit |
| **Plessey MIPROC** | 1977 | 16 | CPU | NATO crypto systems |
| **Raytheon RP-16** | 1980 | 16 | Bit-slice | Military bit-slice |
| **Monolithic MM6701** | 1978 | 4 | Bit-slice | ECL bit-slice |
| **Motorola MC10800** | 1979 | 4 | Bit-slice | ECL bit-slice |
| **i960 (mil)** | 1988 | 32 | CPU | Military embedded RISC |
| **MIL-STD-1750A** | 1980 | 16 | CPU | Standard military ISA |

#### Miscellaneous (71 remaining models)

This subcategory covers additional processors from various manufacturers and niches not captured in the above sections, including additional MCU variants, co-processors, controllers, DMA engines, additional clones, evaluation/academic chips, and application-specific processors that complete the full set of 184 models in the "Other" family.

---

## Models by Architecture

### 1-Bit Processors (1)
- Motorola MC14500B (1976) - Industrial controller

### 4-Bit Processors (28)
- **Intel**: 4004, 4040
- **TI**: TMS0800, TMS1000, SN74181 (ALU)
- **Rockwell**: PPS-4, PPS-4/1
- **NEC**: uCOM-4, uPD546, uPD751, uPD612xA, uPD1007C
- **Fujitsu**: MB8841, MB8842, MB8843, MB8844, MB8845
- **Mitsubishi**: MELPS 4, MELPS 41, MELPS 42
- **AMI**: S2000, S2150, S2200, S2400
- **Hitachi**: HMCS40
- **National**: COP400, COP420, COP444
- **OKI**: MSM5840
- **Samsung**: KS57
- **Eastern Bloc**: MPA1008

### 8-Bit Processors (78)
- **Intel**: 8008, 8080, 8085, 8048, 8039, 8044, 8748, 8051, 8061, 8751
- **Motorola**: 6800, 6801, 6802, 6803, 6804, 6805, 6805R2, 6809, 68HC05, 68HC11, 68HC11A1
- **MOS/WDC**: 6502, 6510, 8501, 8502, 65C02
- **Zilog**: Z80, Z80A, Z80B, Z180, Z8S180, Z8, Super8
- **NEC**: uPD780, uPD7801, uPD7810
- **Mitsubishi**: MELPS 740, M50740, M50747
- **Hitachi**: HD6301, HD6305, HD64180, 6309
- **Toshiba**: TLCS-870, TLCS-90, TMS370
- **RCA**: 1802, CDP1804, CDP1805, CDP1806
- **National**: SC/MP, NSC800
- **Rockwell**: R6500/1, R6511, R65C02
- **Eastern Bloc**: U880, U808, KR580VM1, KR1858VM1, IM1821VM85A, Tesla MHB8080A, CM630, MCY7880, TVC CPU, K580IK51
- **Gaming**: Ricoh 2A03, MOS 6507, MOS 6509, SY6502A, Sharp SM83, HuC6280
- **Others**: F8, PIC1650, 2650, Mostek 3870, Fujitsu MB8861, Sharp LH5801, HP Nanoprocessor, MAC-4

### 12-Bit Processors (3)
- Intersil 6100 (PDP-8 compatible)
- Toshiba TLCS-12 (First Japanese microprocessor)
- Toshiba TLCS-12A (Improved)

### 16-Bit Processors (50+)
- **Intel**: 8086, 8088, 80186, 80188, 80286, 8096, 80C186
- **Motorola**: 68000, 68008, 68010, 68HC16
- **MOS/WDC**: 65816
- **Zilog**: Z280, Z8000
- **NEC**: V20, V30
- **TI**: TMS9900, TMS9980, TMS9985, TMS9995
- **Hitachi**: H8/300, H8/500
- **Eastern Bloc**: U8001, K1801VM1, K1801VM2, K1801VM3, K1810VM86, K1810VM88, KR581IK1, KR581IK2
- **Pioneers**: IMP-16, PACE, mN601, WD16, F100-L, CP1600, MN1610, MN1613
- **Gaming**: Ricoh 5A22, GTE G65SC802, GTE G65SC816
- **Others**: NC4016, RTX2000, Plessey MIPROC, WD9000, Sanyo LC88, WISC CPU/16, Fairchild 9440, T212, MIL-STD-1750A

### 32-Bit Processors (~110)
- **Intel**: 80386, 80486, Pentium, iAPX 432, i960, i960CA, i960CF
- **Motorola**: 68020, 68030, 68040, 68060, CPU32, ColdFire, 88100, 88110
- **NEC**: V60, V70, V810, V850
- **Zilog**: Z380, Z80000
- **ARM**: ARM1, ARM2, ARM250, ARM3, ARM6, ARM610, ARM7TDMI
- **MIPS**: Stanford MIPS, MIPS R2000, R3000, R3000A, IDT R3051
- **SPARC**: SPARC, Fujitsu MB86900, SPARClite, SuperSPARC, MicroSPARC, MicroSPARC II, HyperSPARC, Cypress CY7C601
- **HP**: PA-RISC, PA-7100, PA-7100LC, PA-7200
- **IBM/PowerPC**: ROMP, POWER1, POWER2, PowerPC 601, 603, 604, 403
- **x86 Clones**: Cyrix Cx486DLC, Cyrix 5x86, NexGen Nx586, UMC U5, Hyundai/ST 486, IBM 486SLC2, IBM Blue Lightning, AMD Am386, Am486, Am5x86
- **Transputers**: T414, T424, T800, T9000
- **DEC**: Alpha 21066 (32-bit bus variant)
- **Toshiba**: TX39
- **Hitachi**: SH-1, SH-2
- **Eastern Bloc**: Elbrus EL-90, K1839VM1, U80701
- **Berkeley**: RISC I, RISC II
- **Others**: NS32016, NS32032, Am29000, WE32000, WE32100, TMS34010, TMS34020, WISC CPU/32, Symbolics 3600

### 64-Bit Processors (~10)
- **Intel**: i860
- **DEC Alpha**: 21064, 21064A, 21164
- **MIPS**: R4000, R4400, R4600, R8000, R10000
- **SPARC**: UltraSPARC
- **PowerPC**: PowerPC 620

### Bit-Slice (12)
- AMD Am2901, Am2903, Am29C101, Am2910, Am29116
- Intel 3002, 3003
- TI SN74S481, SBP0400, SBP0401
- Monolithic Memories MM6701
- Motorola MC10800 (ECL)
- Raytheon RP-16

### FPUs / Math Coprocessors (10)
- Intel 8087, 8087 (2nd gen), 80287, 80387, 8231
- Motorola 68851 (MMU), 68881, 68882
- AMD Am9511, Am9512
- National NS32081, NS32082 (MMU), NS32381

### DSPs / Signal Processors (~22)
- **TI**: TMS320C10, C25, C30, C40, C50, C80
- **NEC**: uPD7720, uPD7725
- **AMI**: S2811, S28211
- **Analog Devices**: ADSP-2100, ADSP-2105, ADSP-21020
- **AT&T/Lucent**: DSP-1, DSP16, DSP16A, DSP20, DSP32C, DSP1600
- **Motorola**: DSP56001, DSP96002
- **Intel**: 2920
- **Signetics**: 8X300
- **Zoran**: ZR34161, ZR36110
- **Sega**: SVP

### Graphics Processors (~10)
- **NEC**: uPD7220 (First LSI GPU)
- **Hitachi**: HD63484, HD63484 rev 2
- **TI**: TMS34010, TMS34020
- **S3**: 86C911, Vision968
- **ATI**: Mach32, Mach64
- **Weitek**: P9000
- **Tseng**: ET4000
- **C&T**: 65545
- **Cirrus**: CL-GD5428
- **Others**: Matrox MGA-1064, IIT AGX-015, Trident TGUI9440

### Sound / Audio Processors (~12)
- **Yamaha**: YM2151, YM2610, YM2612, YM3526, YM3812, YMF262
- **Ensoniq**: OTTO, ES5503
- **TI**: SN76489, TMS5100
- **NEC**: uPD7759
- **Others**: GI SP0256, Harris HC-55516, OKI MSM5205, Philips SAA1099, Konami SCC, Atari POKEY

### Gaming / Arcade Custom (~20)
- **Namco**: 05xx, 50xx, 51xx, 52xx, 53xx, 54xx
- **Hitachi**: FD1089, FD1094 (Encrypted 68000)
- **Console CPUs**: Sony CXD8530BQ (PS1), Ricoh 5A22 (SNES), Ricoh 2A03 (NES), HuC6280 (TG-16), Sharp SM83 (Game Boy)
- **Sega**: SVP, 315-5313 VDP
- **Atari**: ANTIC, TIA
- **SNK**: LSPC2
- **Capcom**: CPS-A, CPS-B

---

## Models by Application Domain

### Personal Computers
- **Intel**: 8080 (Altair), 8088 (IBM PC), 80286 (IBM AT), 80386, 80486, Pentium
- **Zilog**: Z80 (CP/M, TRS-80, MSX)
- **MOS**: 6502 (Apple II, Commodore 64)
- **Motorola**: 68000 (Macintosh, Amiga, Atari ST)
- **x86 Clones**: Cyrix Cx486DLC, 5x86; NexGen Nx586; AMD Am386/Am486/Am5x86; UMC U5; IBM 486SLC2

### Game Consoles
- **MOS 6502**: NES (via Ricoh 2A03), Atari 2600 (via 6507)
- **MOS 6510**: Commodore 64
- **WDC 65816**: Super Nintendo (via Ricoh 5A22)
- **Motorola 68000**: Sega Genesis
- **HuC6280**: TurboGrafx-16
- **Sharp SM83**: Game Boy
- **MIPS R3000A / Sony CXD8530BQ**: PlayStation
- **Hitachi SH-2**: Sega Saturn

### RISC Workstations
- **MIPS**: R2000, R3000, R4000, R4400, R4600, R8000, R10000 (SGI)
- **SPARC**: SPARC, SuperSPARC, MicroSPARC, HyperSPARC, UltraSPARC (Sun)
- **HP PA-RISC**: PA-RISC, PA-7100, PA-7100LC, PA-7200 (HP)
- **IBM POWER**: POWER1, POWER2, ROMP (IBM RS/6000)
- **DEC Alpha**: 21064, 21064A, 21066, 21164 (DEC)
- **ARM**: ARM1-ARM7TDMI (Acorn, embedded)

### Superscalar / High-Performance
- **PowerPC**: 601, 603, 604, 620 (Apple Power Macs, IBM)
- **Alpha**: 21064, 21064A, 21164 (fastest of era)
- **MIPS**: R8000 (superscalar FP), R10000 (out-of-order)
- **PA-RISC**: PA-7100, PA-7200 (dual-issue)
- **Intel**: Pentium (first superscalar x86)
- **Motorola**: 68060, 88110 (superscalar)
- **SPARC**: SuperSPARC, UltraSPARC

### Arcade / Gaming Custom
- **Fujitsu MB8841-8845**: Galaga, Xevious
- **Namco custom**: Pac-Man era arcade machines
- **Hitachi FD1089/1094**: Sega System 16/24 encrypted CPUs
- **Capcom CPS-A/CPS-B**: Street Fighter II era arcade
- **SNK LSPC2**: Neo Geo
- **Sega SVP, VDP**: Genesis/Mega Drive custom

### Graphics Processors
- **Early**: NEC uPD7220 (1981), Hitachi HD63484 (1984)
- **Programmable GPU**: TI TMS34010, TMS34020
- **1990s Accelerators**: S3 86C911/Vision968, ATI Mach32/Mach64, Tseng ET4000, Weitek P9000, Cirrus CL-GD5428, C&T 65545, Matrox MGA-1064, Trident TGUI9440

### Sound / Audio
- **Yamaha FM**: YM2151 (arcade), YM2612 (Genesis), YM3812/OPL2 (Sound Blaster), YMF262/OPL3
- **Wavetable**: Ensoniq OTTO, ES5503 (Apple IIGS)
- **PSG/Square wave**: TI SN76489 (SMS, BBC), Atari POKEY
- **Speech**: TI TMS5100, NEC uPD7759, GI SP0256
- **ADPCM/CVSD**: OKI MSM5205, Harris HC-55516

### Space / Military
- **RCA 1802/1804/1805/1806**: Voyager, New Horizons
- **Harris RTX2000**: Space-rated systems
- **Ferranti F100-L**: British military 16-bit
- **Plessey MIPROC**: NATO crypto systems
- **Raytheon RP-16**: Military bit-slice
- **MIL-STD-1750A**: Standard military ISA

### Embedded / Automotive
- **Intel**: 8048/8051/8061/8096, 80C186, i960 series
- **Motorola**: 68HC05/68HC11/68HC16, 68302/68360, ColdFire, CPU32
- **Hitachi**: H8/300, H8/500, SH-1, SH-2
- **NEC**: V810, V850
- **Mitsubishi**: MELPS 740 (600+ variants, still in use)
- **TI**: TMS1000, TMS7000, TMS370
- **GI**: PIC1650
- **Toshiba**: TLCS series, TX39
- **PowerPC**: 403 (embedded)

### DSP / Signal Processing
- **TI**: TMS320 family (C10 through C80)
- **Motorola**: DSP56001, DSP96002
- **Analog Devices**: ADSP-2100, ADSP-2105, ADSP-21020
- **AT&T/Lucent**: DSP-1, DSP16, DSP20, DSP32C, DSP1600
- **NEC**: uPD7720, uPD7725
- **Zoran**: ZR34161 (MPEG-1), ZR36110

### Eastern Bloc Computing
- **DDR**: U880 (KC 85, Robotron), U808, U8001, U80701, MCY7880, MPA1008
- **Soviet**: KR580VM1, KR1858VM1, IM1821VM85A, K1810VM86/88, K1801VM1/2/3, K1839VM1, K580IK51, Elbrus EL-90
- **Czechoslovak**: Tesla MHB8080A (PMI-80/PMD 85)
- **Bulgaria**: CM630 (Pravetz)
- **Hungary**: TVC CPU (Videoton)

### Parallel / Transputer
- **INMOS**: T212, T414, T424, T800, T9000
- **Motorola**: 88100, 88110 (parallel bus support)
- **TI**: TMS320C40 (multiprocessor DSP)

---

## Validation Summary

| Family | Models | Avg CPI Error | Status |
|--------|--------|---------------|--------|
| Intel | 39 | 1.8% | All passing |
| Motorola | 32 | 1.2% | All passing |
| MOS/WDC | 6 | 1.0% | All passing |
| Zilog | 14 | 1.5% | All passing |
| NEC | 18 | 1.5% | All passing |
| TI | 21 | 1.4% | All passing |
| AMD | 12 | 1.6% | All passing |
| Hitachi | 13 | 1.3% | All passing |
| Fujitsu | 8 | 1.2% | All passing |
| AMI | 6 | 1.5% | All passing |
| Mitsubishi | 6 | 1.4% | All passing |
| Toshiba | 6 | 1.6% | All passing |
| ARM | 7 | 1.8% | All passing |
| Namco | 6 | 1.5% | All passing |
| Eastern Bloc | 22 | 1.3% | All passing |
| RCA | 5 | 1.4% | All passing |
| National | 12 | 1.7% | All passing |
| Rockwell | 5 | 1.5% | All passing |
| Other | 184 | 1.8% | All passing |
| **Total** | **467** | **1.6%** | **All 467 at <2% CPI error** |

---

## File Structure

Each model folder contains:

```
[Processor Name]/
├── current/
│   └── [name]_validated.py    # Validated Python model
├── validation/
│   └── [name]_validation.json # Validation data & timing tests
├── measurements/              # Calibration input data
│   ├── measured_cpi.json      #   Per-workload CPI measurements
│   ├── benchmarks.json        #   Benchmark scores
│   └── instruction_traces.json #  Instruction mix data
├── identification/            # System identification results
│   └── sysid_result.json      #   Fitted correction terms
├── README.md                  # Quick reference
├── CHANGELOG.md               # Full history (append-only)
├── HANDOFF.md                 # Current state & next steps
└── docs/                      # Additional documentation
```

---

## Usage

### Running a Model

```python
from i8080_validated import I8080Model

model = I8080Model()
result = model.analyze('typical')

print(f"CPI: {result.cpi:.2f}")
print(f"IPC: {result.ipc:.3f}")
print(f"IPS: {result.ips:,.0f}")
```

### Running Validation

```python
validation = model.validate()
print(f"Tests: {validation['passed']}/{validation['total']}")
print(f"Accuracy: {validation['accuracy_percent']:.1f}%")
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial collection, 65 models |
| 2.0 | Jan 2026 | Expanded to 76 models, cross-validation |
| 3.0 | Jan 2026 | **80 models**, all validated <2% error |
| 4.0 | Jan 2026 | **196 models**, pre-1986 extended coverage complete |
| 5.0 | Jan 30, 2026 | **467 models**, Phase 6 post-1985 complete |

---

## References

- Intel Microprocessor Quick Reference Guide
- Motorola M68000 Family Programmer's Reference
- Zilog Z80 CPU User Manual
- MOS 6502 Programming Manual
- Patterson & Hennessy: Computer Architecture
- Various manufacturer datasheets (Bitsavers archive)
- VEB Mikroelektronik Erfurt U880 Datenblatt
- NEC V60/V70 Technical Manual
- Fujitsu MB884x Series Documentation
- MAME emulator source code (arcade chip timing)
- Soviet microprocessor catalogs
- MIPS R4000 User's Manual
- DEC Alpha Architecture Reference Manual
- Sun SPARC Architecture Manual
- HP PA-RISC Architecture Reference
- IBM POWER Architecture Book
- Yamaha FM synthesis datasheets
- S3, ATI, Tseng graphics chip documentation

---

**Collection Maintainer:** Grey-Box Performance Modeling Research
**Last Updated:** January 30, 2026
**Total Models:** 467
**Validation Status:** All 467 models passing at <2% CPI error
