# Cross-Validation Guide

This guide explains how to cross-validate the grey-box queueing models against cycle-accurate emulators and other reference sources.

## Purpose

Cross-validation ensures our CPI predictions match real-world processor behavior by comparing against:
1. Cycle-accurate emulators (most accurate)
2. Original manufacturer datasheets
3. Benchmark results from period publications
4. Modern emulator timing measurements

## Recommended Emulators by Processor Family

### Intel

| Processor | Emulator | Notes |
|-----------|----------|-------|
| i8080, i8085 | [MAME](https://www.mamedev.org/) | Cycle-accurate 8080/8085 cores |
| i8086, i8088 | [PCem](https://pcem-emulator.co.uk/), [86Box](https://86box.net/) | IBM PC emulation |
| i80286, i80386 | [86Box](https://86box.net/), [PCem](https://pcem-emulator.co.uk/) | AT-class machines |
| i80486, Pentium | [86Box](https://86box.net/) | Modern x86 emulation |
| i8048, i8051 | [MAME](https://www.mamedev.org/) | MCU cores |

### Motorola

| Processor | Emulator | Notes |
|-----------|----------|-------|
| 6800, 6802, 6809 | [MAME](https://www.mamedev.org/) | Multiple arcade/computer systems |
| 68000 series | [Hatari](https://hatari.tuxfamily.org/) (Atari ST), [FS-UAE](https://fs-uae.net/) (Amiga) | 68000-68060 |
| 68HC11 | [THRSim11](http://www.intec.ugent.be/THRSim11/) | Free educational simulator |

### MOS/WDC

| Processor | Emulator | Notes |
|-----------|----------|-------|
| 6502 | [VICE](https://vice-emu.sourceforge.io/) (C64), [Mesen](https://www.mesen.ca/) (NES) | Cycle-accurate |
| 65C02 | [MAME](https://www.mamedev.org/), Apple IIc emulators | WDC variant |
| 65816 | [bsnes](https://github.com/bsnes-emu/bsnes) (SNES) | Cycle-accurate |

### Zilog

| Processor | Emulator | Notes |
|-----------|----------|-------|
| Z80 | [MAME](https://www.mamedev.org/), [Fuse](http://fuse-emulator.sourceforge.net/) (ZX Spectrum) | Very accurate |
| Z8000 | Limited options | Check MAME |

### Other Processors

| Processor | Emulator | Notes |
|-----------|----------|-------|
| RCA 1802 | [Emma 02](http://www.dvq.com/v2/members/emma02) | COSMAC emulator |
| TMS9900 | [Classic99](http://harmlesslion.com/software/classic99) | TI-99/4A emulator |
| ARM | [MAME](https://www.mamedev.org/) | Archimedes, RISC PC |
| SPARC | [QEMU](https://www.qemu.org/) | SPARCstation |
| MIPS R2000/R3000 | [PCSX](https://www.emulator-zone.com/doc.php/psx/) | PlayStation (R3000) |

## Cross-Validation Process

### Step 1: Select Test Programs

Choose small, timing-sensitive programs:
- **Tight loops** - measure pure execution speed
- **Memory copy** - tests load/store timing
- **Bubble sort** - mix of control flow and memory
- **Dhrystone** - standardized benchmark (if available for processor)

### Step 2: Measure in Emulator

```
1. Load test program into emulator
2. Set breakpoints at start/end
3. Record cycle count (most emulators show this)
4. Calculate actual CPI = total_cycles / instruction_count
```

### Step 3: Compare with Model

```python
# Example validation script
from [processor]_validated import [Processor]Model

model = [Processor]Model()
result = model.analyze('typical')

print(f"Model CPI: {result.cpi:.3f}")
print(f"Emulator CPI: {emulator_cpi:.3f}")
print(f"Error: {abs(result.cpi - emulator_cpi) / emulator_cpi * 100:.1f}%")
```

### Step 4: Adjust if Needed

If error > 5%:
1. Check instruction category cycle counts against datasheet
2. Verify workload profile weights match test program
3. Consider adding new instruction categories if needed

## Reference Sources

### Datasheets
- [Bitsavers](https://bitsavers.org/) - Scanned original datasheets
- [CPU-World](https://www.cpu-world.com/) - Specifications database

### Technical Documentation
- [WikiChip](https://en.wikichip.org/) - Detailed processor articles
- [Wikipedia](https://en.wikipedia.org/) - Good starting point

### Period Publications
- BYTE Magazine archives
- IEEE Micro articles
- ACM Computing Surveys

## Validation Status

Track cross-validation results in each processor's `validation/*.json` file:

```json
{
  "cross_validation": {
    "emulator": "MAME 0.250",
    "test_program": "tight_loop.asm",
    "emulator_cpi": 4.2,
    "model_cpi": 4.0,
    "error_percent": 4.8,
    "validated_date": "2026-01-28"
  }
}
```

## Priority Processors for Cross-Validation

High priority (widely emulated, good references):
1. **Z80** - Fuse emulator is cycle-accurate
2. **6502** - VICE and Mesen are excellent
3. **68000** - Hatari and FS-UAE are well-tested
4. **8086/8088** - 86Box is very accurate

Medium priority:
5. **6809** - MAME has good cores
6. **8051** - MAME MCU emulation
7. **ARM2/ARM3** - MAME Archimedes

Lower priority (limited emulator options):
8. **NS32016** - No good emulators
9. **Z80000** - Rare processor
10. **Transputer** - Specialized architecture
