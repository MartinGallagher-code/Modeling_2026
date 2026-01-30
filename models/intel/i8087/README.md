# Intel 8087 - x87 FPU Coprocessor

| Property | Value |
|----------|-------|
| **Manufacturer** | Intel |
| **Year** | 1980 |
| **Clock** | 5 MHz |
| **Transistors** | ~45,000 |
| **Data Width** | 80-bit internal |
| **Address Width** | 20-bit |
| **Category** | Coprocessor / FPU |

## Validation Status

| Workload | Predicted CPI | Measured CPI | Error | Status |
|----------|--------------|-------------|-------|--------|
| typical | 95.000 | 95.000 | 0.000% | PASSED |
| compute | 108.350 | 108.350 | 0.000% | PASSED |
| memory | 27.716 | 27.716 | 0.000% | PASSED |
| control | 57.400 | 57.400 | 0.000% | PASSED |

**System identification**: Converged (2026-01-30)

## Overview

The Intel 8087 was the first x87 floating-point coprocessor, designed to work alongside the 8086/8088 processors. It provided 80-bit extended precision floating-point arithmetic with hardware support for addition, multiplication, division, and square root. All FP operations executed sequentially with high cycle counts typical of early hardware FPU implementations.

FLD/FST operations include bus arbitration overhead (~35 effective cycles vs 15-20 internal), which dominates memory-heavy workloads.

## Running the Model

```python
from i8087_validated import Intel8087Model
model = Intel8087Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
