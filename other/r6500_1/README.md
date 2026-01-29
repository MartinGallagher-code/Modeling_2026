# Rockwell R6500/1

**Single-chip 6502 MCU (1978)**

## Quick Reference

| Specification | Value |
|---------------|-------|
| Year | 1978 |
| Data Width | 8-bit |
| Clock | 1 MHz |
| CPI | ~3.0 cycles |
| Performance | ~333 KIPS |

## Validation Status

| Metric | Value |
|--------|-------|
| Status | PASSED |
| CPI Error | 3.33% |
| Tests Passing | 6/6 |

## Model Files

- `current/r6500_1_validated.py` - Active model
- `validation/r6500_1_validation.json` - Validation data
- `CHANGELOG.md` - Full history
- `HANDOFF.md` - Current state

## Usage

```python
from r6500_1_validated import R6500_1Model

model = R6500_1Model()
result = model.analyze('typical')
print(f"CPI: {result.cpi} cycles, IPS: {result.ips:,.0f}")
```

## Notes

The R6500/1 was Rockwell's single-chip MCU based on the MOS 6502 core.
It integrated 2KB ROM, 64 bytes RAM, I/O ports, and a timer on a single
chip. Instruction timing is identical to the standard 6502, making it
a well-understood and predictable processor for embedded applications.
