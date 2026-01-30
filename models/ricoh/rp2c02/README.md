# Ricoh RP2C02 PPU

**NES/Famicom Picture Processing Unit (NTSC)**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ricoh |
| Year | 1983 |
| Data Width | 8-bit |
| Clock | 5.37 MHz |
| Technology | NMOS |
| Transistors | ~16,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 3.5 |
| Predicted CPI | 3.500 |
| Error | 0.0% |
| Status | **PASSED** |

## Files

- `current/rp2c02_validated.py` - Active grey-box queueing model
- `validation/rp2c02_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/rp2c02/current')
from rp2c02_validated import Rp2c02Model

model = Rp2c02Model()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
