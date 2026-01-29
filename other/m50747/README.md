# Mitsubishi M50747

**MELPS 740 8-bit MCU - M50740 variant with expanded I/O (1984)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1984 |
| Data Width | 8-bit |
| Clock | 2 MHz |
| CPI | ~3.2 cycles |
| Performance | ~625 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | <5% |
| Tests Passing | 7/7 |

## Model Files

- `current/m50747_validated.py` - Active model
- `validation/m50747_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from m50747_validated import M50747Model

model = M50747Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The M50747 is a variant of the M50740 with expanded I/O port configuration.
It uses the same MELPS 740 core (enhanced 6502) with identical instruction
timing. The additional I/O ports make it suitable for applications requiring
more peripheral connections.

## Comparison with M50740

| Feature | M50740 | M50747 |
|---------|--------|--------|
| Core | MELPS 740 | MELPS 740 |
| CPI | 3.2 | 3.2 |
| I/O Ports | Standard | Expanded |
| Package | 42-pin DIP | 64-pin QFP |
