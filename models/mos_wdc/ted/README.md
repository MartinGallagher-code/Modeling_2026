# Commodore TED (7360)

**C16/Plus/4 integrated video, sound, and timer controller**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | MOS Technology/Commodore |
| Year | 1984 |
| Data Width | 8-bit |
| Clock | 7 MHz |
| Technology | NMOS |
| Transistors | ~25,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 4.0 |
| Predicted CPI | 4.000 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/ted_validated.py` - Active grey-box queueing model
- `validation/ted_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ted/current')
from ted_validated import TedModel

model = TedModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
