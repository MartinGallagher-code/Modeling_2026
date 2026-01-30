# Zilog Z8530 SCC Architecture

## Overview
The Zilog Z8530 SCC (1981) is a dual-channel Serial Communications Controller supporting HDLC, SDLC, and asynchronous serial protocols with hardware CRC and DMA.

## Key Features
- 8-bit host bus interface
- 6 MHz clock frequency
- ~15,000 NMOS transistors
- Two independent serial channels
- HDLC/SDLC synchronous protocol support
- Asynchronous mode support
- Hardware CRC-16 and CRC-CCITT
- DMA request/acknowledge interface

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Register I/O | 2 | Read/write internal registers |
| Frame Process | 6 | HDLC frame assembly/disassembly |
| CRC | 4 | CRC generation and checking |
| Control | 3 | Command and status operations |
| DMA | 5 | DMA transfer coordination |

## Application
Serial communications in:
- Apple Macintosh (AppleTalk, serial ports)
- Sun workstations (serial console, networking)
- Networking equipment
- Industrial serial links

## Related Processors
- Zilog Z80-SIO (predecessor, simpler)
- Zilog Z85C30 (CMOS version)
- Intel 82530 (second-source)
