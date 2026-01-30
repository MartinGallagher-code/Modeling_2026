# Zilog Z80-SIO Architecture

## Overview
The Zilog Z80-SIO (1977) is a dual-channel serial I/O controller designed for Z80-based systems, supporting both asynchronous and synchronous serial communication.

## Key Features
- 8-bit host bus interface
- 4 MHz clock frequency
- ~8,000 NMOS transistors
- Two independent serial channels
- Asynchronous mode (5-8 bit characters)
- Synchronous mode (bisync, HDLC)
- Z80 daisy-chain interrupt support
- Programmable baud rate

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Register I/O | 2 | Read/write internal registers |
| Char Process | 4 | Character transmit/receive |
| Sync | 5 | Sync pattern detection |
| Control | 3 | Mode and command processing |
| Interrupt | 4 | Interrupt generation/acknowledge |

## Application
Serial communications in Z80 systems:
- CP/M computer serial ports
- Terminal communications
- Modem interfaces
- Industrial serial links

## Related Processors
- Zilog Z8530 SCC (successor, more capable)
- Zilog Z80-DART (async-only variant)
- Intel 8251 USART (competitor)
