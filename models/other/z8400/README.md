# SGS-Thomson Z8400

**Italian second-source of Zilog Z80, pin-compatible clone**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | SGS-Thomson |
| Year | 1980 |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| Technology | NMOS |
| Transistors | ~8,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.5 |
| Predicted CPI | 5.500 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/z8400_validated.py` - Active grey-box queueing model
- `validation/z8400_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/z8400/current')
from z8400_validated import Z8400Model

model = Z8400Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
