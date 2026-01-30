# Zilog Z8016 DMA Architecture Document

## Overview

| Property | Value |
|----------|-------|
| **Full Name** | Zilog Z8016 DMA Transfer Controller |
| **Manufacturer** | Zilog |
| **Year** | 1981 |
| **Process** | NMOS |
| **Transistors** | ~10,000 |
| **Clock Speed** | 4 MHz |
| **Data Width** | 16-bit |
| **Address Width** | 16-bit |
| **Package** | 40-pin DIP |

## Architecture Description

The Zilog Z8016 was a DMA transfer controller designed for the Z8000 processor family. It provided programmable DMA operations with multiple transfer modes and a hardware search-and-match capability.

### Execution Model

- **Type**: Sequential DMA controller
- **Pipeline**: None
- **Channels**: Programmable DMA channels
- **Addressing**: 16-bit (64 KB address space)

### Instruction Categories

| Category | Base Cycles | Description |
|----------|-------------|-------------|
| transfer | 2 | Single DMA transfer cycle |
| setup | 6 | DMA channel setup and configuration |
| chain | 8 | Chained/scatter-gather transfer |
| control | 4 | Control and status operations |
| search | 5 | Search and match operations |

### Transfer Modes

- **Block Mode**: CPU halted during entire transfer
- **Burst Mode**: CPU halted for burst of transfers, then released
- **Continuous Mode**: Interleaved with CPU bus access

### Key Features

- Multiple DMA transfer modes (block, burst, continuous)
- Hardware search-and-match capability
- Chained transfers for scatter-gather I/O
- Programmable source/destination addressing
- Auto-increment/decrement address modes
- Designed for Z8000 family bus architecture

## References

- Zilog Z8016 DMA Transfer Controller Data Sheet (1981)
- Z8000 CPU Technical Manual
- Wikipedia: Zilog Z8000
