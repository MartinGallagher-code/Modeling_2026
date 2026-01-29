# MIPS R2000 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 3.25%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: RISC (Stanford MIPS)
- Clock: 8 MHz
- Target CPI: 2.0
- Predicted CPI: 2.065
- Pipeline: 5-stage (IF, ID, EX, MEM, WB)
- Key instruction categories: alu, load, store, branch, jump, multiply, shift, divide

## Timing Summary (from validation JSON)
| Category | Model Cycles | Expected Cycles | Notes |
|----------|-------------|-----------------|-------|
| ALU | 1.5 | 1 | Single cycle in pipeline |
| Load | 2.5 | 1 + delay | Load delay slot required |
| Store | 1.5 | 1 | Write buffer |
| Branch | 2.5 | 1 + delay | Branch delay slot |
| Jump | 2.5 | 1 + delay | Jump delay slot |
| Multiply | 4.0 | 12 | Multi-cycle (weighted avg) |
| Divide | 5.0 | 35 | Multi-cycle (weighted avg) |

## Cross-Validation
Related processors in this family:
- **sparc**: Sun's Berkeley RISC implementation (1987)
- **sun_spark**: Sun's tuned SPARC implementation

Key architectural differences from SPARC:
- R2000: 5-stage pipeline vs SPARC: 4-stage
- R2000: Fixed 32 registers vs SPARC: Register windows (136 total)
- R2000: HI/LO registers for multiply vs SPARC: Y register

## Known Issues
- None currently - model validates within 5% error

## Suggested Next Steps
- Consider adding more detailed pipeline hazard modeling if higher accuracy needed
- Could add memory hierarchy effects for cache miss scenarios
- Model currently assumes optimal delay slot filling

## Key Architectural Notes
- One of the first commercial MIPS RISC processors (1985)
- Classic 5-stage pipeline: Instruction Fetch, Decode, Execute, Memory, Writeback
- Load delay slots: instruction after load cannot use loaded value
- Branch delay slots: instruction after branch always executes
- 32 general-purpose registers (r0 hardwired to zero)
- Multiply/divide results stored in HI/LO special registers
