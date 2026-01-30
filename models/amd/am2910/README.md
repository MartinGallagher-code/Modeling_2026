# AMD Am2910

## Quick Reference
| Parameter | Value |
|-----------|-------|
| Year | 1977 |
| Type | Microprogram Sequencer |
| Clock | 10 MHz |
| Transistors | ~1,500 |
| Process | Bipolar |
| Output | 12-bit address |
| Instructions | 16 (all single-cycle) |

## Description
The Am2910 is a microprogram sequencer, NOT a general-purpose CPU. It is the
essential companion to the Am2901 bit-slice ALU, generating the next
microinstruction address on every clock cycle. It provides 16 instructions
for controlling microprogram flow: jumps, conditional branches, subroutine
calls/returns, loops, and counter operations.

All 16 instructions execute in exactly 1 clock cycle. The Am2910 includes a
33-word x 12-bit microprogram address stack for subroutine nesting and a
12-bit loop counter.

## Validation Status
- **Status**: PASSED
- **CPI Error**: 0.0%
- **Model CPI**: 1.000 (target: 1.0)
- **Last Validated**: 2026-01-29

## Notes
This is a deterministic single-cycle device. CPI is always exactly 1.0
regardless of instruction mix, since all 16 instructions take 1 cycle.
