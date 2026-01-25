# Intel 4004 Performance Models

This directory contains performance models for the Intel 4004 processor (world's first commercial microprocessor), organized with both current validated models and archived historical versions.

## Directory Structure

```
4004_models/
├── README.md                       # This file
├── current/                        # Active, validated models
│   └── intel_4004_validated.py     # Primary model (USE THIS)
├── archive/                        # Historical versions (deprecated)
│   └── intel_4004_cpi_stack_v1.py  # Original simplified model
├── validation/                     # Validation data and sources
│   ├── 4004_validated_model.json
│   └── 4004_validation_data.md     # Research compilation
└── docs/                           # Documentation
    └── 4004_improvements_summary.md
```

## Quick Start

```python
# Use the validated model
from current.intel_4004_validated import Intel4004Model, WORKLOADS_4004

# Create model
model = Intel4004Model()

# Analyze performance
result = model.analyze("typical")

print(f"IPS: {result.ips:,.0f}")        # ~74,074
print(f"kIPS: {result.kips:.2f}")       # ~74.07
print(f"MIPS: {result.mips:.4f}")       # ~0.0741
print(f"CPI: {result.cpi_clocks:.1f}")  # ~10.0
print(f"Validation: {result.validation_status}")  # PASS
```

## Model Comparison

| Model | IPS | kIPS | MIPS | Status |
|-------|-----|------|------|--------|
| **intel_4004_validated.py** | 74,074 | 74.07 | 0.074 | ✓ Current |
| intel_4004_cpi_stack_v1.py | ~86,000 | ~86 | ~0.086 | Archived |

## Intel 4004 Specifications

| Parameter | Value |
|-----------|-------|
| Release Date | November 15, 1971 |
| Data Width | 4-bit |
| Clock Frequency | 740 kHz (max) |
| Transistors | 2,300 |
| Process | 10 µm PMOS |
| Package | 16-pin DIP |
| Power | 0.5 W |
| Original Price | $60 |

## Validated Model Features

### Complete Instruction Set
- 46 instructions total
- 40 one-word instructions (8 clocks = 10.8 µs)
- 6 two-word instructions (16 clocks = 21.6 µs)

### Instruction Categories
| Category | Examples | Timing |
|----------|----------|--------|
| Accumulator | IAC, DAC, RAL, RAR | 1 machine cycle |
| ALU | ADD, SUB, ADM, SBM | 1 machine cycle |
| Transfer | LD, XCH, LDM | 1 machine cycle |
| Memory | WRM, RDM, WR0-3, RD0-3 | 1 machine cycle |
| Control | JUN, JMS, JCN, ISZ | 2 machine cycles |

### Workload Profiles
- **typical**: General 4-bit computing
- **compute**: BCD arithmetic heavy (calculator math)
- **control**: Branching and subroutines
- **io_heavy**: Peripheral communication
- **calculator**: Original Busicom 141-PF workload

## Validation Sources

1. **Intel MCS-4 Users Manual** (1971)
2. **Intel 4004 Datasheet**
3. **WikiChip** - en.wikichip.org/wiki/intel/mcs-4/4004
4. **Wikipedia** - en.wikipedia.org/wiki/Intel_4004
5. **e4004.szyc.org** - Instruction set reference

## BCD Addition Benchmark

From the original Intel datasheet:
- Task: Add two 8-digit BCD numbers
- Time: 850 µs
- Machine cycles: 79
- Model prediction: 853.2 µs (0.4% error)

## Why Keep the Archive?

The archived model is retained for:
- **Version history**: Shows modeling evolution
- **Comparison baseline**: Demonstrates validation improvement
- **Educational reference**: Simpler model for learning
- **Fallback**: In case of edge cases

## Running the Models

```bash
# Run validated model with full output
python current/intel_4004_validated.py

# Run archived model (shows deprecation warning)
python archive/intel_4004_cpi_stack_v1.py
```

## Files Description

| File | Purpose |
|------|---------|
| `current/intel_4004_validated.py` | Primary model - use this |
| `archive/intel_4004_cpi_stack_v1.py` | Original simplified model |
| `validation/4004_validated_model.json` | Exported validation data |
| `validation/4004_validation_data.md` | Research sources compilation |
| `docs/4004_improvements_summary.md` | Detailed change documentation |

## Historical Significance

The Intel 4004 was revolutionary:
- **First** commercially available single-chip microprocessor
- Designed for the Busicom 141-PF printing calculator
- Enabled the personal computer revolution
- Established Intel as a microprocessor company

---

**Model Version**: 2.0 (Validated)  
**Last Updated**: January 25, 2026  
**Validation Status**: PASS (22/22 instruction timing tests)
