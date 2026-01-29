# KR1858VM1 (T34VM1)

**Soviet Z80 clone derived from East German U880 masks (1991)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1991 |
| Data Width | 8-bit |
| Clock | 4.0 MHz |
| CPI | ~5.5 |
| Performance | ~0.73 MIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 1.55% |
| Tests Passing | 15/15 |

## Model Files

- `current/kr1858vm1_validated.py` - Active model
- `validation/kr1858vm1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from kr1858vm1_validated import KR1858VM1Model

model = KR1858VM1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi}, IPS: {result.ips:,.0f}")
```

## Notes

The KR1858VM1 (also known as T34VM1) was one of the last Soviet-era processor
designs, produced in 1991. It is a Z80 clone derived from East German U880
photomasks. The processor maintains full timing and instruction set compatibility
with the Zilog Z80. It was used in late Soviet-era computers and industrial
controllers during the final years of the USSR.
