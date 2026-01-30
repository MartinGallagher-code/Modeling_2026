# National COP400

**Hugely popular 4-bit MCU, billions manufactured, used in appliances and toys**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1977 |
| Data Width | 4-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/cop400_validated.py` - Active grey-box queueing model
- `validation/cop400_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/national/cop400/current')
from cop400_validated import Cop400Model

model = Cop400Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
