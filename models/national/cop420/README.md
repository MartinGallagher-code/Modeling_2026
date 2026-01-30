# National COP420

**Enhanced COP400 with 1KB ROM and 64 nibbles RAM**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1979 |
| Data Width | 4-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~6,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/cop420_validated.py` - Active grey-box queueing model
- `validation/cop420_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/national/cop420/current')
from cop420_validated import Cop420Model

model = Cop420Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
