# iWarp

**VLIW/systolic array processor, precursor to modern GPU thinking**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Intel/CMU |
| Year | 1985 |
| Data Width | 32-bit |
| Clock | 20.0 MHz |
| Technology | CMOS |
| Transistors | ~200,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 1.5 |
| Predicted CPI | 1.800 |
| Error | 20.00% |
| Status | **MARGINAL** |

## Files

- `current/iwarp_validated.py` - Active grey-box queueing model
- `validation/iwarp_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/iwarp/current')
from iwarp_validated import IwarpModel

model = IwarpModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
