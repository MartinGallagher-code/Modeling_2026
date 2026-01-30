# Historical Microprocessor Collection - Master Catalog

## Overview

This collection contains **422 queueing-theory-based performance models** covering the complete evolution of microprocessors from the first commercial CPU (Intel 4004, 1971) through the mid-1990s RISC and superscalar era (1995).

The models use grey-box methodology combining architectural knowledge, M/M/1 queueing networks, and calibration against real hardware measurements to achieve typical accuracy within 5% of actual performance. All 422 models are validated with <5% CPI error.

---

## Collection at a Glance

| Metric | Value |
|--------|-------|
| Total Models | 422 |
| Year Range | 1970-1995 |
| Manufacturers | 60+ |
| Architectures | 4-bit, 8-bit, 12-bit, 16-bit, 32-bit, 64-bit |
| Categories | CPUs, MCUs, DSPs, Bit-slice, Arcade custom, Calculator |

---

## Complete Model Inventory

### Intel Corporation (39 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **4004** | 1971 | 4 | CPU | First commercial microprocessor |
| **4040** | 1974 | 4 | CPU | Enhanced 4004, interrupts added |
| **8008** | 1972 | 8 | CPU | First 8-bit microprocessor |
| **8080** | 1974 | 8 | CPU | Industry standard, enabled Altair |
| **8085** | 1976 | 8 | CPU | Improved 8080, single supply |
| **8085a** | 1976 | 8 | CPU | Speed-graded 8085 |
| **8035** | 1976 | 8 | MCU | MCS-48 family, ROM-less |
| **8039** | 1976 | 8 | MCU | MCS-48, more RAM |
| **8048** | 1976 | 8 | MCU | MCS-48 flagship |
| **8049** | 1976 | 8 | MCU | MCS-48 variant, 2KB ROM |
| **8051** | 1980 | 8 | MCU | MCS-51 flagship, still made today |
| **8052** | 1980 | 8 | MCU | 8KB ROM, 256B RAM |
| **8061** | 1983 | 8 | MCU | Ford EEC-IV engine controller |
| **8086** | 1978 | 16 | CPU | x86 architecture origin |
| **8088** | 1979 | 16 | CPU | IBM PC processor |
| **80186** | 1982 | 16 | CPU | Integrated 8086 system |
| **80188** | 1982 | 16 | CPU | 8-bit bus 80186 |
| **80286** | 1982 | 16 | CPU | Protected mode, IBM AT |
| **80386** | 1985 | 32 | CPU | First x86 32-bit |
| **80386SX** | 1988 | 32 | CPU | 16-bit bus 80386 |
| **80486** | 1989 | 32 | CPU | Integrated FPU and cache |
| **80486DX2** | 1992 | 32 | CPU | Clock-doubled 486 |
| **80486DX4** | 1994 | 32 | CPU | Clock-tripled 486 |
| **Pentium** | 1993 | 32 | CPU | Superscalar x86 |
| **Pentium Pro** | 1995 | 32 | CPU | Out-of-order x86 |
| **8096** | 1982 | 16 | MCU | Automotive standard |
| **8196** | 1984 | 16 | MCU | ROM-less 8096 |
| **i860** | 1989 | 64 | CPU | RISC/VLIW hybrid |
| **i960** | 1988 | 32 | CPU | Embedded RISC |
| **iAPX 432** | 1981 | 32 | CPU | Object-oriented architecture |
| **80287** | 1982 | - | FPU | x87 coprocessor for 286 |
| **80387** | 1987 | - | FPU | x87 coprocessor for 386 |
| *+8 additional variants* | | | | MCS-48/51 family and embedded |

