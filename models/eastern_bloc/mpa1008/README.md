# MPA1008

**Romanian Z80A clone (1980s)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1982 |
| Data Width | 8-bit |
| Clock | 2.5 MHz |
| CPI | ~5.5 |
| Performance | ~0.455 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/mpa1008_validated.py` - Active model
- `validation/mpa1008_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from mpa1008_validated import MPA1008Model

model = MPA1008Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The MPA1008 was a Romanian clone of the Zilog Z80A microprocessor, produced in
the early 1980s. It was fully compatible with the Z80 instruction set including
block transfer and search operations. It was used in Romanian computer systems
including the CoBra and HC-85 home computers.
