# NEC uPD7810

**Enhanced uPD7801 with 16-bit operations**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 6.0 MHz |
| Technology | NMOS |
| Transistors | ~20,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.900 |
| Error | 7.27% |
| Status | **MARGINAL** |

## Files

- `current/upd7810_validated.py` - Active grey-box queueing model
- `validation/upd7810_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/nec/upd7810/current')
from upd7810_validated import Upd7810Model

model = Upd7810Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
