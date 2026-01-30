# TI TMS0800

**Single-chip PMOS calculator IC (1973)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1973 |
| Data Width | 4-bit (serial) |
| Clock | 300 kHz |
| Transistors | ~5,000 |
| CPI | 7.0 (typical) |
| Performance | ~43 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 7/7 |

## Model Files

- `current/tms0800_validated.py` - Active model
- `validation/tms0800_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from tms0800_validated import Tms0800Model

model = Tms0800Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

Single-chip PMOS calculator IC for TI desktop calculators. Features a 4-bit
serial BCD data path with shift registers. Supports 11-digit BCD display
with integrated display scanning and segment driving. Predecessor to the
TMS1000 microcontroller family.
