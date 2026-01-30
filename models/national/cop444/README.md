# National COP444

**Top-end COP4xx with 2KB ROM and 160 nibbles RAM**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1982 |
| Data Width | 4-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~8,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/cop444_validated.py` - Active grey-box queueing model
- `validation/cop444_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/national/cop444/current')
from cop444_validated import Cop444Model

model = Cop444Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
