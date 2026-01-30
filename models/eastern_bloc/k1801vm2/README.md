# K1801VM2

**Enhanced Soviet PDP-11 compatible microprocessor (1983)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1983 |
| Data Width | 16-bit |
| Clock | 8.0 MHz |
| CPI | ~4.0 |
| Performance | ~2.0 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/k1801vm2_validated.py` - Active model
- `validation/k1801vm2_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k1801vm2_validated import K1801VM2Model

model = K1801VM2Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K1801VM2 was an enhanced Soviet PDP-11 compatible processor produced in
1983. Running at 8 MHz with 25,000 transistors, it offered improved performance
over the VM1 including floating point support. It was used in DVK-3 and DVK-4
desktop computer systems.
