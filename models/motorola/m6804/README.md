# Motorola 6804

**Minimal 8-bit MCU (1KB ROM, 64B RAM), ultra-low-cost applications**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Motorola |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 1.0 MHz |
| Technology | NMOS |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.900 |
| Error | 7.27% |
| Status | **MARGINAL** |

## Files

- `current/m6804_validated.py` - Active grey-box queueing model
- `validation/m6804_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/motorola/m6804/current')
from m6804_validated import M6804Model

model = M6804Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
