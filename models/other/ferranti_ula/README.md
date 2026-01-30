# Ferranti ULA

**ZX Spectrum ULA, semi-custom gate array for memory/IO/video**

## Quick Reference

| Parameter | Value |
|-----------|-------|
| Manufacturer | Ferranti |
| Year | 1981 |
| Data Width | 8-bit |
| Clock | 3.5 MHz |
| Technology | Gate Array |
| Transistors | ~5,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Expected CPI | 5.0 |
| Predicted CPI | 5.000 |
| Error | 0.00% |
| Status | **PASSED** |

## Files

- `current/ferranti_ula_validated.py` - Active grey-box queueing model
- `validation/ferranti_ula_validation.json` - Validation data
- `CHANGELOG.md` - Complete history
- `HANDOFF.md` - Current state and next steps

## Usage

```python
import sys
sys.path.insert(0, 'models/other/ferranti_ula/current')
from ferranti_ula_validated import FerrantiUlaModel

model = FerrantiUlaModel()
for workload in ['typical', 'compute', 'memory', 'control']:
    result = model.analyze(workload)
    print(f'{workload}: CPI={result.cpi:.3f} IPC={result.ipc:.3f}')
```
