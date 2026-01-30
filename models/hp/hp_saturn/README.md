# HP Saturn

**Custom HP calculator CPU with 64-bit registers (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 4-bit (64-bit registers) |
| Clock | 640 kHz |
| Transistors | ~40,000 |
| CPI | 8.0 (typical) |
| Performance | ~80 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 8/8 |

## Model Files

- `current/hp_saturn_validated.py` - Active model
- `validation/hp_saturn_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from hp_saturn_validated import HpSaturnModel

model = HpSaturnModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

Custom CMOS CPU designed by HP for their calculator line. Features a unique
nibble-serial architecture with 4-bit data path but 64-bit registers (16
nibbles). Native BCD arithmetic provides calculator-grade decimal precision.
Used in the HP 71B, HP 48 series, and HP 49 series. Later versions (Lewis,
Sacajawea) clocked up to 4 MHz.
