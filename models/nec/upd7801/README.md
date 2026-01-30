# NEC uPD7801

**NEC proprietary 8-bit MCU with large Japanese market share**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Technology | NMOS |
| Transistors | ~15,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 6.0 |
| Predicted CPI | 6.500 |
| Error | 8.33% |
| Status | **MARGINAL** |

## Files

- `current/upd7801_validated.py` - Active grey-box queueing model
- `validation/upd7801_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/nec/upd7801/current')
from upd7801_validated import Upd7801Model

model = Upd7801Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
