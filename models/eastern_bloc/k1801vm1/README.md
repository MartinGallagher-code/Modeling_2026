# K1801VM1

**Soviet PDP-11 compatible microprocessor (1980)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1980 |
| Data Width | 16-bit |
| Clock | 5.0 MHz |
| CPI | ~5.0 |
| Performance | ~1.0 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/k1801vm1_validated.py` - Active model
- `validation/k1801vm1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k1801vm1_validated import K1801VM1Model

model = K1801VM1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K1801VM1 was the first Soviet single-chip PDP-11 compatible microprocessor,
produced in 1980. It implemented the PDP-11 instruction set with 15,000
transistors at 5 MHz. It was used in DVK desktop computers and Elektronika
systems, providing Soviet institutions with PDP-11 compatible computing
capability.
