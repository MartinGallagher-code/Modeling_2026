# ARM6 Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 4.1%
- **Last Updated**: 2026-01-28

## Current Model Summary
- Architecture: 32-bit RISC, 3-stage pipeline, full 32-bit addressing
- Clock: 20 MHz (up to 40 MHz)
- Target CPI: 1.43
- Predicted CPI: 1.37
- Key instruction categories: alu (1 cycle), load (1.9 cycles), store (1.5 cycles), branch (2.0 cycles)

## Cross-Validation Status
- Family position: Fourth generation - foundation of modern ARM
- Predecessor: ARM3
- Successor: ARM7 (not in this model set)
- Per-instruction timing tests: 17 tests documented
- Family evolution documented: ARM1 -> ARM2 -> ARM3 -> ARM6

## Known Issues
- CPI error at 4.1% is highest among the four ARM models but still within 5% threshold
- Model validated - no changes required

## Suggested Next Steps
- Consider adding ARM610 cache variant modeling
- Could add Thumb instruction set timing if ARM7 compatibility needed
- Low priority since validation passed

## Key Architectural Notes
- Foundation of modern ARM architecture from ARM Ltd (1991)
- First ARM with full 32-bit address space (4GB vs 64MB)
- Separate CPSR/SPSR status registers (vs packed in PC)
- MSR/MRS instructions for status register access
- First ARM designed primarily for licensing
- Optimized for low power mobile use
- Powered Apple Newton - first major consumer ARM device
- 35,000 transistors on 1um CMOS process

## ARM Family Context
| Processor | Year | CPI | MIPS | Key Feature |
|-----------|------|-----|------|-------------|
| ARM1 | 1985 | 1.8 | 3.0 | First ARM, no cache |
| ARM2 | 1986 | 1.43 | 4.5 | Hardware multiplier |
| ARM3 | 1989 | 1.33 | 18.0 | First with 4KB cache |
| ARM6 | 1991 | 1.43 | 14.0 | 32-bit address space |

## Architectural Significance
- ARM6 CPI (1.43) similar to ARM2 - same core architecture optimized
- Focus on architectural improvements (32-bit addressing) not raw speed
- ARM6 broke backward compatibility to enable 32-bit addressing
- Licensing model started with ARM6 led to ARM's market dominance
- Apple Newton partnership proved ARM viable for mobile computing

## Key Differences from ARM3
- Full 32-bit address space (4GB vs 64MB)
- Separate CPSR/SPSR for status (vs packed in PC)
- MSR/MRS instructions for status register access
- Designed for licensing (ARM3 was Acorn-specific)
- Optimized for low power mobile use
- Variants: ARM60 (no cache), ARM610 (4KB), ARM6100 (8KB)
