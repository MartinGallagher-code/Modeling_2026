# Western Digital WD2010 Architecture

## Overview
The Western Digital WD2010 (1983) is an 8-bit hard disk controller implementing the ST-506/ST-412 Winchester disk interface with hardware ECC and format support.

## Key Features
- 8-bit host bus interface
- 5 MHz clock frequency
- ~15,000 NMOS transistors
- ST-506/ST-412 disk interface
- Hardware ECC error checking
- Track format capability
- Multi-sector read/write
- Head seek management

## Instruction Categories
| Category | Cycles | Description |
|----------|--------|-------------|
| Command | 4 | Command decode and dispatch |
| Data Transfer | 3 | Sector data read/write |
| Seek | 8 | Head positioning |
| Format | 10 | Track format operations |
| Error Check | 5 | ECC generation/checking |

## Application
Hard disk control in personal computers:
- IBM PC/XT hard disk adapter
- Compatible PC hard disk controllers
- Industrial storage systems

## Related Processors
- WD1010 (predecessor)
- WD1003 (controller board using WD2010)
- WD33C93 (SCSI controller successor)
