# Mostek MK5005

**Early calculator-on-a-chip (1972)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1972 |
| Data Width | 4-bit (serial) |
| Clock | 200 kHz |
| Transistors | ~3,000 |
| CPI | 9.0 (typical) |
| Performance | ~22 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 7/7 |

## Model Files

- `current/mk5005_validated.py` - Active model
- `validation/mk5005_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from mk5005_validated import Mk5005Model

model = Mk5005Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

One of the earliest calculator-on-a-chip designs. PMOS technology with only
~3,000 transistors. 4-bit serial BCD data path with shift-register based
architecture. Includes integrated keyboard scanning and display multiplexing.
High cycle counts reflect the slow PMOS technology of the early 1970s.
