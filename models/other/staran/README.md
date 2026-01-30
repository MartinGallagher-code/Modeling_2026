# Goodyear STARAN

**Associative/bit-serial massively parallel processor, used by NASA**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Goodyear Aerospace |
| Year | 1972 |
| Data Width | 1-bit |
| Clock | 5.0 MHz |
| Technology | TTL/MSI |
| Transistors | N/A (board-level) |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 8.0 |
| Predicted CPI | 7.250 |
| Error | 9.38% |
| Status | **MARGINAL** |

## Files

- `current/staran_validated.py` - Active grey-box queueing model
- `validation/staran_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/staran/current')
from staran_validated import StaranModel

model = StaranModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
