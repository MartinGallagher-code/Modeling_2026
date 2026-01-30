# Intel 8089 - I/O Processor

| Property | Value |
|----------|-------|
| **Manufacturer** | Intel |
| **Year** | 1979 |
| **Clock** | 5 MHz |
| **Transistors** | ~40,000 |
| **Data Width** | 16-bit |
| **Address Width** | 20-bit |
| **Category** | Coprocessor / I/O Processor |

## Validation Status

| Metric | Value |
|--------|-------|
| **Target CPI** | 6.5 |
| **Predicted CPI** | 6.5 |
| **Error** | 0.00% |
| **Status** | PASSED |

## Overview

The Intel 8089 was a dedicated I/O processor designed to offload data transfer and channel management from the 8086/8088 host CPU. It featured two independent DMA channels and could execute channel programs autonomously with its own instruction set optimized for I/O operations.

## Running the Model

```python
from i8089_validated import Intel8089Model
model = Intel8089Model()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
