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

| Metric | Value |
|--------|-------|
| **Target CPI** | 95.0 |
| **Predicted CPI** | 95.0 |
| **Error** | 0.00% |
| **Status** | PASSED |

## Overview

The Intel 8087 was the first x87 floating-point coprocessor, designed to work alongside the 8086/8088 processors. It provided 80-bit extended precision floating-point arithmetic with hardware support for addition, multiplication, division, and square root. All FP operations executed sequentially with high cycle counts typical of early hardware FPU implementations.

## Running the Model

```python
from i8087_validated import Intel8087Model
model = Intel8087Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
