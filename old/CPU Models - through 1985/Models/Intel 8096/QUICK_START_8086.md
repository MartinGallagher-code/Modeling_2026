# Intel 8086 - Quick Start

## Dual Model Approach

| Model | Question | File |
|-------|----------|------|
| **Queueing** | "What's the bottleneck?" | `ibm_pc_8086_model.py` |
| **CPI Stack** | "Where do cycles go?" | `ibm_pc_8086_cpi_stack.py` |
| **Unified** | Both together | `ibm_pc_8086_unified.py` |

## Fastest Start

```python
from ibm_pc_8086_unified import Intel8086UnifiedModel, WORKLOADS

model = Intel8086UnifiedModel()
result = model.analyze(WORKLOADS["dos_typical"])
model.print_combined_analysis(result)
```

## Key Specs

| Spec | Value |
|------|-------|
| Clock | 5-10 MHz |
| Bus | 16-bit |
| Prefetch | 6 bytes |
| IPC | ~0.10 |
| MIPS | ~0.5 @ 5MHz |

## CPI Breakdown (Typical)

| Component | % |
|-----------|---|
| Base execution | 90% |
| EA calculation | 4% |
| Branches | 3% |
| Bus contention | 2% |
| Other | 1% |

## Optimization

- **EA penalties high?** → Use simpler addressing
- **Branch penalties high?** → Reduce conditionals  
- **Bus contention?** → Use registers more

---

*Use both models together for complete insight!*
