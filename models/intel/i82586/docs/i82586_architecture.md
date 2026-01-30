# Intel 82586 Architecture

## Overview
The Intel 82586 (1983) is a 16-bit Ethernet LAN coprocessor implementing the full IEEE 802.3 CSMA/CD protocol with command block architecture and DMA.

## Key Features
- 16-bit data bus, 24-bit address bus
- 8 MHz clock frequency
- ~30,000 NMOS transistors
- Full IEEE 802.3 Ethernet MAC
- Command block list processing
- DMA with scatter/gather buffer chains
- CSMA/CD collision detection and backoff

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Frame Process | 4 | Ethernet frame send/receive |
| DMA | 6 | DMA buffer transfer operations |
| Command | 8 | Command block execution |
| Status | 3 | Status register reporting |
| Buffer | 5 | Buffer descriptor chain management |

## Application
10 Mbit/s Ethernet networking:
- PC network interface cards
- Workstation LAN controllers
- Bridge/router front-ends

## Related Processors
- Intel 82596 (successor, higher performance)
- Intel 82557 (PCI Ethernet controller)
