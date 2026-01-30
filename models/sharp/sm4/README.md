# Sharp SM4

**Sharp 4-bit CMOS MCU for calculators and Game & Watch handhelds**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Sharp |
| Year | 1982 |
| Data Width | 4-bit |
| Clock | 0.5 MHz |
| Technology | CMOS |
| Transistors | ~4,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.200 |
| Error | 5.00% |
| Status | **MARGINAL** |

## Files

- `current/sm4_validated.py` - Active grey-box queueing model
- `validation/sm4_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/sm4/current')
from sm4_validated import Sm4Model

model = Sm4Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
