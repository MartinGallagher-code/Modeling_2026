# NEC uPD546

**Early NEC 4-bit MCU for calculators and appliances**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | NEC |
| Year | 1975 |
| Data Width | 4-bit |
| Clock | 0.5 MHz |
| Technology | NMOS |
| Transistors | ~3,500 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.200 |
| Error | 4.00% |
| Status | **PASSED** |

## Files

- `current/upd546_validated.py` - Active grey-box queueing model
- `validation/upd546_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/nec/upd546/current')
from upd546_validated import Upd546Model

model = Upd546Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
