# NEC uPD8080AF Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.0%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: 8-bit sequential execution (1975)
- Clock: 2.0 MHz, NMOS technology
- Categories: alu (4.0c), data_transfer (5.0c), memory (7.0c), control (5.0c), stack (10.0c)
- Predicted typical CPI: 5.500 (target: 5.5)

## Known Issues
- Model uses simplified category-based timing
- Fixed workload profiles may not match all real-world use cases

## Suggested Next Steps
- Cross-validate against Intel 8080 model for consistency
- Verify timing against NEC datasheet if available
- Consider relationship to NEC V20/V30 lineage

## Key Architectural Notes
- One of the earliest Intel 8080 clones (1975, same year as 8080A)
- NEC manufactured under second-source agreement with Intel
- Predates NEC's own V-series (V20, V30) which added extensions
- Widely used in Japanese personal computers and industrial systems
- "AF" suffix indicates improved electrical specifications
