# K1801VM3

**Final Soviet PDP-11 compatible microprocessor (1985)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1985 |
| Data Width | 16-bit |
| Clock | 10.0 MHz |
| CPI | ~3.2 |
| Performance | ~3.125 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 0.0% |
| Tests Passing | 15/15 |

## Model Files

- `current/k1801vm3_validated.py` - Active model
- `validation/k1801vm3_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from k1801vm3_validated import K1801VM3Model

model = K1801VM3Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The K1801VM3 was the final and most advanced Soviet PDP-11 compatible processor,
produced in 1985. With 40,000 transistors at 10 MHz and pipelined execution,
it achieved significantly better performance than its predecessors. It was used
in advanced DVK systems and the Elektronika-85 computer.
