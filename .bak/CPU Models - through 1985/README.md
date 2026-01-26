# Pre-1986 Microprocessor Unified Modeling Interface

## Overview

A **single interface** to access all performance modeling capabilities for the complete collection of **62 pre-1986 microprocessors**.

Provides:
- **Queueing Theory** models (bottleneck identification)
- **CPI Stack** analysis (penalty breakdown)
- **Processor comparison** across families
- **What-if analysis** for design exploration
- **Export** to JSON/CSV

---

## Quick Start

### Python API

```python
from pre1986_unified import ModelingInterface

# Create interface
interface = ModelingInterface()

# List processors
processors = interface.list_processors()

# Analyze a processor
result = interface.analyze("Intel 8086")
interface.print_result(result)

# Compare processors
results = interface.compare(["Intel 8080", "Zilog Z80", "MOS 6502"])
interface.print_comparison(results)

# What-if analysis
whatif = interface.what_if("Intel 8086", "clock_mhz", [5, 8, 10])
```

### Command Line

```bash
# Analyze single processor
python pre1986_unified.py --processor "Intel 8086"

# Compare processors
python pre1986_unified.py --compare "Intel 8080,Zilog Z80,MOS 6502"

# Compare all processors
python pre1986_unified.py --all

# Export results
python pre1986_unified.py --all --export results.csv

# Interactive mode
python pre1986_unified.py --interactive

# List all processors
python pre1986_unified.py --list
```

---

## Sample Output

### Single Processor Analysis

```
======================================================================
  Intel 8086
  Foundation of x86 architecture
======================================================================

  Year: 1978  |  16-bit  |  5.0 MHz  |  Intel

  ┌─ QUEUEING MODEL ────────────────────────────────────────────────┐
  │  IPC: 0.1709  |  MIPS: 0.855  |  Bottleneck: execution_unit     │
  └──────────────────────────────────────────────────────────────────┘

  ┌─ CPI STACK ─────────────────────────────────────────────────────┐
  │  IPC: 0.1443  |  MIPS: 0.722  |  CPI: 6.93  |  Penalty: memory   │
  │                                                                  │
  │  Component          CPI      %  Bar                              │
  │  -------------------------------------------------------------- │
  │  base              5.85  84.4%  █████████████████████████        │
  │  branch            0.36   5.2%  █                                │
  │  memory            0.72  10.4%  ███                         ←    │
  └──────────────────────────────────────────────────────────────────┘

  SUMMARY: IPC=0.1576, MIPS=0.788
```

### Processor Comparison

```
==========================================================================================
PROCESSOR COMPARISON
==========================================================================================

Processor                     Year  Bits    MHz     IPC     MIPS Bottleneck  
------------------------------------------------------------------------------------------
MIPS R2000                    1985    32    8.0  0.7013    5.611 cache       
ARM1                          1985    32    6.0  0.5070    3.042 branch      
Motorola 68000                1979    32    8.0  0.1526    1.221 prefetch    
Intel 8086                    1978    16    5.0  0.1576    0.788 memory      
Zilog Z80                     1976     8    2.5  0.1747    0.437 memory      
Intel 8080                    1974     8    2.0  0.1674    0.335 memory      
MOS 6502                      1975     8    1.0  0.3262    0.326 memory      
------------------------------------------------------------------------------------------
```

---

## Supported Processors (62)

### By Family

| Family | Count | Examples |
|--------|-------|----------|
| Intel | 18 | 4004, 8080, 8086, 80386 |
| Motorola | 12 | 6800, 6809, 68000, 68020 |
| MOS/WDC | 4 | 6502, 65c02, 65816 |
| Zilog | 6 | Z80, Z180, Z8000 |
| RCA | 4 | 1802, CDP1804-1806 |
| TI | 4 | TMS1000, TMS9900 |
| National | 3 | NSC800, NS32016 |
| NEC | 2 | V20, V30 |
| Other | 9 | AMD 2901, ARM1, MIPS R2000 |

### By Category

| Category | Count | Examples |
|----------|-------|----------|
| 4-bit | 3 | 4004, 4040, TMS1000 |
| Simple 8-bit | 7 | 8080, 6502, 6800 |
| Enhanced 8-bit | 5 | Z80, 6809, 6309 |
| 8-bit MCU | 10 | 8051, 8048, PIC |
| 16-bit Prefetch | 6 | 8086, 8088, V20 |
| 16-bit Protected | 2 | 80286, Z280 |
| Early 32-bit | 8 | 68000, Z8000, TMS9900 |
| Full 32-bit | 4 | 80386, 68020, NS32032 |
| RISC | 2 | ARM1, MIPS R2000 |
| Special | 6 | 1802, iAPX 432, AMD 2901 |

---

## API Reference

### ModelingInterface Class

#### Listing Methods

```python
list_processors(family=None, category=None, year_range=None, bits=None)
list_families()
list_categories()
list_workloads()
get_processor_info(processor)
```

#### Analysis Methods

```python
analyze(processor, workload="typical", model=ModelType.BOTH)
compare(processors, workload="typical", model=ModelType.BOTH)
compare_all(workload="typical", model=ModelType.BOTH)
what_if(processor, parameter, values, workload="typical")
```

#### Output Methods

```python
print_result(result, detailed=True)
print_comparison(results, sort_by="mips")
export_json(results, filename)
export_csv(results, filename)
```

### Model Types

```python
ModelType.QUEUEING   # Run only queueing model
ModelType.CPI_STACK  # Run only CPI Stack model
ModelType.BOTH       # Run both models (default)
```

### Workloads

| Name | Description |
|------|-------------|
| typical | Typical mixed workload |
| compute | High ALU, low memory |
| memory | High memory, low ALU |
| control | High branch rate |
| string | String processing pattern |

---

## Interactive Mode

```
> list
Processors (62):
  AMD 2901
  ARM1
  ...

> info Intel 8086
Intel 8086:
  family: Intel
  category: 16-bit with Prefetch
  year: 1978
  bits: 16
  clock_mhz: 5.0
  ...

> analyze Intel 8086
[Full analysis output]

> compare Intel 8080,Zilog Z80,MOS 6502
[Comparison table]

> quit
Goodbye!
```

---

## Files

| File | Description |
|------|-------------|
| `pre1986_unified.py` | Main unified interface |
| `README.md` | This documentation |

---

## Two Models, Complete Insight

| Model | Question | Answer Type |
|-------|----------|-------------|
| **Queueing** | "What resource is saturated?" | Bottleneck identification |
| **CPI Stack** | "Where do the cycles go?" | Penalty breakdown |

**Use both together for complete performance understanding!**

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial release with 62 processors |

---

**Collection:** Grey-Box Performance Modeling Research  
**Last Updated:** January 25, 2026
