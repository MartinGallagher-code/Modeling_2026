# Tesla MHB8080A Model Changelog

## 2026-01-29: Initial Model Creation

### Changes Made
- Created Tesla MHB8080A model as Intel 8080A clone
- Used Intel 8080 timing as reference (Tesla maintained full compatibility)
- Calibrated instruction categories from 8080 datasheet:
  - alu: 5.0 cycles (ADD/SUB r @4, ADD M @7, weighted)
  - data_transfer: 5.5 cycles (MOV r,r @5, MVI @7, LXI @10, weighted)
  - memory: 10.0 cycles (LDA @13, STA @13, weighted)
  - io: 10.0 cycles (IN/OUT @10)
  - control: 9.0 cycles (JMP @10, CALL @17, RET @10, weighted)
  - stack: 10.5 cycles (PUSH @11, POP @10, weighted)

### Results
- Target CPI: 7.5 (same as Intel 8080)
- Status: VALIDATED

### Technical Notes
- Czechoslovak Intel 8080A clone by Tesla Piestany (1982)
- Used in PMI-80 and PMD 85 computers
- NMOS technology, 2 MHz clock

### References
- Intel 8080A Datasheet (timing reference)
- Tesla Piestany documentation
