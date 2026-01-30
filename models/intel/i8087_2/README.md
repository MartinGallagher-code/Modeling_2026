# Intel 8087-2 - Fast x87 FPU Coprocessor

| Property | Value |
|----------|-------|
| **Manufacturer** | Intel |
| **Year** | 1982 |
| **Clock** | 8 MHz |
| **Transistors** | ~45,000 |
| **Data Width** | 80-bit internal |
| **Address Width** | 20-bit |
| **Category** | Coprocessor / FPU |

## Validation Status

| Metric | Value |
|--------|-------|
| **Target CPI** | 76.0 |
| **Predicted CPI** | 76.0 |
| **Error** | 0.00% |
| **Status** | PASSED |

## Overview

The Intel 8087-2 was a speed-binned variant of the original 8087 FPU coprocessor, operating at 8 MHz with approximately 20% fewer cycles per floating-point operation. It maintained full instruction set compatibility while offering significantly improved throughput for scientific computing workloads.

## Running the Model

```python
from i8087_2_validated import Intel80872Model
model = Intel80872Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
