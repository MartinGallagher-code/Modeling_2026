# Zilog Z280

**Enhanced Z80 with MMU, 256-byte cache, and on-chip peripherals**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Zilog |
| Year | 1985 |
| Data Width | 8-bit |
| Clock | 10.0 MHz |
| Technology | CMOS |
| Transistors | ~68,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.5 |
| Predicted CPI | 5.000 |
| Error | 11.11% |
| Status | **MARGINAL** |

## Files

- `current/z280_validated.py` - Active grey-box queueing model
- `validation/z280_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/zilog/z280/current')
from z280_validated import Z280Model

model = Z280Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