### Motorola (32 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6800** | 1974 | 8 | CPU | Motorola's first microprocessor |
| **6801** | 1978 | 8 | MCU | 6800 + ROM + RAM + I/O |
| **6802** | 1977 | 8 | CPU | 6800 + 128B RAM + clock |
| **6803** | 1983 | 8 | MCU | ROM-less 6801 |
| **6805** | 1979 | 8 | MCU | Low-cost MCU family |
| **6809** | 1979 | 8 | CPU | Most advanced 8-bit |
| **6811** | 1985 | 8 | MCU | HC11 family, still in use |
| **68000** | 1979 | 16/32 | CPU | Macintosh, Amiga, Atari ST |
| **68008** | 1982 | 16/32 | CPU | 8-bit bus 68000 |
| **68010** | 1982 | 16/32 | CPU | Virtual memory support |
| **68020** | 1984 | 32 | CPU | Full 32-bit 68k |
| **68030** | 1987 | 32 | CPU | Integrated MMU |
| **68040** | 1990 | 32 | CPU | Integrated FPU + caches |
| **68060** | 1994 | 32 | CPU | Superscalar 68k |
| **68HC05** | 1984 | 8 | MCU | CMOS version of 6805 |
| **68HC08** | 1993 | 8 | MCU | Enhanced HC05 |
| **68HC11** | 1985 | 8 | MCU | De facto MCU standard |
| **68HC12** | 1996 | 16 | MCU | HC11 successor |
| **68HC16** | 1991 | 16 | MCU | 16-bit MCU |
| **DSP56001** | 1987 | 24 | DSP | 24-bit fixed-point DSP |
| **56002** | 1990 | 24 | DSP | Enhanced DSP56001 |
| **68302** | 1989 | 32 | Comm | Integrated communications |
| **88000** | 1988 | 32 | CPU | Motorola RISC architecture |
| **88100** | 1988 | 32 | CPU | 88000 CPU component |
| **88110** | 1991 | 32 | CPU | Superscalar 88k |
| **ColdFire** | 1994 | 32 | CPU | Embedded 68k replacement |
| **PowerPC 601** | 1993 | 32 | CPU | Apple Power Macintosh |
| **PowerPC 603** | 1994 | 32 | CPU | Low-power PowerPC |
| *+4 additional variants* | | | | 68xx family and embedded |

### MOS Technology / Western Design Center (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6502** | 1975 | 8 | CPU | Apple II, C64, NES |
| **6507** | 1975 | 8 | CPU | Atari 2600, reduced pins |
| **6510** | 1982 | 8 | CPU | Commodore 64 variant |
| **65C02** | 1983 | 8 | CPU | CMOS 6502, new instructions |
| **65802** | 1984 | 16 | CPU | 65816 in 40-pin package |
| **65816** | 1984 | 16 | CPU | Apple IIGS, SNES |

### Zilog (14 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Z80** | 1976 | 8 | CPU | CP/M standard, MSX, TRS-80 |
| **Z80 Peripherals** | 1976 | - | Support | PIO, SIO, CTC reference |
| **Z80A** | 1976 | 8 | CPU | 4 MHz Z80 |
| **Z80B** | 1976 | 8 | CPU | 6 MHz Z80 |
| **Z80H** | 1980 | 8 | CPU | 8 MHz Z80 |
| **Z180** | 1985 | 8 | CPU | Enhanced Z80, MMU |
| **Z280** | 1985 | 16 | CPU | Failed Z80 successor |
| **Z380** | 1994 | 32 | CPU | 32-bit Z80 lineage |
| **Z8** | 1979 | 8 | MCU | Zilog microcontroller |
| **Z8000** | 1979 | 16 | CPU | Zilog 16-bit |
| **Z8001** | 1979 | 16 | CPU | Segmented Z8000 |
| **Z8002** | 1979 | 16 | CPU | Non-segmented Z8000 |
| **eZ80** | 1999 | 8 | CPU | Pipelined Z80 successor |
| *+1 additional variant* | | | | Z80 family |

### ARM (7 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **ARM1** | 1985 | 32 | CPU | First ARM, RISC pioneer |
| **ARM2** | 1986 | 32 | CPU | Acorn Archimedes |
| **ARM3** | 1989 | 32 | CPU | First ARM with cache |
| **ARM6** | 1991 | 32 | CPU | First licensable core |
| **ARM7** | 1993 | 32 | CPU | Game Boy Advance |
| **ARM7TDMI** | 1994 | 32 | CPU | Thumb + debug extensions |
| **ARM610** | 1992 | 32 | CPU | Apple Newton processor |

### RCA (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **1802** | 1976 | 8 | CPU | Voyager spacecraft, rad-hard |
| **CDP1802A** | 1980 | 8 | CPU | Speed-enhanced 1802 |
| **CDP1804** | 1980 | 8 | CPU | Enhanced 1802 |
| **CDP1805** | 1984 | 8 | CPU | Further enhanced, New Horizons |
| **CDP1806** | 1985 | 8 | CPU | Final COSMAC |

