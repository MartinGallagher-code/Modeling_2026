# Matsushita MN10200

**16-bit MCU for VCRs and camcorders**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Matsushita (Panasonic) |
| Year | 1985 |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| Technology | CMOS |
| Transistors | ~25,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/mn10200_validated.py` - Active grey-box queueing model
- `validation/mn10200_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/mn10200/current')
from mn10200_validated import Mn10200Model

model = Mn10200Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
