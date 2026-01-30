# Ferranti ULA Model Handoff

## Current Status
- **Validation**: PASSED
- **CPI Error**: 0.4%
- **Last Updated**: 2026-01-29

## Current Model Summary
- Architecture: Uncommitted Logic Array / gate array (1981)
- Clock: 3.5 MHz (7 MHz pixel clock / 2), ~5000 transistors
- 8 instruction categories: video_fetch(4.5c), attribute_fetch(4.5c), io_decode(3.5c), bus_arbitration(5.0c), keyboard_scan(6.5c), border_gen(2.0c), memory_control(4.0c), interrupt_gen(4.0c)
- Bus contention factor: 1.10
- Queueing factor: 1.0 + rho * 0.08
- Predicted typical CPI: 5.018 (target: 5.0)

## Workload Results
| Workload | CPI | IPC | IPS |
|----------|-----|-----|-----|
| typical | 5.018 | 0.1993 | 697,489 |
| compute | 4.985 | 0.2006 | 702,106 |
| memory | 5.091 | 0.1964 | 687,488 |
| control | 5.123 | 0.1952 | 683,193 |

## Known Issues
- None significant - model is well-calibrated across all workloads

## Suggested Next Steps
- No changes needed - model passes with excellent 0.4% error
- One of the best-calibrated models in the collection

## Key Architectural Notes
- NOT a CPU - ZX Spectrum ULA for video/IO/bus management
- Manages Z80 bus contention during screen refresh
- Generates video signal, handles keyboard scanning
- Semi-custom Ferranti gate array

## System Identification (2026-01-29)
- **Status**: Converged
- **CPI Error**: 0.82%
- **Free Parameters**: 4
- **Corrections**: See `identification/sysid_result.json`