### Texas Instruments (21 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **SN74181** | 1970 | 4 | ALU | First single-chip ALU |
| **TMS1000** | 1974 | 4 | MCU | First mass-produced MCU |
| **TMS1100** | 1975 | 4 | MCU | Enhanced TMS1000 |
| **TMS1400** | 1978 | 4 | MCU | Extended TMS1000 family |
| **TMS7000** | 1981 | 8 | MCU | TI's 8-bit MCU family |
| **TMS7002** | 1985 | 8 | MCU | Dual-processor TMS7000 |
| **TMS9900** | 1976 | 16 | CPU | TI-99/4A, workspace architecture |
| **TMS9980** | 1979 | 16 | CPU | Cost-reduced TMS9900 |
| **TMS9995** | 1981 | 16 | CPU | Enhanced TMS9900 |
| **TMS9940** | 1981 | 16 | MCU | TMS9900-based MCU |
| **TMS320C10** | 1983 | 16 | DSP | First TI DSP |
| **TMS320C25** | 1986 | 16 | DSP | Second-gen TI DSP |
| **TMS320C30** | 1988 | 32 | DSP | Floating-point DSP |
| **TMS320C40** | 1991 | 32 | DSP | Multiprocessing DSP |
| **TMS320C50** | 1991 | 16 | DSP | Low-cost fixed-point |
| **TMS320C54x** | 1995 | 16 | DSP | Cell phone standard |
| **TMS370** | 1986 | 8 | MCU | Automotive MCU family |
| **MSP430** | 1993 | 16 | MCU | Ultra-low-power MCU |
| *+3 additional variants* | | | | TMS family extensions |

### National Semiconductor (12 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **SC/MP** | 1974 | 8 | CPU | Simple low-cost processor |
| **NSC800** | 1979 | 8 | CPU | CMOS Z80 clone |
| **COP400** | 1977 | 4 | MCU | National's 4-bit MCU line |
| **COP800** | 1986 | 8 | MCU | 8-bit MCU family |
| **NS32008** | 1981 | 32 | CPU | First NS32000 family |
| **NS32016** | 1982 | 32 | CPU | Early 32-bit CPU |
| **NS32032** | 1984 | 32 | CPU | Improved NS32016 |
| **NS32332** | 1988 | 32 | CPU | Full 32-bit bus NS32k |
| **NS32532** | 1990 | 32 | CPU | Final NS32000 family |
| **CompactRISC** | 1992 | 32 | CPU | Embedded RISC from National |
| *+2 additional models* | | | | Peripheral/support chips |

### NEC (18 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **V20** | 1984 | 16 | CPU | Faster 8088, 8080 mode |
| **V30** | 1984 | 16 | CPU | Faster 8086, 8080 mode |
| **V25** | 1986 | 16 | CPU | Enhanced V20 with MCU features |
| **V33** | 1988 | 16 | CPU | Enhanced V30 |
| **V40** | 1986 | 16 | CPU | V20 with bus controller |
| **V50** | 1987 | 16 | CPU | V30 with bus controller |
| **V60** | 1986 | 32 | CPU | 32-bit CISC |
| **V70** | 1987 | 32 | CPU | Enhanced V60 |
| **V810** | 1994 | 32 | CPU | Virtual Boy processor |
| **V850** | 1994 | 32 | CPU | Automotive embedded RISC |
| **uPD7720** | 1981 | 16 | DSP | Early signal processor |
| **uPD7725** | 1985 | 16 | DSP | Enhanced DSP (SNES coprocessor) |
| **uPD780** | 1976 | 8 | CPU | Z80 second source |
| **uPD8080** | 1974 | 8 | CPU | 8080 second source |
| **78K0** | 1986 | 8 | MCU | NEC 8-bit MCU family |
| **78K4** | 1993 | 16 | MCU | NEC 16-bit MCU |
| *+2 additional variants* | | | | V-series and DSP family |

