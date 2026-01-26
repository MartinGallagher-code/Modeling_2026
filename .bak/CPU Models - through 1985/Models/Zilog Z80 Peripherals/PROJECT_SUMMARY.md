# Z80 Peripheral Chips - Project Summary

## Reference Document (Not a CPU Model)

The Z80 wasn't just a CPU - Zilog created a complete family of compatible peripheral chips.

## The Family
- **Z80-PIO**: Parallel I/O (2×8-bit ports)
- **Z80-SIO**: Serial I/O (2 channels, HDLC)
- **Z80-CTC**: Counter/Timer (4 channels)
- **Z80-DMA**: DMA Controller (1.25 MB/s)

## Key Innovation
All chips designed together:
- Same bus timing
- Same interrupt scheme (daisy-chain)
- Same voltage (+5V)
- Direct connection, no glue logic

This family approach reduced system complexity significantly compared to Intel 8080 systems.

---
**Version:** 1.0 | **Date:** January 24, 2026
