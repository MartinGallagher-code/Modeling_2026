# Plessey MIPROC

**PDP-11 compatible 16-bit processor for NATO crypto (1975)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1975 |
| Data Width | 16-bit |
| Clock | 5 MHz |
| CPI | ~5.0 cycles |
| Performance | ~1.0 MIPS |
| Transistors | ~8,000 |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 3.0% |
| Tests Passing | 7/7 |

## Model Files

- `current/miproc_validated.py` - Active model
- `validation/miproc_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from miproc_validated import MiprocModel

model = MiprocModel()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The Plessey MIPROC was a single-chip PDP-11 compatible processor developed
by Plessey Semiconductors for military and defense applications. It was
notably used in NATO cryptographic equipment, leveraging the well-proven
PDP-11 instruction set architecture. With ~8000 transistors and 5 MHz
clock, it provided minicomputer-class computing in a single chip for
secure communications applications.
