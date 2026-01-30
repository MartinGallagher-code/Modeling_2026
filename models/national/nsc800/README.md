# National NSC800

**Z80-compatible CMOS, used in Epson HX-20 (first laptop) and military**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | National Semiconductor |
| Year | 1979 |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| Technology | CMOS |
| Transistors | ~9,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.860 |
| Error | 6.55% |
| Status | **MARGINAL** |

## Files

- `current/nsc800_validated.py` - Active grey-box queueing model
- `validation/nsc800_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/national/nsc800/current')
from nsc800_validated import Nsc800Model

model = Nsc800Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
