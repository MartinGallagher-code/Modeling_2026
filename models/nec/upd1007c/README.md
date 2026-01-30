# NEC uPD1007C

**NEC calculator CPU for Casio calculators (1978)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1978 |
| Data Width | 4-bit |
| Clock | 500 kHz |
| Transistors | ~6,000 |
| CPI | 6.0 (typical) |
| Performance | ~83 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/upd1007c_validated.py` - Active model
- `validation/upd1007c_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from upd1007c_validated import Upd1007cModel

model = Upd1007cModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

Custom NEC CMOS calculator CPU designed for Casio scientific and programmable
calculators. 4-bit data path with native BCD arithmetic and integrated
LCD/LED display driver. Low-power CMOS design optimized for battery operation
in handheld devices.