### AMD (12 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **Am2901** | 1975 | 4 | Bit-slice | Bit-slice ALU building block |
| **Am2903** | 1976 | 4 | Bit-slice | Enhanced Am2901 |
| **Am2910** | 1976 | - | Sequencer | Microprogram sequencer |
| **Am9080** | 1975 | 8 | CPU | AMD 8080 clone |
| **Am9511** | 1978 | - | FPU | Arithmetic processor |
| **Am29000** | 1987 | 32 | CPU | AMD RISC, laser printers |
| **Am29050** | 1990 | 32 | CPU | Enhanced 29k with FPU |
| **Am386** | 1991 | 32 | CPU | AMD's 386 clone |
| **Am486** | 1993 | 32 | CPU | AMD's 486 clone |
| **Am5x86** | 1995 | 32 | CPU | Enhanced 486 |
| **Am29116** | 1983 | 16 | Bit-slice | 16-bit bipolar processor |
| *+1 additional model* | | | | Bit-slice family |

### Hitachi (13 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **6309** | 1982 | 8 | CPU | Enhanced 6809, "best 8-bit ever" |
| **6301** | 1983 | 8 | MCU | 6801-compatible, Sega Master System |
| **6303** | 1985 | 8 | MCU | Enhanced 6301 |
| **63C09** | 1984 | 8 | CPU | CMOS 6309 |
| **H8/300** | 1990 | 16 | MCU | Popular embedded MCU |
| **H8/500** | 1993 | 16 | MCU | Enhanced H8 series |
| **HD6413xx** | 1988 | 8 | MCU | Industrial MCU series |
| **SH-1** | 1992 | 32 | CPU | SuperH RISC, Sega 32X |
| **SH-2** | 1994 | 32 | CPU | Sega Saturn |
| **SH-3** | 1995 | 32 | CPU | Windows CE devices |
| **HD63484** | 1985 | 16 | GPU | Graphics processor |
| **HD64180** | 1985 | 8 | CPU | Z180 second-source |
| *+1 additional model* | | | | HD series variants |

### Fujitsu (8 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **MB8841** | 1980 | 4 | MCU | Arcade game controller |
| **MB8842** | 1981 | 4 | MCU | Enhanced MB8841 |
| **MB8843** | 1982 | 4 | MCU | Namco arcade custom |
| **MB8844** | 1983 | 4 | MCU | Extended 884x family |
| **MB88401** | 1984 | 4 | MCU | Arcade sound controller |
| **SPARClite** | 1992 | 32 | CPU | Embedded SPARC |
| *+2 additional models* | | | | Arcade and embedded |

### AMI (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **S2000** | 1971 | 4 | Calculator | Early calculator chip |
| **S2150** | 1972 | 4 | Calculator | Scientific calculator |
| **S2200** | 1973 | 4 | Calculator | Enhanced calculator |
| **S2400** | 1974 | 4 | Calculator | Programmable calculator |
| **S9000** | 1975 | 4 | MCU | General-purpose MCU |
| *+1 additional model* | | | | Calculator/MCU family |

### Mitsubishi (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **MELPS740** | 1983 | 8 | MCU | 6502-based MCU family |
| **MELPS7700** | 1990 | 16 | MCU | 65816-based MCU |
| **M16C** | 1993 | 16 | MCU | Embedded 16-bit MCU |
| **M32R** | 1994 | 32 | CPU | Embedded RISC |
| *+2 additional models* | | | | MELPS family variants |

### Toshiba (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **TLCS-90** | 1988 | 8 | MCU | Z80-compatible MCU |
| **TLCS-900** | 1990 | 16/32 | MCU | Advanced MCU family |
| **TLCS-870** | 1987 | 8 | MCU | Low-power MCU |
| **T3444** | 1983 | 4 | MCU | 4-bit MCU |
| **TX39** | 1994 | 32 | CPU | MIPS-based embedded |
| *+1 additional model* | | | | TLCS family |

### Namco Custom (6 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **CUS47** | 1984 | 8 | Custom | Namco arcade custom CPU |
| **C65** | 1985 | 8 | Custom | Namco System 1 |
| **C68** | 1987 | 16 | Custom | Namco System 2 |
| **C70** | 1987 | 8 | Custom | Namco I/O controller |
| **C140** | 1987 | - | Sound | Namco sound processor |
| *+1 additional model* | | | | Arcade custom ICs |

