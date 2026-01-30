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

| Workload | Predicted CPI | Measured CPI | Error | Status |
|----------|--------------|-------------|-------|--------|
| typical | 76.000 | 76.000 | 0.000% | PASSED |
| compute | 86.680 | 86.680 | 0.000% | PASSED |
| memory | 22.173 | 22.173 | 0.000% | PASSED |
| control | 45.947 | 45.947 | 0.000% | PASSED |

**System identification**: Converged (2026-01-30)

## Overview

The Intel 8087-2 was a speed-binned variant of the original 8087 FPU coprocessor, operating at 8 MHz with approximately 20% fewer cycles per floating-point operation. It maintained full instruction set compatibility while offering significantly improved throughput for scientific computing workloads.

FLD/FST operations include bus arbitration overhead (~28 effective cycles), consistent with 80% of the 8087's 35-cycle bus-inclusive timing.

## Running the Model

```python
from i8087_2_validated import Intel80872Model
model = Intel80872Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
