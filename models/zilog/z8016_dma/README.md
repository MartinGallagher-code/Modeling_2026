# Zilog Z8016 - DMA Transfer Controller

| Property | Value |
|----------|-------|
| **Manufacturer** | Zilog |
| **Year** | 1981 |
| **Clock** | 4 MHz |
| **Transistors** | ~10,000 |
| **Data Width** | 16-bit |
| **Address Width** | 16-bit |
| **Category** | Coprocessor / DMA Controller |

## Validation Status

| Metric | Value |
|--------|-------|
| **Target CPI** | 4.0 |
| **Predicted CPI** | 4.0 |
| **Error** | 0.00% |
| **Status** | PASSED |

## Overview

The Z8016 was a DMA controller designed for Zilog's Z8000 family. It provided programmable DMA transfers with block, burst, and continuous modes, as well as hardware search-and-match capability. It supported chained transfers for scatter-gather operations.

## Running the Model

```python
from z8016_dma_validated import ZilogZ8016DMAModel
model = ZilogZ8016DMAModel()
result = model.analyze('typical')
print(f"CPI={result.cpi:.2f}, IPC={result.ipc:.4f}")
```