### Eastern Bloc (22 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **U880** | 1980 | 8 | CPU | DDR Z80 clone (VEB Mikroelektronik) |
| **U880D** | 1981 | 8 | CPU | Enhanced U880 |
| **U8820** | 1982 | 8 | CPU | DDR Z8 clone |
| **U80601** | 1986 | 32 | CPU | DDR 32-bit attempt |
| **KR580VM80A** | 1978 | 8 | CPU | Soviet 8080 clone |
| **T34VM1** | 1983 | 16 | CPU | Soviet original design |
| **KR1810VM86** | 1983 | 16 | CPU | Soviet 8086 clone |
| **1839VM1** | 1988 | 16 | CPU | Soviet PDP-11 compatible |
| **KR1801VM1** | 1981 | 16 | CPU | Soviet DEC LSI-11 clone |
| **Elbrus-1** | 1979 | 64 | CPU | Soviet supercomputer CPU |
| **Elbrus-2** | 1985 | 64 | CPU | Enhanced Elbrus |
| **Tesla MHB8080** | 1977 | 8 | CPU | Czech 8080 clone |
| **CEMI MCY7880** | 1979 | 8 | CPU | Polish 8080 clone |
| **MMN80CPU** | 1980 | 8 | CPU | Romanian Z80 clone |
| *+8 additional models* | | | | Soviet/DDR/Czech variants |

### Rockwell (5 models)

| Model | Year | Bits | Type | Significance |
|-------|------|------|------|--------------|
| **PPS-4** | 1972 | 4 | MCU | Early 4-bit processor |
| **PPS-8** | 1975 | 8 | CPU | Rockwell 8-bit family |
| **R6502** | 1978 | 8 | CPU | Rockwell 6502 variant |
| **R6511** | 1980 | 8 | MCU | 6502 variant with peripherals |
| **R65C02** | 1984 | 8 | CPU | Rockwell CMOS 6502 |

### Other Manufacturers (184 models)

This category includes processors from 40+ manufacturers. Notable entries:

| Model | Manufacturer | Year | Bits | Significance |
|-------|--------------|------|------|--------------|
| **F8** | Fairchild | 1975 | 8 | Unique two-chip architecture |
| **F100-L** | Ferranti | 1976 | 16 | British military processor |
| **6100** | Intersil | 1975 | 12 | PDP-8 on a chip |
| **R2000** | MIPS | 1985 | 32 | RISC pioneer |
| **R3000** | MIPS | 1988 | 32 | Widely used RISC |
| **R4000** | MIPS | 1991 | 64 | First 64-bit MIPS |
| **R4400** | MIPS | 1993 | 64 | Enhanced R4000 |
| **SPARC** | Sun | 1987 | 32 | Register-window RISC |
| **SuperSPARC** | Sun | 1992 | 32 | Superscalar SPARC |
| **PA-7100** | HP | 1992 | 32 | PA-RISC |
| **Alpha 21064** | DEC | 1992 | 64 | Fastest CPU of its era |
| **Alpha 21164** | DEC | 1995 | 64 | Superscalar Alpha |
| **VAX-11/780** | DEC | 1977 | 32 | "1 MIPS" reference machine |
| **MicroVAX** | DEC | 1984 | 32 | Single-chip VAX |
| **POWER1** | IBM | 1990 | 32 | RS/6000 processor |
| **POWER2** | IBM | 1993 | 32 | Enhanced POWER |
| **PowerPC 604** | IBM/Moto | 1994 | 32 | High-performance PPC |
| **CP1600** | GI | 1975 | 16 | Intellivision game console |
| **PIC1650** | GI | 1977 | 8 | First PIC microcontroller |
| **PIC16C84** | Microchip | 1993 | 8 | Flash-based PIC |
| **ADSP-2100** | AD | 1986 | 16 | Analog Devices DSP |
| **DSP56001** | AT&T | 1987 | 32 | DSP32C family |
| **WE32000** | AT&T | 1982 | 32 | Bell Labs BELLMAC |
| **i960** | Various | 1990 | 32 | Embedded RISC |
| **Transputer T800** | Inmos | 1987 | 32 | Parallel processing pioneer |
| **SC61860** | Sharp | 1982 | 8 | Pocket computer CPU |
| **2650** | Signetics | 1975 | 8 | Innovative but unsuccessful |
| **CDP1802** | Harris | 1990 | 8 | Harris rad-hard remake |
| *+156 additional models* | Various | 1970-1995 | Various | See individual directories |

