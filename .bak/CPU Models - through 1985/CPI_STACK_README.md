# CPI Stack Models for Pre-1986 Processors

## Overview

This package adds **CPI Stack analysis** to all 62 processor models in the pre-1986 collection. The CPI Stack approach complements the existing queueing theory models by answering a different question:

| Approach | Question | Insight |
|----------|----------|---------|
| **Queueing Theory** | "What resource is saturated?" | Bottleneck identification |
| **CPI Stack** | "Where do the cycles go?" | Penalty breakdown |

---

## Contents

### Framework File
- `cpi_stack_framework.py` - Universal CPI Stack model with specs for all 62 processors

### Individual Model Files
One `*_cpi_stack.py` file for each processor folder:

```
Models/
├── AMD 2901/amd_2901_cpi_stack.py
├── ARM1/arm1_cpi_stack.py
├── Fairchild F8/fairchild_f8_cpi_stack.py
├── Intel 4004/intel_4004_cpi_stack.py
├── Intel 8080/intel_8080_cpi_stack.py
├── Intel 8086/intel_8086_cpi_stack.py
├── Intel 80386/intel_80386_cpi_stack.py
├── MIPS R2000/mips_r2000_cpi_stack.py
├── Motorola 68000/motorola_68000_cpi_stack.py
├── MOS 6502/mos_6502_cpi_stack.py
├── Zilog Z80/zilog_z80_cpi_stack.py
└── ... (62 total)
```

---

## Installation

Copy the appropriate `*_cpi_stack.py` file into each processor folder alongside the existing queueing model files:

```
Intel 8086/
├── ibm_pc_8086_model.json      # Existing queueing config
├── ibm_pc_8086_model.py        # Existing queueing model
├── intel_8086_cpi_stack.py     # NEW: CPI Stack model
├── README_8086.md
└── QUICK_START_8086.md
```

---

## Usage

### Using Individual Model

```python
from intel_8086_cpi_stack import Intel8086CPIStackModel, WORKLOADS

model = Intel8086CPIStackModel()
result = model.predict(WORKLOADS["typical"])
model.print_result(result)
```

### Using Universal Framework

```python
from cpi_stack_framework import UniversalCPIStackModel, STANDARD_WORKLOADS

model = UniversalCPIStackModel()

# Analyze any processor
result = model.predict("Intel 8086")
model.print_result(result)

# Compare processors
results = model.compare_processors(["Intel 8080", "Intel 8086", "Intel 80386"])
```

---

## CPI Components

### For Simple Processors (8080, 6502, Z80, etc.)
- **Base CPI**: Ideal execution from instruction mix
- **Memory penalty**: Extra cycles for memory operands

### For Pipelined Processors (8086, 68000, etc.)
- **Base CPI**: Ideal execution
- **Prefetch penalty**: Stalls waiting for instruction bytes
- **Branch penalty**: Pipeline flush on taken branches
- **Memory penalty**: Memory operand delays

### For Advanced Processors (80386, 68020, ARM1, MIPS R2000)
- **Base CPI**: Ideal execution
- **Prefetch penalty**: Instruction supply stalls
- **Branch penalty**: Misprediction/flush costs
- **Memory penalty**: Memory access delays
- **Cache penalty**: Miss costs (if applicable)
- **Pipeline penalty**: Hazards and stalls

---

## Sample Output

```
=======================================================
CPI STACK: Intel 8086
=======================================================

Component          CPI      %  Bar
--------------------------------------------------
Base (ideal)      5.85  84.4%  █████████████████████████
Branch            0.36   5.2%  █
Memory            0.72  10.4%  ███ ←
--------------------------------------------------
TOTAL             6.93 100.0%

IPC: 0.1443  |  MIPS: 0.722
Primary penalty: memory
```

---

## Processor Coverage

| Category | Count | Examples |
|----------|-------|----------|
| 4-bit | 3 | 4004, 4040, TMS1000 |
| Simple 8-bit | 10 | 8080, 6502, 6800, F8 |
| Enhanced 8-bit | 6 | Z80, 6809, 6309, 65c02 |
| 8-bit MCU | 12 | 8051, 8048, PIC1650 |
| Prefetch 16-bit | 8 | 8086, 8088, V20, V30 |
| Protected 16-bit | 2 | 80286, Z280 |
| Early 32-bit | 8 | 68000, Z8000, TMS9900 |
| Full 32-bit | 5 | 80386, 68020, NS32032 |
| RISC | 2 | ARM1, MIPS R2000 |
| Special | 6 | 1802, iAPX 432, AMD 2901 |
| **Total** | **62** | |

---

## Combined Analysis Approach

For complete insight, use BOTH models:

```python
# Queueing model
from ibm_pc_8086_model import Intel8086QueueModel
qmodel = Intel8086QueueModel('ibm_pc_8086_model.json')
q_ipc, q_metrics = qmodel.predict_ipc(arrival_rate=0.10)

# CPI Stack model  
from intel_8086_cpi_stack import Intel8086CPIStackModel
cpi_model = Intel8086CPIStackModel()
cpi_result = cpi_model.predict()

# Combined insight
print(f"Queueing:  IPC={q_ipc:.4f}, Bottleneck={q_metrics[0].name}")
print(f"CPI Stack: IPC={cpi_result.ipc:.4f}, Penalty={cpi_result.bottleneck}")
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 2026 | Initial CPI Stack models for all 62 processors |

---

**Collection:** Grey-Box Performance Modeling Research  
**Last Updated:** January 25, 2026