---

## Models by Architecture

### 4-Bit Processors (~25 models)
- Intel: 4004, 4040
- TI: TMS1000, TMS1100, TMS1400
- AMI: S2000 family (6)
- Fujitsu: MB884x arcade family (5)
- National: COP400 family
- Rockwell: PPS-4
- Toshiba: T3444
- Various: Calculator and arcade custom chips

### 8-Bit Processors (~130 models)
- Intel: 8008, 8080, 8085, 8085a, 8035, 8039, 8048, 8049, 8051, 8052, 8061
- Motorola: 6800, 6801, 6802, 6803, 6805, 6809, 6811, 68HC05, 68HC08, 68HC11
- MOS/WDC: 6502, 6507, 6510, 65C02
- Zilog: Z80, Z80A, Z80B, Z80H, Z180, Z8, eZ80
- RCA: 1802, CDP1802A, CDP1804, CDP1805, CDP1806
- NEC: uPD780, uPD8080, 78K0
- Hitachi: 6309, 6301, 6303, 63C09, HD64180, HD6413xx
- Rockwell: PPS-8, R6502, R6511, R65C02
- Eastern Bloc: U880, U880D, U8820, KR580VM80A, Tesla MHB8080, CEMI MCY7880, MMN80CPU
- Others: F8, 2650, NSC800, TMS7000, PIC1650, SC61860, TLCS-90, TLCS-870

### 12-Bit Processors (~3 models)
- Intersil 6100 (PDP-8 compatible)
- PDP-8 variants

### 16-Bit Processors (~80 models)
- Intel: 8086, 8088, 80186, 80188, 80286, 8096, 8196
- Motorola: 68000, 68008, 68010, 68HC12, 68HC16
- MOS/WDC: 65802, 65816
- Zilog: Z280, Z8000, Z8001, Z8002
- TI: TMS9900, TMS9980, TMS9995, TMS9940, MSP430
- NEC: V20, V25, V30, V33, V40, V50, 78K4
- National: NS32008
- Hitachi: H8/300, H8/500, HD63484
- Eastern Bloc: T34VM1, KR1810VM86, 1839VM1, KR1801VM1
- Others: F100-L, CP1600

### 32-Bit Processors (~110 models)
- Intel: 80386, 80386SX, 80486, 80486DX2, 80486DX4, Pentium, Pentium Pro, iAPX 432, i960
- Motorola: 68020, 68030, 68040, 68060, ColdFire, 88000, 88100, 88110, PowerPC 601, 603
- AMD: Am29000, Am29050, Am386, Am486, Am5x86
- ARM: ARM1, ARM2, ARM3, ARM6, ARM7, ARM7TDMI, ARM610
- National: NS32016, NS32032, NS32332, NS32532, CompactRISC
- NEC: V60, V70, V810, V850
- Hitachi: SH-1, SH-2, SH-3
- MIPS: R2000, R3000
- TI: TMS320C30, TMS320C40
- Others: SPARC, SuperSPARC, PA-7100, POWER1, POWER2, PowerPC 604, VAX, MicroVAX, WE32000, Transputer T800, Toshiba TX39

### 64-Bit Processors (~10 models)
- Intel: i860
- MIPS: R4000, R4400
- DEC: Alpha 21064, Alpha 21164
- Eastern Bloc: Elbrus-1, Elbrus-2
- Others: early 64-bit RISC designs

### DSP Processors (~22 models)
- TI: TMS320C10, C25, C30, C40, C50, C54x
- Motorola: DSP56001, 56002
- NEC: uPD7720, uPD7725
- Analog Devices: ADSP-2100 family
- AT&T: DSP32C family
- Others: Application-specific DSPs

### Bit-Slice Processors (~8 models)
- AMD: Am2901, Am2903, Am2910, Am29116
- TI: SN74181
- Others: Custom bit-slice designs

### Special Categories
- **Arcade Custom**: Namco CUS47/C65/C68/C70/C140, Fujitsu MB884x
- **Calculator**: AMI S2000 family
- **Communications**: Motorola 68302

---

## Models by Application Domain

### Personal Computers
- Intel 8080 (Altair), 8088 (IBM PC), 80286 (IBM AT), 80386/486/Pentium
- Zilog Z80 (CP/M machines, TRS-80)
- MOS 6502 (Apple II, Commodore 64)
- Motorola 68000 (Macintosh, Amiga, Atari ST), 68030/68040 (Mac II/Quadra)
- PowerPC 601/603 (Power Macintosh)
- DEC Alpha (DEC workstations)
- SPARC (Sun workstations)

### Game Consoles
- MOS 6502/6507 (NES, Atari 2600)
- GI CP1600 (Intellivision)
- WDC 65816 (Super Nintendo)
- Motorola 68000 (Sega Genesis)
- Hitachi SH-2 (Sega Saturn)
- NEC V810 (Virtual Boy)
- ARM7TDMI (Game Boy Advance)

### Arcade Systems
- Namco CUS47/C65/C68 (Namco System 1/2)
- Fujitsu MB884x (Various arcade boards)
- Motorola 68000 (Numerous arcade boards)
- Hitachi 6301 (Sega arcade)

### Space / Military
- RCA 1802/1804/1805/1806 (Voyager, New Horizons)
- Ferranti F100-L (Tornado, Rapier)
- Various rad-hard and mil-spec processors

### Automotive
- Intel 8096 (Engine control, dominant 1985-2005)
- Motorola 68HC11 (Automotive systems)
- NEC V850 (Automotive embedded)
- Hitachi SH series (Automotive ECU)

### Consumer Electronics
- TI TMS1000 (Calculators, Speak & Spell)
- Intel 8048/8051 (Keyboards, appliances)
- Sharp SC61860 (Pocket computers)
- AMI S2000 (Calculators)

### Digital Signal Processing
- TI TMS320 family (Audio, telecom, modems)
- Motorola DSP56001 (Audio processing)
- NEC uPD7720/7725 (Audio/SNES DSP)
- Analog Devices ADSP-2100 (Instrumentation)

### Telecommunications
- Motorola 68302 (Networking equipment)
- TI TMS320C54x (Cell phones)
- Various embedded controllers

---

## File Structure

Each model folder contains:

```
[processor]/
├── current/
│   └── [processor]_validated.py        # Active model (edit this)
├── validation/
│   └── [processor]_validation.json     # Validation data and accuracy metrics
├── measurements/                       # Calibration input data
│   ├── measured_cpi.json               #   Per-workload CPI measurements
│   ├── benchmarks.json                 #   Benchmark scores
│   └── instruction_traces.json         #   Instruction mix data
├── identification/                     # System identification results
│   └── sysid_result.json              #   Fitted correction terms
├── docs/                               # Architecture documentation
├── README.md                           # Quick reference, validation status
├── CHANGELOG.md                        # Cumulative history (append-only)
└── HANDOFF.md                          # Current state + next steps
```

---

## Usage

### Running a Model

```python
import sys
sys.path.insert(0, 'models/[family]/[processor]/current')
from [processor]_validated import [Processor]Model

model = [Processor]Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi:.3f}, IPC: {result.ipc:.3f}, MIPS: {result.mips:.3f}")
```

### Running All Workloads

```python
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Jan 2026 | Initial collection, 65 models |
| 2.0 | Jan 2026 | Phase 2 expansion, ~130 models |
| 3.0 | Jan 2026 | Phase 3, ~220 models, new families |
| 4.0 | Jan 2026 | Phase 5, ~321 models, 19 families |
| 5.0 | Jan 30, 2026 | **422 models**, Phase 6 complete |

---

## References

- Intel Microprocessor Quick Reference Guide
- Motorola M68000 Family Programmer's Reference
- Zilog Z80 CPU User Manual
- MOS 6502 Programming Manual
- ARM Architecture Reference Manual
- TI TMS320 Family User Guides
- NEC V-Series Data Books
- DEC Alpha Architecture Handbook
- MIPS R-Series Programmer's Manual
- Various academic papers on processor performance modeling
- Bitsavers.org archival documentation

---

**Collection Maintainer:** Grey-Box Performance Modeling Research
**Last Updated:** January 30, 2026
**Status:** All 422 models validated with <5% CPI error
