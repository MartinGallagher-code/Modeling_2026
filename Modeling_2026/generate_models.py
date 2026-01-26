#!/usr/bin/env python3
"""
Generate all 63 processor models for Modeling_2026.

This script creates the Python model files, JSON configs, and READMEs
for all processors in the project.
"""

import os
import json
from pathlib import Path

# Complete processor database with timing data
PROCESSORS = {
    'intel': {
        'i4004': {
            'name': 'Intel 4004', 'year': 1971, 'clock_mhz': 0.740, 'bus_width': 4,
            'transistors': 2300, 'ips_min': 46000, 'ips_max': 93000,
            'cpi_min': 8, 'cpi_max': 16, 'bottleneck': ['fetch', 'sequential fetch'],
            'categories': {
                'register_ops': {'cycles': 8, 'weight': 0.25, 'desc': 'INC, ADD, SUB, LD, XCH'},
                'accumulator_imm': {'cycles': 16, 'weight': 0.15, 'desc': 'LDM, FIM'},
                'memory_ops': {'cycles': 8, 'weight': 0.20, 'desc': 'RDM, WRM, RDR, WRR'},
                'bcd_arithmetic': {'cycles': 8, 'weight': 0.10, 'desc': 'DAA, CLC, STC'},
                'jump_unconditional': {'cycles': 16, 'weight': 0.08, 'desc': 'JUN'},
                'jump_conditional': {'cycles': 16, 'weight': 0.07, 'desc': 'JCN'},
                'subroutine': {'cycles': 16, 'weight': 0.05, 'desc': 'JMS, BBL'},
                'io_ops': {'cycles': 8, 'weight': 0.08, 'desc': 'I/O operations'},
                'nop_misc': {'cycles': 8, 'weight': 0.02, 'desc': 'NOP'}
            },
            'source': 'MCS-4 Users Manual'
        },
        'i4040': {
            'name': 'Intel 4040', 'year': 1974, 'clock_mhz': 0.740, 'bus_width': 4,
            'transistors': 3000, 'ips_min': 50000, 'ips_max': 100000,
            'cpi_min': 7, 'cpi_max': 15, 'bottleneck': ['fetch', 'sequential fetch'],
            'categories': {
                'register_ops': {'cycles': 8, 'weight': 0.25, 'desc': 'INC, ADD, SUB, LD, XCH'},
                'accumulator_imm': {'cycles': 16, 'weight': 0.15, 'desc': 'LDM, FIM'},
                'memory_ops': {'cycles': 8, 'weight': 0.18, 'desc': 'RDM, WRM'},
                'bcd_arithmetic': {'cycles': 8, 'weight': 0.10, 'desc': 'DAA operations'},
                'jump_unconditional': {'cycles': 16, 'weight': 0.08, 'desc': 'JUN'},
                'jump_conditional': {'cycles': 16, 'weight': 0.07, 'desc': 'JCN'},
                'subroutine': {'cycles': 16, 'weight': 0.05, 'desc': 'JMS, BBL'},
                'io_ops': {'cycles': 8, 'weight': 0.08, 'desc': 'I/O operations'},
                'interrupt': {'cycles': 16, 'weight': 0.02, 'desc': 'Interrupt handling'},
                'nop_misc': {'cycles': 8, 'weight': 0.02, 'desc': 'NOP, HLT'}
            },
            'source': 'MCS-40 Users Manual'
        },
        'i8008': {
            'name': 'Intel 8008', 'year': 1972, 'clock_mhz': 0.500, 'bus_width': 8,
            'transistors': 3500, 'ips_min': 23000, 'ips_max': 80000,
            'cpi_min': 10, 'cpi_max': 22, 'bottleneck': ['fetch', 'sequential'],
            'categories': {
                'mov_reg_reg': {'cycles': 10, 'weight': 0.20, 'desc': 'MOV r1,r2 (5 T-states)'},
                'mov_reg_mem': {'cycles': 16, 'weight': 0.15, 'desc': 'MOV r,M / MOV M,r'},
                'alu_register': {'cycles': 10, 'weight': 0.20, 'desc': 'ADD/SUB/AND/OR r'},
                'alu_memory': {'cycles': 16, 'weight': 0.10, 'desc': 'ADD M, etc.'},
                'immediate': {'cycles': 16, 'weight': 0.10, 'desc': 'MVI, ADI, etc.'},
                'jump_unconditional': {'cycles': 22, 'weight': 0.08, 'desc': 'JMP'},
                'jump_conditional': {'cycles': 18, 'weight': 0.07, 'desc': 'Jcc'},
                'call_return': {'cycles': 22, 'weight': 0.05, 'desc': 'CALL, RET'},
                'io_ops': {'cycles': 16, 'weight': 0.03, 'desc': 'IN, OUT'},
                'misc': {'cycles': 10, 'weight': 0.02, 'desc': 'HLT, NOP'}
            },
            'source': 'Intel 8008 Users Manual'
        },
        'i8080': {
            'name': 'Intel 8080', 'year': 1974, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 4500, 'ips_min': 290000, 'ips_max': 500000,
            'cpi_min': 4, 'cpi_max': 18, 'bottleneck': ['decode', 'fetch'],
            'categories': {
                'mov_reg_reg': {'cycles': 5, 'weight': 0.20, 'desc': 'MOV r1,r2'},
                'mov_reg_mem': {'cycles': 7, 'weight': 0.15, 'desc': 'MOV r,M / MOV M,r'},
                'alu_register': {'cycles': 4, 'weight': 0.25, 'desc': 'ADD/SUB/AND/OR r'},
                'alu_memory': {'cycles': 7, 'weight': 0.10, 'desc': 'ADD M, etc.'},
                'immediate': {'cycles': 7, 'weight': 0.10, 'desc': 'MVI, ADI, etc.'},
                'branch_taken': {'cycles': 10, 'weight': 0.08, 'desc': 'JZ, JNZ taken'},
                'branch_not_taken': {'cycles': 10, 'weight': 0.04, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 17, 'weight': 0.05, 'desc': 'CALL=17, RET=10'},
                'stack_ops': {'cycles': 11, 'weight': 0.03, 'desc': 'PUSH/POP'}
            },
            'source': 'Intel 8080 Microcomputer Systems User Manual'
        },
        'i8085': {
            'name': 'Intel 8085', 'year': 1976, 'clock_mhz': 3.0, 'bus_width': 8,
            'transistors': 6500, 'ips_min': 370000, 'ips_max': 770000,
            'cpi_min': 4, 'cpi_max': 16, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_reg_reg': {'cycles': 4, 'weight': 0.22, 'desc': 'MOV r1,r2'},
                'mov_reg_mem': {'cycles': 7, 'weight': 0.15, 'desc': 'MOV r,M'},
                'alu_register': {'cycles': 4, 'weight': 0.25, 'desc': 'ADD/SUB/AND/OR r'},
                'alu_memory': {'cycles': 7, 'weight': 0.08, 'desc': 'ADD M, etc.'},
                'immediate': {'cycles': 7, 'weight': 0.10, 'desc': 'MVI, ADI'},
                'branch_taken': {'cycles': 10, 'weight': 0.08, 'desc': 'Conditional jumps'},
                'branch_not_taken': {'cycles': 7, 'weight': 0.04, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 16, 'weight': 0.05, 'desc': 'CALL/RET'},
                'stack_ops': {'cycles': 12, 'weight': 0.03, 'desc': 'PUSH/POP'}
            },
            'source': 'Intel 8085A Users Manual'
        },
        'i8086': {
            'name': 'Intel 8086', 'year': 1978, 'clock_mhz': 5.0, 'bus_width': 16,
            'transistors': 29000, 'ips_min': 330000, 'ips_max': 750000,
            'cpi_min': 7, 'cpi_max': 15, 'bottleneck': ['ea_calc', 'prefetch'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.18, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 12, 'weight': 0.15, 'desc': 'MOV r,m with EA calc'},
                'alu_register': {'cycles': 3, 'weight': 0.20, 'desc': 'ADD/SUB/AND/OR r,r'},
                'alu_memory': {'cycles': 17, 'weight': 0.10, 'desc': 'ALU with memory'},
                'immediate': {'cycles': 4, 'weight': 0.12, 'desc': 'MOV r,imm'},
                'branch_taken': {'cycles': 16, 'weight': 0.08, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 23, 'weight': 0.05, 'desc': 'CALL near'},
                'string_ops': {'cycles': 18, 'weight': 0.04, 'desc': 'MOVSB, REP'},
                'multiply': {'cycles': 133, 'weight': 0.03, 'desc': 'MUL/IMUL'}
            },
            'source': 'Intel 8086 Family Users Manual'
        },
        'i8088': {
            'name': 'Intel 8088', 'year': 1979, 'clock_mhz': 5.0, 'bus_width': 8,
            'transistors': 29000, 'ips_min': 250000, 'ips_max': 500000,
            'cpi_min': 10, 'cpi_max': 20, 'bottleneck': ['prefetch', 'bus_width'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.18, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 16, 'weight': 0.15, 'desc': 'MOV r,m (slower bus)'},
                'alu_register': {'cycles': 3, 'weight': 0.20, 'desc': 'ADD/SUB/AND/OR r,r'},
                'alu_memory': {'cycles': 21, 'weight': 0.10, 'desc': 'ALU with memory'},
                'immediate': {'cycles': 4, 'weight': 0.12, 'desc': 'MOV r,imm'},
                'branch_taken': {'cycles': 16, 'weight': 0.08, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 28, 'weight': 0.05, 'desc': 'CALL near'},
                'string_ops': {'cycles': 22, 'weight': 0.04, 'desc': 'String operations'},
                'multiply': {'cycles': 143, 'weight': 0.03, 'desc': 'MUL/IMUL'}
            },
            'source': 'Intel 8088 Users Manual'
        },
        'i80186': {
            'name': 'Intel 80186', 'year': 1982, 'clock_mhz': 8.0, 'bus_width': 16,
            'transistors': 55000, 'ips_min': 900000, 'ips_max': 1500000,
            'cpi_min': 5, 'cpi_max': 10, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.20, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 9, 'weight': 0.15, 'desc': 'MOV r,m'},
                'alu_register': {'cycles': 3, 'weight': 0.22, 'desc': 'ALU r,r'},
                'alu_memory': {'cycles': 12, 'weight': 0.10, 'desc': 'ALU r,m'},
                'immediate': {'cycles': 3, 'weight': 0.12, 'desc': 'Immediate ops'},
                'branch_taken': {'cycles': 13, 'weight': 0.08, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 15, 'weight': 0.05, 'desc': 'CALL/RET'},
                'multiply': {'cycles': 36, 'weight': 0.03, 'desc': 'MUL/IMUL (faster)'}
            },
            'source': 'Intel 80186/80188 Users Manual'
        },
        'i80188': {
            'name': 'Intel 80188', 'year': 1982, 'clock_mhz': 8.0, 'bus_width': 8,
            'transistors': 55000, 'ips_min': 700000, 'ips_max': 1200000,
            'cpi_min': 7, 'cpi_max': 12, 'bottleneck': ['prefetch', 'bus_width'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.20, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 12, 'weight': 0.15, 'desc': 'MOV r,m'},
                'alu_register': {'cycles': 3, 'weight': 0.22, 'desc': 'ALU r,r'},
                'alu_memory': {'cycles': 16, 'weight': 0.10, 'desc': 'ALU r,m'},
                'immediate': {'cycles': 3, 'weight': 0.12, 'desc': 'Immediate ops'},
                'branch_taken': {'cycles': 13, 'weight': 0.08, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 18, 'weight': 0.05, 'desc': 'CALL/RET'},
                'multiply': {'cycles': 40, 'weight': 0.03, 'desc': 'MUL/IMUL'}
            },
            'source': 'Intel 80186/80188 Users Manual'
        },
        'i80286': {
            'name': 'Intel 80286', 'year': 1982, 'clock_mhz': 8.0, 'bus_width': 16,
            'transistors': 134000, 'ips_min': 900000, 'ips_max': 2700000,
            'cpi_min': 3, 'cpi_max': 9, 'bottleneck': ['memory', 'decode'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.22, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 5, 'weight': 0.15, 'desc': 'MOV r,m'},
                'alu_register': {'cycles': 2, 'weight': 0.25, 'desc': 'ALU r,r'},
                'alu_memory': {'cycles': 7, 'weight': 0.10, 'desc': 'ALU r,m'},
                'immediate': {'cycles': 3, 'weight': 0.10, 'desc': 'Immediate ops'},
                'branch_taken': {'cycles': 11, 'weight': 0.07, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 3, 'weight': 0.04, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 13, 'weight': 0.05, 'desc': 'CALL/RET'},
                'multiply': {'cycles': 21, 'weight': 0.02, 'desc': 'MUL/IMUL'}
            },
            'source': 'Intel 80286 Programmers Reference Manual'
        },
        'i80386': {
            'name': 'Intel 80386', 'year': 1985, 'clock_mhz': 16.0, 'bus_width': 32,
            'transistors': 275000, 'ips_min': 3000000, 'ips_max': 11000000,
            'cpi_min': 2, 'cpi_max': 6, 'bottleneck': ['cache', 'memory'],
            'categories': {
                'mov_reg_reg': {'cycles': 2, 'weight': 0.22, 'desc': 'MOV r,r'},
                'mov_reg_mem': {'cycles': 4, 'weight': 0.18, 'desc': 'MOV r,m'},
                'alu_register': {'cycles': 2, 'weight': 0.25, 'desc': 'ALU r,r'},
                'alu_memory': {'cycles': 6, 'weight': 0.10, 'desc': 'ALU r,m'},
                'immediate': {'cycles': 2, 'weight': 0.10, 'desc': 'Immediate ops'},
                'branch_taken': {'cycles': 10, 'weight': 0.06, 'desc': 'Jcc taken'},
                'branch_not_taken': {'cycles': 3, 'weight': 0.04, 'desc': 'Jcc not taken'},
                'call_return': {'cycles': 10, 'weight': 0.03, 'desc': 'CALL/RET'},
                'multiply': {'cycles': 14, 'weight': 0.02, 'desc': 'MUL/IMUL'}
            },
            'source': 'Intel 80386 Programmers Reference Manual'
        },
        'i8048': {
            'name': 'Intel 8048', 'year': 1976, 'clock_mhz': 6.0, 'bus_width': 8,
            'transistors': 6000, 'ips_min': 400000, 'ips_max': 800000,
            'cpi_min': 8, 'cpi_max': 15, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'mov_a_r': {'cycles': 15, 'weight': 0.25, 'desc': 'MOV A,Rn'},
                'mov_a_mem': {'cycles': 15, 'weight': 0.15, 'desc': 'MOV A,@Ri'},
                'alu_ops': {'cycles': 15, 'weight': 0.25, 'desc': 'ADD, ADDC, ANL, ORL'},
                'immediate': {'cycles': 30, 'weight': 0.10, 'desc': 'MOV A,#data'},
                'jump': {'cycles': 30, 'weight': 0.10, 'desc': 'JMP, CALL'},
                'conditional': {'cycles': 30, 'weight': 0.08, 'desc': 'JZ, JNZ'},
                'io_ops': {'cycles': 30, 'weight': 0.05, 'desc': 'IN, OUT'},
                'misc': {'cycles': 15, 'weight': 0.02, 'desc': 'NOP, other'}
            },
            'source': 'Intel MCS-48 Users Manual'
        },
        'i8051': {
            'name': 'Intel 8051', 'year': 1980, 'clock_mhz': 12.0, 'bus_width': 8,
            'transistors': 128000, 'ips_min': 500000, 'ips_max': 1000000,
            'cpi_min': 12, 'cpi_max': 24, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_direct': {'cycles': 12, 'weight': 0.20, 'desc': 'MOV direct'},
                'mov_indirect': {'cycles': 12, 'weight': 0.15, 'desc': 'MOV @Ri'},
                'alu_ops': {'cycles': 12, 'weight': 0.25, 'desc': 'ADD, ADDC, SUBB'},
                'immediate': {'cycles': 12, 'weight': 0.12, 'desc': 'MOV #data'},
                'branch': {'cycles': 24, 'weight': 0.10, 'desc': 'SJMP, AJMP'},
                'call_return': {'cycles': 24, 'weight': 0.05, 'desc': 'ACALL, RET'},
                'bit_ops': {'cycles': 12, 'weight': 0.08, 'desc': 'SETB, CLR, CPL'},
                'multiply': {'cycles': 48, 'weight': 0.03, 'desc': 'MUL, DIV'},
                'misc': {'cycles': 12, 'weight': 0.02, 'desc': 'NOP'}
            },
            'source': 'Intel MCS-51 Users Manual'
        },
        'i8748': {
            'name': 'Intel 8748', 'year': 1977, 'clock_mhz': 6.0, 'bus_width': 8,
            'transistors': 8000, 'ips_min': 400000, 'ips_max': 750000,
            'cpi_min': 8, 'cpi_max': 15, 'bottleneck': ['fetch'],
            'categories': {
                'mov_a_r': {'cycles': 15, 'weight': 0.25, 'desc': 'MOV A,Rn'},
                'mov_a_mem': {'cycles': 15, 'weight': 0.15, 'desc': 'MOV A,@Ri'},
                'alu_ops': {'cycles': 15, 'weight': 0.25, 'desc': 'ALU operations'},
                'immediate': {'cycles': 30, 'weight': 0.10, 'desc': 'MOV A,#data'},
                'jump': {'cycles': 30, 'weight': 0.10, 'desc': 'JMP, CALL'},
                'conditional': {'cycles': 30, 'weight': 0.08, 'desc': 'Conditional jumps'},
                'io_ops': {'cycles': 30, 'weight': 0.05, 'desc': 'I/O operations'},
                'misc': {'cycles': 15, 'weight': 0.02, 'desc': 'NOP'}
            },
            'source': 'Intel MCS-48 Users Manual'
        },
        'i8751': {
            'name': 'Intel 8751', 'year': 1980, 'clock_mhz': 12.0, 'bus_width': 8,
            'transistors': 128000, 'ips_min': 500000, 'ips_max': 1000000,
            'cpi_min': 12, 'cpi_max': 24, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_direct': {'cycles': 12, 'weight': 0.20, 'desc': 'MOV direct'},
                'mov_indirect': {'cycles': 12, 'weight': 0.15, 'desc': 'MOV @Ri'},
                'alu_ops': {'cycles': 12, 'weight': 0.25, 'desc': 'ALU operations'},
                'immediate': {'cycles': 12, 'weight': 0.12, 'desc': 'MOV #data'},
                'branch': {'cycles': 24, 'weight': 0.10, 'desc': 'Branch ops'},
                'call_return': {'cycles': 24, 'weight': 0.05, 'desc': 'CALL, RET'},
                'bit_ops': {'cycles': 12, 'weight': 0.08, 'desc': 'Bit operations'},
                'multiply': {'cycles': 48, 'weight': 0.03, 'desc': 'MUL, DIV'},
                'misc': {'cycles': 12, 'weight': 0.02, 'desc': 'NOP'}
            },
            'source': 'Intel MCS-51 Users Manual'
        },
        'iapx432': {
            'name': 'Intel iAPX 432', 'year': 1981, 'clock_mhz': 8.0, 'bus_width': 32,
            'transistors': 220000, 'ips_min': 100000, 'ips_max': 300000,
            'cpi_min': 25, 'cpi_max': 80, 'bottleneck': ['decode', 'microcode'],
            'categories': {
                'simple_ops': {'cycles': 20, 'weight': 0.25, 'desc': 'Simple operations'},
                'memory_ops': {'cycles': 30, 'weight': 0.20, 'desc': 'Memory access'},
                'object_ops': {'cycles': 50, 'weight': 0.15, 'desc': 'Object manipulation'},
                'branch': {'cycles': 35, 'weight': 0.12, 'desc': 'Branch operations'},
                'call_return': {'cycles': 80, 'weight': 0.10, 'desc': 'Procedure call'},
                'capability': {'cycles': 100, 'weight': 0.10, 'desc': 'Capability operations'},
                'context_switch': {'cycles': 200, 'weight': 0.05, 'desc': 'Context switch'},
                'misc': {'cycles': 25, 'weight': 0.03, 'desc': 'Other'}
            },
            'source': 'Intel iAPX 432 General Data Processor'
        },
        'i80287': {
            'name': 'Intel 80287', 'year': 1982, 'clock_mhz': 8.0, 'bus_width': 16,
            'transistors': 45000, 'ips_min': 50000, 'ips_max': 150000,
            'cpi_min': 50, 'cpi_max': 200, 'bottleneck': ['execute', 'fpu'],
            'categories': {
                'fld': {'cycles': 40, 'weight': 0.20, 'desc': 'FLD (load)'},
                'fst': {'cycles': 50, 'weight': 0.15, 'desc': 'FST (store)'},
                'fadd': {'cycles': 90, 'weight': 0.20, 'desc': 'FADD'},
                'fsub': {'cycles': 90, 'weight': 0.10, 'desc': 'FSUB'},
                'fmul': {'cycles': 140, 'weight': 0.15, 'desc': 'FMUL'},
                'fdiv': {'cycles': 200, 'weight': 0.10, 'desc': 'FDIV'},
                'fsqrt': {'cycles': 180, 'weight': 0.05, 'desc': 'FSQRT'},
                'fcomp': {'cycles': 50, 'weight': 0.05, 'desc': 'FCOMP'}
            },
            'source': 'Intel 80287 Programmers Reference'
        },
        'i80387': {
            'name': 'Intel 80387', 'year': 1987, 'clock_mhz': 16.0, 'bus_width': 32,
            'transistors': 104000, 'ips_min': 150000, 'ips_max': 500000,
            'cpi_min': 30, 'cpi_max': 120, 'bottleneck': ['execute', 'fpu'],
            'categories': {
                'fld': {'cycles': 20, 'weight': 0.20, 'desc': 'FLD (load)'},
                'fst': {'cycles': 25, 'weight': 0.15, 'desc': 'FST (store)'},
                'fadd': {'cycles': 30, 'weight': 0.20, 'desc': 'FADD'},
                'fsub': {'cycles': 30, 'weight': 0.10, 'desc': 'FSUB'},
                'fmul': {'cycles': 50, 'weight': 0.15, 'desc': 'FMUL'},
                'fdiv': {'cycles': 90, 'weight': 0.10, 'desc': 'FDIV'},
                'fsqrt': {'cycles': 120, 'weight': 0.05, 'desc': 'FSQRT'},
                'fcomp': {'cycles': 25, 'weight': 0.05, 'desc': 'FCOMP'}
            },
            'source': 'Intel 80387 Programmers Reference'
        }
    },
    'motorola': {
        'm6800': {
            'name': 'Motorola 6800', 'year': 1974, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 4100, 'ips_min': 250000, 'ips_max': 500000,
            'cpi_min': 2, 'cpi_max': 10, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'inherent': {'cycles': 2, 'weight': 0.20, 'desc': 'NOP, TAB, etc.'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'LDA #imm'},
                'direct': {'cycles': 3, 'weight': 0.20, 'desc': 'LDA direct'},
                'extended': {'cycles': 4, 'weight': 0.12, 'desc': 'LDA extended'},
                'indexed': {'cycles': 5, 'weight': 0.10, 'desc': 'LDA indexed'},
                'branch_taken': {'cycles': 4, 'weight': 0.08, 'desc': 'Branch taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Branch not taken'},
                'jsr_rts': {'cycles': 9, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'stack': {'cycles': 4, 'weight': 0.02, 'desc': 'PSH, PUL'}
            },
            'source': 'Motorola M6800 Programming Reference Manual'
        },
        'm6802': {
            'name': 'Motorola 6802', 'year': 1977, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 5000, 'ips_min': 250000, 'ips_max': 500000,
            'cpi_min': 2, 'cpi_max': 10, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'inherent': {'cycles': 2, 'weight': 0.20, 'desc': 'Inherent addressing'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 3, 'weight': 0.20, 'desc': 'Direct page'},
                'extended': {'cycles': 4, 'weight': 0.12, 'desc': 'Extended'},
                'indexed': {'cycles': 5, 'weight': 0.10, 'desc': 'Indexed'},
                'branch_taken': {'cycles': 4, 'weight': 0.08, 'desc': 'Branch taken'},
                'branch_not_taken': {'cycles': 4, 'weight': 0.05, 'desc': 'Branch not taken'},
                'jsr_rts': {'cycles': 9, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'stack': {'cycles': 4, 'weight': 0.02, 'desc': 'Stack ops'}
            },
            'source': 'Motorola MC6802 Data Sheet'
        },
        'm6809': {
            'name': 'Motorola 6809', 'year': 1978, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 9000, 'ips_min': 250000, 'ips_max': 600000,
            'cpi_min': 2, 'cpi_max': 8, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'inherent': {'cycles': 2, 'weight': 0.18, 'desc': 'Inherent'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 4, 'weight': 0.18, 'desc': 'Direct'},
                'indexed': {'cycles': 5, 'weight': 0.15, 'desc': 'Indexed'},
                'extended': {'cycles': 5, 'weight': 0.10, 'desc': 'Extended'},
                'branch_short': {'cycles': 3, 'weight': 0.08, 'desc': 'Short branch'},
                'branch_long': {'cycles': 5, 'weight': 0.05, 'desc': 'Long branch'},
                'jsr_rts': {'cycles': 7, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 11, 'weight': 0.03, 'desc': 'MUL'}
            },
            'source': 'Motorola MC6809 Programming Manual'
        },
        'm68000': {
            'name': 'Motorola 68000', 'year': 1979, 'clock_mhz': 8.0, 'bus_width': 16,
            'transistors': 68000, 'ips_min': 1000000, 'ips_max': 2000000,
            'cpi_min': 4, 'cpi_max': 158, 'bottleneck': ['ea_calc', 'decode'],
            'categories': {
                'move_reg': {'cycles': 4, 'weight': 0.20, 'desc': 'MOVE Dn,Dn'},
                'move_mem': {'cycles': 12, 'weight': 0.15, 'desc': 'MOVE (An),Dn'},
                'alu_reg': {'cycles': 4, 'weight': 0.20, 'desc': 'ADD, SUB, AND reg'},
                'alu_mem': {'cycles': 12, 'weight': 0.10, 'desc': 'ALU with memory'},
                'immediate': {'cycles': 8, 'weight': 0.10, 'desc': 'MOVE #imm'},
                'branch': {'cycles': 10, 'weight': 0.10, 'desc': 'Bcc'},
                'jsr_rts': {'cycles': 18, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 70, 'weight': 0.05, 'desc': 'MULS, MULU'},
                'divide': {'cycles': 158, 'weight': 0.03, 'desc': 'DIVS, DIVU'},
                'misc': {'cycles': 4, 'weight': 0.02, 'desc': 'NOP, etc.'}
            },
            'source': 'M68000 Users Manual'
        },
        'm68008': {
            'name': 'Motorola 68008', 'year': 1982, 'clock_mhz': 8.0, 'bus_width': 8,
            'transistors': 68000, 'ips_min': 600000, 'ips_max': 1200000,
            'cpi_min': 7, 'cpi_max': 160, 'bottleneck': ['bus_width', 'memory'],
            'categories': {
                'move_reg': {'cycles': 4, 'weight': 0.20, 'desc': 'MOVE Dn,Dn'},
                'move_mem': {'cycles': 18, 'weight': 0.15, 'desc': 'MOVE (An),Dn'},
                'alu_reg': {'cycles': 4, 'weight': 0.20, 'desc': 'ALU register'},
                'alu_mem': {'cycles': 18, 'weight': 0.10, 'desc': 'ALU memory'},
                'immediate': {'cycles': 12, 'weight': 0.10, 'desc': 'Immediate'},
                'branch': {'cycles': 14, 'weight': 0.10, 'desc': 'Branch'},
                'jsr_rts': {'cycles': 24, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 74, 'weight': 0.05, 'desc': 'Multiply'},
                'divide': {'cycles': 162, 'weight': 0.03, 'desc': 'Divide'},
                'misc': {'cycles': 4, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'M68008 Users Manual'
        },
        'm68010': {
            'name': 'Motorola 68010', 'year': 1982, 'clock_mhz': 10.0, 'bus_width': 16,
            'transistors': 84000, 'ips_min': 1200000, 'ips_max': 2500000,
            'cpi_min': 4, 'cpi_max': 150, 'bottleneck': ['ea_calc', 'memory'],
            'categories': {
                'move_reg': {'cycles': 4, 'weight': 0.22, 'desc': 'MOVE Dn,Dn'},
                'move_mem': {'cycles': 10, 'weight': 0.15, 'desc': 'MOVE (An),Dn'},
                'alu_reg': {'cycles': 4, 'weight': 0.22, 'desc': 'ALU register'},
                'alu_mem': {'cycles': 10, 'weight': 0.10, 'desc': 'ALU memory'},
                'immediate': {'cycles': 6, 'weight': 0.10, 'desc': 'Immediate'},
                'branch': {'cycles': 8, 'weight': 0.08, 'desc': 'Branch (loop mode)'},
                'jsr_rts': {'cycles': 14, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 60, 'weight': 0.04, 'desc': 'Multiply'},
                'divide': {'cycles': 140, 'weight': 0.02, 'desc': 'Divide'},
                'misc': {'cycles': 4, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'MC68010 Users Manual'
        },
        'm68020': {
            'name': 'Motorola 68020', 'year': 1984, 'clock_mhz': 16.0, 'bus_width': 32,
            'transistors': 190000, 'ips_min': 3000000, 'ips_max': 6000000,
            'cpi_min': 3, 'cpi_max': 60, 'bottleneck': ['cache', 'memory'],
            'categories': {
                'move_reg': {'cycles': 2, 'weight': 0.25, 'desc': 'MOVE Dn,Dn'},
                'move_mem': {'cycles': 6, 'weight': 0.18, 'desc': 'MOVE (An),Dn'},
                'alu_reg': {'cycles': 2, 'weight': 0.25, 'desc': 'ALU register'},
                'alu_mem': {'cycles': 6, 'weight': 0.10, 'desc': 'ALU memory'},
                'immediate': {'cycles': 3, 'weight': 0.08, 'desc': 'Immediate'},
                'branch': {'cycles': 6, 'weight': 0.06, 'desc': 'Branch'},
                'jsr_rts': {'cycles': 10, 'weight': 0.04, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 28, 'weight': 0.02, 'desc': 'Multiply'},
                'divide': {'cycles': 60, 'weight': 0.02, 'desc': 'Divide'}
            },
            'source': 'MC68020 Users Manual'
        },
        'm6801': {
            'name': 'Motorola 6801', 'year': 1978, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 15000, 'ips_min': 300000, 'ips_max': 600000,
            'cpi_min': 2, 'cpi_max': 8, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'inherent': {'cycles': 2, 'weight': 0.20, 'desc': 'Inherent'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 3, 'weight': 0.20, 'desc': 'Direct'},
                'indexed': {'cycles': 4, 'weight': 0.15, 'desc': 'Indexed'},
                'extended': {'cycles': 4, 'weight': 0.10, 'desc': 'Extended'},
                'branch': {'cycles': 3, 'weight': 0.08, 'desc': 'Branch'},
                'jsr_rts': {'cycles': 6, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 10, 'weight': 0.02, 'desc': 'MUL'},
                'misc': {'cycles': 2, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'MC6801 Data Sheet'
        },
        'm6805': {
            'name': 'Motorola 6805', 'year': 1979, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 8000, 'ips_min': 300000, 'ips_max': 600000,
            'cpi_min': 3, 'cpi_max': 11, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'inherent': {'cycles': 3, 'weight': 0.20, 'desc': 'Inherent'},
                'immediate': {'cycles': 4, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 4, 'weight': 0.20, 'desc': 'Direct'},
                'indexed': {'cycles': 5, 'weight': 0.15, 'desc': 'Indexed'},
                'extended': {'cycles': 5, 'weight': 0.10, 'desc': 'Extended'},
                'branch': {'cycles': 5, 'weight': 0.08, 'desc': 'Branch'},
                'jsr_rts': {'cycles': 9, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'bit_ops': {'cycles': 5, 'weight': 0.02, 'desc': 'BSET, BCLR'},
                'misc': {'cycles': 3, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'MC6805 Data Sheet'
        },
        'm68hc11': {
            'name': 'Motorola 68HC11', 'year': 1985, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 45000, 'ips_min': 500000, 'ips_max': 1000000,
            'cpi_min': 2, 'cpi_max': 8, 'bottleneck': ['memory', 'decode'],
            'categories': {
                'inherent': {'cycles': 2, 'weight': 0.18, 'desc': 'Inherent'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 3, 'weight': 0.18, 'desc': 'Direct'},
                'indexed': {'cycles': 4, 'weight': 0.15, 'desc': 'Indexed'},
                'extended': {'cycles': 4, 'weight': 0.10, 'desc': 'Extended'},
                'branch': {'cycles': 3, 'weight': 0.08, 'desc': 'Branch'},
                'jsr_rts': {'cycles': 5, 'weight': 0.05, 'desc': 'JSR, RTS'},
                'multiply': {'cycles': 10, 'weight': 0.04, 'desc': 'MUL, IDIV'},
                'misc': {'cycles': 2, 'weight': 0.04, 'desc': 'Other'}
            },
            'source': 'MC68HC11 Reference Manual'
        },
        'm68881': {
            'name': 'Motorola 68881', 'year': 1984, 'clock_mhz': 16.0, 'bus_width': 32,
            'transistors': 155000, 'ips_min': 150000, 'ips_max': 500000,
            'cpi_min': 30, 'cpi_max': 120, 'bottleneck': ['execute', 'fpu'],
            'categories': {
                'fmove': {'cycles': 20, 'weight': 0.20, 'desc': 'FMOVE'},
                'fadd': {'cycles': 30, 'weight': 0.20, 'desc': 'FADD'},
                'fsub': {'cycles': 30, 'weight': 0.10, 'desc': 'FSUB'},
                'fmul': {'cycles': 45, 'weight': 0.20, 'desc': 'FMUL'},
                'fdiv': {'cycles': 90, 'weight': 0.10, 'desc': 'FDIV'},
                'fsqrt': {'cycles': 120, 'weight': 0.05, 'desc': 'FSQRT'},
                'fsin_fcos': {'cycles': 200, 'weight': 0.05, 'desc': 'FSIN, FCOS'},
                'fcomp': {'cycles': 25, 'weight': 0.10, 'desc': 'FCMP'}
            },
            'source': 'MC68881 Users Manual'
        },
        'm68882': {
            'name': 'Motorola 68882', 'year': 1985, 'clock_mhz': 25.0, 'bus_width': 32,
            'transistors': 175000, 'ips_min': 250000, 'ips_max': 800000,
            'cpi_min': 25, 'cpi_max': 100, 'bottleneck': ['execute', 'fpu'],
            'categories': {
                'fmove': {'cycles': 15, 'weight': 0.20, 'desc': 'FMOVE'},
                'fadd': {'cycles': 25, 'weight': 0.20, 'desc': 'FADD'},
                'fsub': {'cycles': 25, 'weight': 0.10, 'desc': 'FSUB'},
                'fmul': {'cycles': 35, 'weight': 0.20, 'desc': 'FMUL'},
                'fdiv': {'cycles': 75, 'weight': 0.10, 'desc': 'FDIV'},
                'fsqrt': {'cycles': 100, 'weight': 0.05, 'desc': 'FSQRT'},
                'fsin_fcos': {'cycles': 160, 'weight': 0.05, 'desc': 'FSIN, FCOS'},
                'fcomp': {'cycles': 20, 'weight': 0.10, 'desc': 'FCMP'}
            },
            'source': 'MC68882 Users Manual'
        }
    },
    'mos_wdc': {
        'mos6502': {
            'name': 'MOS 6502', 'year': 1975, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 3510, 'ips_min': 430000, 'ips_max': 1000000,
            'cpi_min': 2, 'cpi_max': 7, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'implied': {'cycles': 2, 'weight': 0.18, 'desc': 'TAX, INX, etc.'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'LDA #imm'},
                'zero_page': {'cycles': 3, 'weight': 0.22, 'desc': 'LDA $00'},
                'zero_page_x': {'cycles': 4, 'weight': 0.10, 'desc': 'LDA $00,X'},
                'absolute': {'cycles': 4, 'weight': 0.10, 'desc': 'LDA $0000'},
                'absolute_x': {'cycles': 5, 'weight': 0.05, 'desc': 'LDA $0000,X (+1 page)'},
                'branch_taken': {'cycles': 3, 'weight': 0.08, 'desc': 'BNE taken'},
                'branch_not_taken': {'cycles': 2, 'weight': 0.04, 'desc': 'BNE not taken'},
                'jsr_rts': {'cycles': 6, 'weight': 0.05, 'desc': 'JSR=6, RTS=6'}
            },
            'source': 'MOS 6500 Hardware Manual'
        },
        'mos6510': {
            'name': 'MOS 6510', 'year': 1982, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 4000, 'ips_min': 430000, 'ips_max': 1000000,
            'cpi_min': 2, 'cpi_max': 7, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'implied': {'cycles': 2, 'weight': 0.18, 'desc': 'Implied'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'zero_page': {'cycles': 3, 'weight': 0.22, 'desc': 'Zero page'},
                'zero_page_x': {'cycles': 4, 'weight': 0.10, 'desc': 'Zero page,X'},
                'absolute': {'cycles': 4, 'weight': 0.10, 'desc': 'Absolute'},
                'absolute_x': {'cycles': 5, 'weight': 0.05, 'desc': 'Absolute,X'},
                'branch_taken': {'cycles': 3, 'weight': 0.08, 'desc': 'Branch taken'},
                'branch_not_taken': {'cycles': 2, 'weight': 0.04, 'desc': 'Branch not taken'},
                'jsr_rts': {'cycles': 6, 'weight': 0.05, 'desc': 'JSR, RTS'}
            },
            'source': 'MOS 6510 Data Sheet'
        },
        'wdc65c02': {
            'name': 'WDC 65C02', 'year': 1983, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 4500, 'ips_min': 900000, 'ips_max': 2000000,
            'cpi_min': 2, 'cpi_max': 6, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'implied': {'cycles': 2, 'weight': 0.18, 'desc': 'Implied'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'zero_page': {'cycles': 3, 'weight': 0.22, 'desc': 'Zero page'},
                'zero_page_x': {'cycles': 4, 'weight': 0.10, 'desc': 'Zero page,X'},
                'absolute': {'cycles': 4, 'weight': 0.10, 'desc': 'Absolute'},
                'indirect_zp': {'cycles': 5, 'weight': 0.05, 'desc': '(ZP) indirect'},
                'branch_taken': {'cycles': 3, 'weight': 0.08, 'desc': 'Branch taken'},
                'branch_not_taken': {'cycles': 2, 'weight': 0.04, 'desc': 'Branch not taken'},
                'jsr_rts': {'cycles': 6, 'weight': 0.05, 'desc': 'JSR, RTS'}
            },
            'source': 'WDC 65C02 Data Sheet'
        },
        'wdc65816': {
            'name': 'WDC 65816', 'year': 1984, 'clock_mhz': 2.8, 'bus_width': 16,
            'transistors': 22000, 'ips_min': 1000000, 'ips_max': 2500000,
            'cpi_min': 2, 'cpi_max': 8, 'bottleneck': ['memory', 'fetch'],
            'categories': {
                'implied': {'cycles': 2, 'weight': 0.15, 'desc': 'Implied'},
                'immediate': {'cycles': 2, 'weight': 0.18, 'desc': 'Immediate'},
                'direct': {'cycles': 3, 'weight': 0.18, 'desc': 'Direct page'},
                'direct_x': {'cycles': 4, 'weight': 0.10, 'desc': 'Direct,X'},
                'absolute': {'cycles': 4, 'weight': 0.12, 'desc': 'Absolute'},
                'long': {'cycles': 5, 'weight': 0.08, 'desc': 'Long addressing'},
                'branch_taken': {'cycles': 3, 'weight': 0.08, 'desc': 'Branch taken'},
                'branch_not_taken': {'cycles': 2, 'weight': 0.04, 'desc': 'Branch not taken'},
                'jsr_rts': {'cycles': 8, 'weight': 0.07, 'desc': 'JSR, RTS'}
            },
            'source': 'WDC 65816 Data Sheet'
        }
    },
    'zilog': {
        'z80': {
            'name': 'Zilog Z80', 'year': 1976, 'clock_mhz': 2.5, 'bus_width': 8,
            'transistors': 8500, 'ips_min': 290000, 'ips_max': 800000,
            'cpi_min': 4, 'cpi_max': 23, 'bottleneck': ['decode', 'fetch'],
            'categories': {
                'ld_r_r': {'cycles': 4, 'weight': 0.20, 'desc': 'LD r,r'},
                'ld_r_n': {'cycles': 7, 'weight': 0.12, 'desc': 'LD r,n'},
                'ld_r_hl': {'cycles': 7, 'weight': 0.15, 'desc': 'LD r,(HL)'},
                'ld_r_ix': {'cycles': 19, 'weight': 0.05, 'desc': 'LD r,(IX+d)'},
                'alu_r': {'cycles': 4, 'weight': 0.18, 'desc': 'ADD, SUB, etc.'},
                'alu_hl': {'cycles': 7, 'weight': 0.08, 'desc': 'ADD A,(HL)'},
                'jp': {'cycles': 10, 'weight': 0.08, 'desc': 'JP nn'},
                'jr_taken': {'cycles': 12, 'weight': 0.05, 'desc': 'JR cc taken'},
                'jr_not_taken': {'cycles': 7, 'weight': 0.03, 'desc': 'JR cc not taken'},
                'call_ret': {'cycles': 17, 'weight': 0.04, 'desc': 'CALL, RET'},
                'push_pop': {'cycles': 11, 'weight': 0.02, 'desc': 'PUSH, POP'}
            },
            'source': 'Z80 CPU Users Manual'
        },
        'z80a': {
            'name': 'Zilog Z80A', 'year': 1978, 'clock_mhz': 4.0, 'bus_width': 8,
            'transistors': 8500, 'ips_min': 460000, 'ips_max': 1280000,
            'cpi_min': 4, 'cpi_max': 23, 'bottleneck': ['decode', 'fetch'],
            'categories': {
                'ld_r_r': {'cycles': 4, 'weight': 0.20, 'desc': 'LD r,r'},
                'ld_r_n': {'cycles': 7, 'weight': 0.12, 'desc': 'LD r,n'},
                'ld_r_hl': {'cycles': 7, 'weight': 0.15, 'desc': 'LD r,(HL)'},
                'ld_r_ix': {'cycles': 19, 'weight': 0.05, 'desc': 'LD r,(IX+d)'},
                'alu_r': {'cycles': 4, 'weight': 0.18, 'desc': 'ALU register'},
                'alu_hl': {'cycles': 7, 'weight': 0.08, 'desc': 'ALU (HL)'},
                'jp': {'cycles': 10, 'weight': 0.08, 'desc': 'JP'},
                'jr_taken': {'cycles': 12, 'weight': 0.05, 'desc': 'JR taken'},
                'jr_not_taken': {'cycles': 7, 'weight': 0.03, 'desc': 'JR not taken'},
                'call_ret': {'cycles': 17, 'weight': 0.04, 'desc': 'CALL, RET'},
                'push_pop': {'cycles': 11, 'weight': 0.02, 'desc': 'PUSH, POP'}
            },
            'source': 'Z80A Data Sheet'
        },
        'z80b': {
            'name': 'Zilog Z80B', 'year': 1980, 'clock_mhz': 6.0, 'bus_width': 8,
            'transistors': 8500, 'ips_min': 690000, 'ips_max': 1920000,
            'cpi_min': 4, 'cpi_max': 23, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'ld_r_r': {'cycles': 4, 'weight': 0.20, 'desc': 'LD r,r'},
                'ld_r_n': {'cycles': 7, 'weight': 0.12, 'desc': 'LD r,n'},
                'ld_r_hl': {'cycles': 7, 'weight': 0.15, 'desc': 'LD r,(HL)'},
                'ld_r_ix': {'cycles': 19, 'weight': 0.05, 'desc': 'LD r,(IX+d)'},
                'alu_r': {'cycles': 4, 'weight': 0.18, 'desc': 'ALU register'},
                'alu_hl': {'cycles': 7, 'weight': 0.08, 'desc': 'ALU (HL)'},
                'jp': {'cycles': 10, 'weight': 0.08, 'desc': 'JP'},
                'jr_taken': {'cycles': 12, 'weight': 0.05, 'desc': 'JR taken'},
                'jr_not_taken': {'cycles': 7, 'weight': 0.03, 'desc': 'JR not taken'},
                'call_ret': {'cycles': 17, 'weight': 0.04, 'desc': 'CALL, RET'},
                'push_pop': {'cycles': 11, 'weight': 0.02, 'desc': 'PUSH, POP'}
            },
            'source': 'Z80B Data Sheet'
        },
        'z8000': {
            'name': 'Zilog Z8000', 'year': 1979, 'clock_mhz': 4.0, 'bus_width': 16,
            'transistors': 17500, 'ips_min': 500000, 'ips_max': 1200000,
            'cpi_min': 3, 'cpi_max': 12, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'ld_r_r': {'cycles': 3, 'weight': 0.22, 'desc': 'LD R,R'},
                'ld_r_im': {'cycles': 4, 'weight': 0.15, 'desc': 'LD R,#imm'},
                'ld_r_mem': {'cycles': 7, 'weight': 0.18, 'desc': 'LD R,@addr'},
                'alu_r': {'cycles': 4, 'weight': 0.20, 'desc': 'ADD, SUB, etc.'},
                'alu_mem': {'cycles': 8, 'weight': 0.08, 'desc': 'ALU with memory'},
                'jp': {'cycles': 6, 'weight': 0.08, 'desc': 'JP cc'},
                'call_ret': {'cycles': 12, 'weight': 0.05, 'desc': 'CALL, RET'},
                'multiply': {'cycles': 70, 'weight': 0.02, 'desc': 'MULT'},
                'divide': {'cycles': 107, 'weight': 0.02, 'desc': 'DIV'}
            },
            'source': 'Z8000 CPU Users Manual'
        },
        'z80000': {
            'name': 'Zilog Z80000', 'year': 1986, 'clock_mhz': 25.0, 'bus_width': 32,
            'transistors': 91000, 'ips_min': 4000000, 'ips_max': 10000000,
            'cpi_min': 2, 'cpi_max': 8, 'bottleneck': ['cache', 'memory'],
            'categories': {
                'ld_r_r': {'cycles': 2, 'weight': 0.25, 'desc': 'LD R,R'},
                'ld_r_mem': {'cycles': 4, 'weight': 0.20, 'desc': 'LD R,@addr'},
                'alu_r': {'cycles': 2, 'weight': 0.25, 'desc': 'ALU register'},
                'alu_mem': {'cycles': 5, 'weight': 0.10, 'desc': 'ALU memory'},
                'jp': {'cycles': 4, 'weight': 0.08, 'desc': 'JP'},
                'call_ret': {'cycles': 8, 'weight': 0.05, 'desc': 'CALL, RET'},
                'multiply': {'cycles': 15, 'weight': 0.04, 'desc': 'MULT'},
                'divide': {'cycles': 30, 'weight': 0.03, 'desc': 'DIV'}
            },
            'source': 'Z80000 CPU Manual'
        },
        'z8': {
            'name': 'Zilog Z8', 'year': 1979, 'clock_mhz': 8.0, 'bus_width': 8,
            'transistors': 9000, 'ips_min': 500000, 'ips_max': 1000000,
            'cpi_min': 6, 'cpi_max': 20, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'ld_r_r': {'cycles': 6, 'weight': 0.22, 'desc': 'LD r,r'},
                'ld_r_im': {'cycles': 6, 'weight': 0.15, 'desc': 'LD r,#imm'},
                'ld_r_ir': {'cycles': 8, 'weight': 0.15, 'desc': 'LD r,@Rr'},
                'alu_r': {'cycles': 6, 'weight': 0.20, 'desc': 'ALU r,r'},
                'jp': {'cycles': 10, 'weight': 0.10, 'desc': 'JP cc'},
                'call_ret': {'cycles': 14, 'weight': 0.08, 'desc': 'CALL, RET'},
                'djnz': {'cycles': 12, 'weight': 0.05, 'desc': 'DJNZ'},
                'misc': {'cycles': 6, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'Z8 MCU Users Manual'
        },
        'z180': {
            'name': 'Zilog Z180', 'year': 1985, 'clock_mhz': 6.0, 'bus_width': 8,
            'transistors': 20000, 'ips_min': 900000, 'ips_max': 2000000,
            'cpi_min': 3, 'cpi_max': 18, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'ld_r_r': {'cycles': 3, 'weight': 0.22, 'desc': 'LD r,r'},
                'ld_r_n': {'cycles': 5, 'weight': 0.12, 'desc': 'LD r,n'},
                'ld_r_hl': {'cycles': 5, 'weight': 0.15, 'desc': 'LD r,(HL)'},
                'alu_r': {'cycles': 3, 'weight': 0.20, 'desc': 'ALU r'},
                'alu_hl': {'cycles': 5, 'weight': 0.08, 'desc': 'ALU (HL)'},
                'jp': {'cycles': 8, 'weight': 0.08, 'desc': 'JP'},
                'jr_taken': {'cycles': 10, 'weight': 0.05, 'desc': 'JR taken'},
                'call_ret': {'cycles': 14, 'weight': 0.05, 'desc': 'CALL, RET'},
                'multiply': {'cycles': 18, 'weight': 0.03, 'desc': 'MLT'},
                'push_pop': {'cycles': 9, 'weight': 0.02, 'desc': 'PUSH, POP'}
            },
            'source': 'Z180 Users Manual'
        }
    },
    'other': {
        'rca1802': {
            'name': 'RCA 1802', 'year': 1976, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 5000, 'ips_min': 125000, 'ips_max': 400000,
            'cpi_min': 8, 'cpi_max': 24, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'short_branch': {'cycles': 8, 'weight': 0.15, 'desc': 'Short branch'},
                'long_branch': {'cycles': 16, 'weight': 0.08, 'desc': 'Long branch'},
                'memory_ref': {'cycles': 8, 'weight': 0.20, 'desc': 'Memory reference'},
                'reg_ops': {'cycles': 8, 'weight': 0.25, 'desc': 'Register ops'},
                'immediate': {'cycles': 16, 'weight': 0.12, 'desc': 'Immediate'},
                'io_ops': {'cycles': 8, 'weight': 0.10, 'desc': 'I/O operations'},
                'control': {'cycles': 8, 'weight': 0.05, 'desc': 'Control'},
                'subroutine': {'cycles': 24, 'weight': 0.05, 'desc': 'SEP, RET'}
            },
            'source': 'RCA CDP1802 Users Manual'
        },
        'rca1805': {
            'name': 'RCA 1805', 'year': 1977, 'clock_mhz': 3.0, 'bus_width': 8,
            'transistors': 6000, 'ips_min': 187000, 'ips_max': 600000,
            'cpi_min': 8, 'cpi_max': 24, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'short_branch': {'cycles': 8, 'weight': 0.15, 'desc': 'Short branch'},
                'long_branch': {'cycles': 16, 'weight': 0.08, 'desc': 'Long branch'},
                'memory_ref': {'cycles': 8, 'weight': 0.20, 'desc': 'Memory reference'},
                'reg_ops': {'cycles': 8, 'weight': 0.25, 'desc': 'Register ops'},
                'immediate': {'cycles': 16, 'weight': 0.12, 'desc': 'Immediate'},
                'io_ops': {'cycles': 8, 'weight': 0.10, 'desc': 'I/O operations'},
                'control': {'cycles': 8, 'weight': 0.05, 'desc': 'Control'},
                'subroutine': {'cycles': 24, 'weight': 0.05, 'desc': 'Subroutine'}
            },
            'source': 'RCA CDP1805 Data Sheet'
        },
        'scmp': {
            'name': 'National SC/MP', 'year': 1974, 'clock_mhz': 1.0, 'bus_width': 8,
            'transistors': 5000, 'ips_min': 50000, 'ips_max': 150000,
            'cpi_min': 7, 'cpi_max': 22, 'bottleneck': ['fetch', 'serial_bus'],
            'categories': {
                'implied': {'cycles': 7, 'weight': 0.20, 'desc': 'Implied'},
                'immediate': {'cycles': 10, 'weight': 0.18, 'desc': 'Immediate'},
                'memory': {'cycles': 18, 'weight': 0.20, 'desc': 'Memory'},
                'auto_indexed': {'cycles': 18, 'weight': 0.10, 'desc': 'Auto-indexed'},
                'branch': {'cycles': 9, 'weight': 0.12, 'desc': 'Branch'},
                'transfer': {'cycles': 7, 'weight': 0.10, 'desc': 'Transfer'},
                'io': {'cycles': 22, 'weight': 0.05, 'desc': 'I/O'},
                'misc': {'cycles': 7, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'National SC/MP Programmers Guide'
        },
        'f8': {
            'name': 'Fairchild F8', 'year': 1975, 'clock_mhz': 2.0, 'bus_width': 8,
            'transistors': 4000, 'ips_min': 200000, 'ips_max': 500000,
            'cpi_min': 4, 'cpi_max': 13, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'accumulator': {'cycles': 4, 'weight': 0.25, 'desc': 'Accumulator ops'},
                'scratchpad': {'cycles': 4, 'weight': 0.20, 'desc': 'Scratchpad'},
                'memory': {'cycles': 8, 'weight': 0.15, 'desc': 'Memory'},
                'immediate': {'cycles': 5, 'weight': 0.15, 'desc': 'Immediate'},
                'branch': {'cycles': 8, 'weight': 0.10, 'desc': 'Branch'},
                'call_return': {'cycles': 13, 'weight': 0.08, 'desc': 'PI, POP'},
                'io': {'cycles': 8, 'weight': 0.05, 'desc': 'I/O'},
                'misc': {'cycles': 4, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'Fairchild F8 Users Guide'
        },
        'signetics2650': {
            'name': 'Signetics 2650', 'year': 1975, 'clock_mhz': 1.25, 'bus_width': 8,
            'transistors': 6000, 'ips_min': 200000, 'ips_max': 500000,
            'cpi_min': 2, 'cpi_max': 9, 'bottleneck': ['fetch', 'decode'],
            'categories': {
                'register': {'cycles': 2, 'weight': 0.25, 'desc': 'Register ops'},
                'immediate': {'cycles': 4, 'weight': 0.18, 'desc': 'Immediate'},
                'absolute': {'cycles': 6, 'weight': 0.15, 'desc': 'Absolute'},
                'relative': {'cycles': 6, 'weight': 0.12, 'desc': 'Relative'},
                'indirect': {'cycles': 9, 'weight': 0.08, 'desc': 'Indirect'},
                'branch': {'cycles': 5, 'weight': 0.10, 'desc': 'Branch'},
                'call_return': {'cycles': 9, 'weight': 0.07, 'desc': 'ZBSR, RETC'},
                'io': {'cycles': 6, 'weight': 0.05, 'desc': 'I/O'}
            },
            'source': 'Signetics 2650 Microprocessor Manual'
        },
        'am2901': {
            'name': 'AMD Am2901', 'year': 1975, 'clock_mhz': 10.0, 'bus_width': 4,
            'transistors': 1700, 'ips_min': 2000000, 'ips_max': 10000000,
            'cpi_min': 1, 'cpi_max': 5, 'bottleneck': ['microcode', 'external'],
            'categories': {
                'alu_pass': {'cycles': 1, 'weight': 0.30, 'desc': 'ALU pass through'},
                'alu_add': {'cycles': 1, 'weight': 0.25, 'desc': 'ALU add'},
                'alu_sub': {'cycles': 1, 'weight': 0.15, 'desc': 'ALU subtract'},
                'alu_logic': {'cycles': 1, 'weight': 0.15, 'desc': 'ALU logic ops'},
                'shift': {'cycles': 2, 'weight': 0.08, 'desc': 'Shift operations'},
                'ram_access': {'cycles': 1, 'weight': 0.05, 'desc': 'RAM access'},
                'output': {'cycles': 1, 'weight': 0.02, 'desc': 'Output'}
            },
            'source': 'AMD Am2901 Data Sheet'
        },
        'am2903': {
            'name': 'AMD Am2903', 'year': 1976, 'clock_mhz': 12.5, 'bus_width': 4,
            'transistors': 2000, 'ips_min': 2500000, 'ips_max': 12500000,
            'cpi_min': 1, 'cpi_max': 5, 'bottleneck': ['microcode', 'external'],
            'categories': {
                'alu_pass': {'cycles': 1, 'weight': 0.28, 'desc': 'ALU pass through'},
                'alu_add': {'cycles': 1, 'weight': 0.25, 'desc': 'ALU add'},
                'alu_sub': {'cycles': 1, 'weight': 0.15, 'desc': 'ALU subtract'},
                'alu_logic': {'cycles': 1, 'weight': 0.15, 'desc': 'ALU logic ops'},
                'shift': {'cycles': 2, 'weight': 0.08, 'desc': 'Shift operations'},
                'multiply': {'cycles': 4, 'weight': 0.05, 'desc': 'Hardware multiply'},
                'ram_access': {'cycles': 1, 'weight': 0.04, 'desc': 'RAM access'}
            },
            'source': 'AMD Am2903 Data Sheet'
        },
        'am29000': {
            'name': 'AMD Am29000', 'year': 1987, 'clock_mhz': 25.0, 'bus_width': 32,
            'transistors': 300000, 'ips_min': 15000000, 'ips_max': 25000000,
            'cpi_min': 1, 'cpi_max': 4, 'bottleneck': ['cache', 'pipeline'],
            'categories': {
                'alu_reg': {'cycles': 1, 'weight': 0.30, 'desc': 'ALU register'},
                'load': {'cycles': 2, 'weight': 0.18, 'desc': 'Load'},
                'store': {'cycles': 2, 'weight': 0.10, 'desc': 'Store'},
                'branch': {'cycles': 1, 'weight': 0.12, 'desc': 'Branch (delay slot)'},
                'call_ret': {'cycles': 4, 'weight': 0.08, 'desc': 'CALL, RET'},
                'multiply': {'cycles': 2, 'weight': 0.10, 'desc': 'Multiply'},
                'divide': {'cycles': 35, 'weight': 0.02, 'desc': 'Divide'},
                'misc': {'cycles': 1, 'weight': 0.10, 'desc': 'Other'}
            },
            'source': 'AMD Am29000 Users Manual'
        },
        'tms9900': {
            'name': 'TI TMS9900', 'year': 1976, 'clock_mhz': 3.0, 'bus_width': 16,
            'transistors': 8000, 'ips_min': 300000, 'ips_max': 700000,
            'cpi_min': 8, 'cpi_max': 52, 'bottleneck': ['memory', 'workspace'],
            'categories': {
                'register': {'cycles': 14, 'weight': 0.20, 'desc': 'Register-register'},
                'immediate': {'cycles': 14, 'weight': 0.15, 'desc': 'Immediate'},
                'memory': {'cycles': 22, 'weight': 0.18, 'desc': 'Memory'},
                'indexed': {'cycles': 26, 'weight': 0.10, 'desc': 'Indexed'},
                'jump': {'cycles': 10, 'weight': 0.12, 'desc': 'Jump'},
                'cru': {'cycles': 12, 'weight': 0.08, 'desc': 'CRU bit ops'},
                'shift': {'cycles': 20, 'weight': 0.05, 'desc': 'Shift'},
                'multiply': {'cycles': 52, 'weight': 0.05, 'desc': 'MPY'},
                'divide': {'cycles': 92, 'weight': 0.02, 'desc': 'DIV'},
                'blwp': {'cycles': 26, 'weight': 0.05, 'desc': 'BLWP context switch'}
            },
            'source': 'TI TMS9900 Users Guide'
        },
        'tms9995': {
            'name': 'TI TMS9995', 'year': 1981, 'clock_mhz': 12.0, 'bus_width': 8,
            'transistors': 24000, 'ips_min': 500000, 'ips_max': 1200000,
            'cpi_min': 8, 'cpi_max': 40, 'bottleneck': ['memory', 'bus_width'],
            'categories': {
                'register': {'cycles': 8, 'weight': 0.22, 'desc': 'Register-register'},
                'immediate': {'cycles': 10, 'weight': 0.15, 'desc': 'Immediate'},
                'memory': {'cycles': 16, 'weight': 0.18, 'desc': 'Memory'},
                'jump': {'cycles': 8, 'weight': 0.12, 'desc': 'Jump'},
                'cru': {'cycles': 10, 'weight': 0.08, 'desc': 'CRU bit ops'},
                'shift': {'cycles': 14, 'weight': 0.08, 'desc': 'Shift'},
                'multiply': {'cycles': 40, 'weight': 0.05, 'desc': 'MPY'},
                'divide': {'cycles': 60, 'weight': 0.02, 'desc': 'DIV'},
                'blwp': {'cycles': 18, 'weight': 0.05, 'desc': 'Context switch'},
                'misc': {'cycles': 8, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'TI TMS9995 Users Guide'
        },
        'tms320c10': {
            'name': 'TI TMS320C10', 'year': 1983, 'clock_mhz': 20.0, 'bus_width': 16,
            'transistors': 15000, 'ips_min': 5000000, 'ips_max': 10000000,
            'cpi_min': 1, 'cpi_max': 4, 'bottleneck': ['memory', 'pipeline'],
            'categories': {
                'accumulator': {'cycles': 1, 'weight': 0.30, 'desc': 'Accumulator ops'},
                'mac': {'cycles': 1, 'weight': 0.25, 'desc': 'MAC (multiply-accumulate)'},
                'load_store': {'cycles': 1, 'weight': 0.15, 'desc': 'Load/Store'},
                'branch': {'cycles': 2, 'weight': 0.10, 'desc': 'Branch'},
                'call_ret': {'cycles': 2, 'weight': 0.08, 'desc': 'CALL, RET'},
                'io': {'cycles': 2, 'weight': 0.07, 'desc': 'I/O'},
                'misc': {'cycles': 1, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'TI TMS320C1x Users Guide'
        },
        'ns32016': {
            'name': 'National NS32016', 'year': 1982, 'clock_mhz': 10.0, 'bus_width': 16,
            'transistors': 60000, 'ips_min': 800000, 'ips_max': 2000000,
            'cpi_min': 5, 'cpi_max': 25, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_reg': {'cycles': 5, 'weight': 0.22, 'desc': 'MOV reg,reg'},
                'mov_mem': {'cycles': 12, 'weight': 0.18, 'desc': 'MOV mem,reg'},
                'alu_reg': {'cycles': 5, 'weight': 0.22, 'desc': 'ALU reg,reg'},
                'alu_mem': {'cycles': 14, 'weight': 0.10, 'desc': 'ALU mem,reg'},
                'branch': {'cycles': 8, 'weight': 0.10, 'desc': 'Branch'},
                'call_ret': {'cycles': 20, 'weight': 0.06, 'desc': 'BSR, RET'},
                'multiply': {'cycles': 25, 'weight': 0.05, 'desc': 'MUL'},
                'divide': {'cycles': 50, 'weight': 0.02, 'desc': 'DIV'},
                'misc': {'cycles': 5, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'NS32016 Data Sheet'
        },
        'ns32032': {
            'name': 'National NS32032', 'year': 1984, 'clock_mhz': 15.0, 'bus_width': 32,
            'transistors': 80000, 'ips_min': 1500000, 'ips_max': 4000000,
            'cpi_min': 4, 'cpi_max': 20, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_reg': {'cycles': 4, 'weight': 0.25, 'desc': 'MOV reg,reg'},
                'mov_mem': {'cycles': 8, 'weight': 0.18, 'desc': 'MOV mem,reg'},
                'alu_reg': {'cycles': 4, 'weight': 0.25, 'desc': 'ALU reg,reg'},
                'alu_mem': {'cycles': 10, 'weight': 0.10, 'desc': 'ALU mem,reg'},
                'branch': {'cycles': 6, 'weight': 0.08, 'desc': 'Branch'},
                'call_ret': {'cycles': 15, 'weight': 0.06, 'desc': 'BSR, RET'},
                'multiply': {'cycles': 18, 'weight': 0.04, 'desc': 'MUL'},
                'divide': {'cycles': 35, 'weight': 0.02, 'desc': 'DIV'},
                'misc': {'cycles': 4, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'NS32032 Data Sheet'
        },
        'r2000': {
            'name': 'MIPS R2000', 'year': 1985, 'clock_mhz': 8.0, 'bus_width': 32,
            'transistors': 110000, 'ips_min': 5000000, 'ips_max': 10000000,
            'cpi_min': 1, 'cpi_max': 3, 'bottleneck': ['pipeline', 'cache'],
            'categories': {
                'alu_reg': {'cycles': 1, 'weight': 0.30, 'desc': 'ALU R-type'},
                'load': {'cycles': 2, 'weight': 0.20, 'desc': 'LW (load delay)'},
                'store': {'cycles': 1, 'weight': 0.12, 'desc': 'SW'},
                'branch': {'cycles': 1, 'weight': 0.12, 'desc': 'BEQ, BNE (delay slot)'},
                'jump': {'cycles': 1, 'weight': 0.08, 'desc': 'J, JAL'},
                'immediate': {'cycles': 1, 'weight': 0.10, 'desc': 'ADDI, ORI, etc.'},
                'multiply': {'cycles': 12, 'weight': 0.05, 'desc': 'MULT'},
                'divide': {'cycles': 35, 'weight': 0.03, 'desc': 'DIV'}
            },
            'source': 'MIPS R2000 Users Manual'
        },
        'sparc': {
            'name': 'Sun SPARC', 'year': 1987, 'clock_mhz': 16.0, 'bus_width': 32,
            'transistors': 100000, 'ips_min': 10000000, 'ips_max': 20000000,
            'cpi_min': 1, 'cpi_max': 3, 'bottleneck': ['pipeline', 'cache'],
            'categories': {
                'alu_reg': {'cycles': 1, 'weight': 0.32, 'desc': 'ALU register'},
                'load': {'cycles': 2, 'weight': 0.18, 'desc': 'Load (delay slot)'},
                'store': {'cycles': 1, 'weight': 0.10, 'desc': 'Store'},
                'branch': {'cycles': 1, 'weight': 0.12, 'desc': 'Branch (delay slot)'},
                'call_ret': {'cycles': 2, 'weight': 0.08, 'desc': 'CALL, RET'},
                'save_restore': {'cycles': 1, 'weight': 0.05, 'desc': 'Register windows'},
                'immediate': {'cycles': 1, 'weight': 0.08, 'desc': 'Immediate'},
                'multiply': {'cycles': 5, 'weight': 0.05, 'desc': 'SMUL'},
                'divide': {'cycles': 18, 'weight': 0.02, 'desc': 'SDIV'}
            },
            'source': 'SPARC Architecture Manual'
        },
        'arm1': {
            'name': 'Acorn ARM1', 'year': 1985, 'clock_mhz': 8.0, 'bus_width': 32,
            'transistors': 25000, 'ips_min': 4000000, 'ips_max': 8000000,
            'cpi_min': 1, 'cpi_max': 4, 'bottleneck': ['memory', 'pipeline'],
            'categories': {
                'data_proc': {'cycles': 1, 'weight': 0.35, 'desc': 'Data processing'},
                'load_single': {'cycles': 3, 'weight': 0.18, 'desc': 'LDR'},
                'store_single': {'cycles': 2, 'weight': 0.10, 'desc': 'STR'},
                'load_multiple': {'cycles': 4, 'weight': 0.05, 'desc': 'LDM'},
                'branch': {'cycles': 3, 'weight': 0.12, 'desc': 'B, BL'},
                'branch_link': {'cycles': 4, 'weight': 0.05, 'desc': 'BL'},
                'multiply': {'cycles': 16, 'weight': 0.05, 'desc': 'MUL'},
                'swi': {'cycles': 4, 'weight': 0.02, 'desc': 'SWI'},
                'misc': {'cycles': 1, 'weight': 0.08, 'desc': 'Other'}
            },
            'source': 'ARM1 Technical Reference Manual'
        },
        't414': {
            'name': 'Inmos T414', 'year': 1985, 'clock_mhz': 15.0, 'bus_width': 32,
            'transistors': 200000, 'ips_min': 5000000, 'ips_max': 10000000,
            'cpi_min': 1, 'cpi_max': 6, 'bottleneck': ['memory', 'channel'],
            'categories': {
                'direct': {'cycles': 1, 'weight': 0.35, 'desc': 'Direct functions'},
                'indirect': {'cycles': 2, 'weight': 0.20, 'desc': 'Indirect functions'},
                'load_store': {'cycles': 2, 'weight': 0.15, 'desc': 'Load/Store'},
                'jump': {'cycles': 3, 'weight': 0.10, 'desc': 'Jump'},
                'call': {'cycles': 4, 'weight': 0.05, 'desc': 'CALL'},
                'channel': {'cycles': 6, 'weight': 0.08, 'desc': 'Channel comms'},
                'alt': {'cycles': 10, 'weight': 0.03, 'desc': 'ALT'},
                'misc': {'cycles': 1, 'weight': 0.04, 'desc': 'Other'}
            },
            'source': 'Inmos T414 Technical Manual'
        },
        'we32000': {
            'name': 'AT&T WE 32000', 'year': 1982, 'clock_mhz': 14.0, 'bus_width': 32,
            'transistors': 145000, 'ips_min': 1000000, 'ips_max': 3000000,
            'cpi_min': 4, 'cpi_max': 15, 'bottleneck': ['decode', 'memory'],
            'categories': {
                'mov_reg': {'cycles': 4, 'weight': 0.22, 'desc': 'MOV reg,reg'},
                'mov_mem': {'cycles': 8, 'weight': 0.18, 'desc': 'MOV mem,reg'},
                'alu_reg': {'cycles': 4, 'weight': 0.22, 'desc': 'ALU reg,reg'},
                'alu_mem': {'cycles': 10, 'weight': 0.10, 'desc': 'ALU mem,reg'},
                'branch': {'cycles': 6, 'weight': 0.10, 'desc': 'Branch'},
                'call_ret': {'cycles': 12, 'weight': 0.06, 'desc': 'JSB, RSB'},
                'multiply': {'cycles': 15, 'weight': 0.05, 'desc': 'MULW'},
                'divide': {'cycles': 30, 'weight': 0.02, 'desc': 'DIVW'},
                'misc': {'cycles': 4, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'WE 32000 Users Manual'
        },
        'rtx2000': {
            'name': 'Harris RTX2000', 'year': 1988, 'clock_mhz': 10.0, 'bus_width': 16,
            'transistors': 15000, 'ips_min': 8000000, 'ips_max': 12000000,
            'cpi_min': 1, 'cpi_max': 2, 'bottleneck': ['stack', 'memory'],
            'categories': {
                'alu': {'cycles': 1, 'weight': 0.40, 'desc': 'ALU operations'},
                'stack': {'cycles': 1, 'weight': 0.20, 'desc': 'Stack operations'},
                'memory': {'cycles': 2, 'weight': 0.15, 'desc': 'Memory access'},
                'call_ret': {'cycles': 1, 'weight': 0.10, 'desc': 'CALL, RET'},
                'branch': {'cycles': 2, 'weight': 0.08, 'desc': 'Branch'},
                'multiply': {'cycles': 2, 'weight': 0.05, 'desc': 'Multiply'},
                'misc': {'cycles': 1, 'weight': 0.02, 'desc': 'Other'}
            },
            'source': 'Harris RTX2000 Data Sheet'
        },
        'nc4016': {
            'name': 'Novix NC4016', 'year': 1985, 'clock_mhz': 8.0, 'bus_width': 16,
            'transistors': 12000, 'ips_min': 6000000, 'ips_max': 10000000,
            'cpi_min': 1, 'cpi_max': 2, 'bottleneck': ['stack', 'memory'],
            'categories': {
                'alu': {'cycles': 1, 'weight': 0.40, 'desc': 'ALU operations'},
                'stack': {'cycles': 1, 'weight': 0.25, 'desc': 'Stack operations'},
                'memory': {'cycles': 2, 'weight': 0.12, 'desc': 'Memory access'},
                'call_ret': {'cycles': 1, 'weight': 0.10, 'desc': 'CALL, RET'},
                'branch': {'cycles': 2, 'weight': 0.08, 'desc': 'Branch'},
                'misc': {'cycles': 1, 'weight': 0.05, 'desc': 'Other'}
            },
            'source': 'Novix NC4016 Data Sheet'
        }
    }
}


def generate_model_py(family: str, proc_id: str, proc_data: dict) -> str:
    """Generate Python model file content."""
    categories_str = ""
    for cat_name, cat_data in proc_data['categories'].items():
        categories_str += f"""    '{cat_name}': {{
        'cycles': {cat_data['cycles']},
        'weight': {cat_data['weight']},
        'description': '{cat_data['desc']}',
        'source': '{proc_data['source']}'
    }},
"""

    return f'''#!/usr/bin/env python3
"""
{proc_data['name']} Performance Model

Grey-box queueing model for the {proc_data['name']} microprocessor ({proc_data['year']}).

Specifications:
- Clock: {proc_data['clock_mhz']} MHz
- Bus Width: {proc_data['bus_width']}-bit
- Transistors: {proc_data['transistors']:,}

Source: {proc_data['source']}
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from common.queueing import QueueingModel
from common.validation import create_standard_suite


# Processor configuration
CONFIG = {{
    'name': '{proc_data['name']}',
    'year': {proc_data['year']},
    'clock_mhz': {proc_data['clock_mhz']},
    'bus_width': {proc_data['bus_width']},
    'transistors': {proc_data['transistors']}
}}

# Timing categories (5-15 categories capturing major instruction classes)
TIMING_CATEGORIES = {{
{categories_str}}}

# Validation targets from documentation
VALIDATION_TARGETS = {{
    'ips_min': {proc_data['ips_min']},
    'ips_max': {proc_data['ips_max']},
    'cpi_min': {proc_data['cpi_min']},
    'cpi_max': {proc_data['cpi_max']},
    'expected_bottlenecks': {proc_data['bottleneck']},
    'source': '{proc_data['source']}'
}}

# Create the queueing model
MODEL = QueueingModel(
    clock_mhz=CONFIG['clock_mhz'],
    timing_categories=TIMING_CATEGORIES,
    bus_width=CONFIG['bus_width']
)


def analyze(workload='typical'):
    """Analyze processor performance with given workload."""
    return MODEL.analyze(workload)


def validate():
    """Run validation suite."""
    result = analyze('typical')
    suite = create_standard_suite(
        CONFIG['name'],
        (VALIDATION_TARGETS['ips_min'], VALIDATION_TARGETS['ips_max']),
        (VALIDATION_TARGETS['cpi_min'], VALIDATION_TARGETS['cpi_max']),
        VALIDATION_TARGETS['expected_bottlenecks'],
        TIMING_CATEGORIES,
        [VALIDATION_TARGETS['source']],
        result.ips,
        result.cpi,
        result.bottleneck
    )
    return suite


def main():
    """Main entry point."""
    print(f"{{CONFIG['name']}} Performance Model")
    print("=" * 50)
    print(f"Clock: {{CONFIG['clock_mhz']}} MHz")
    print(f"Bus: {{CONFIG['bus_width']}}-bit")
    print(f"Transistors: {{CONFIG['transistors']:,}}")
    print()
    
    # Analyze with typical workload
    result = analyze('typical')
    print(f"IPS: {{result.ips:,.0f}}")
    print(f"CPI: {{result.cpi:.2f}}")
    print(f"Bottleneck: {{result.bottleneck}}")
    print()
    
    # Run validation
    suite = validate()
    results, all_passed = suite.run()
    print(suite.summary())


if __name__ == '__main__':
    main()
'''


def generate_model_json(proc_id: str, proc_data: dict) -> str:
    """Generate JSON configuration file."""
    config = {
        'name': proc_data['name'],
        'year': proc_data['year'],
        'clock_mhz': proc_data['clock_mhz'],
        'bus_width': proc_data['bus_width'],
        'transistors': proc_data['transistors'],
        'timing_categories': proc_data['categories'],
        'validation_targets': {
            'ips_range': [proc_data['ips_min'], proc_data['ips_max']],
            'cpi_range': [proc_data['cpi_min'], proc_data['cpi_max']],
            'expected_bottlenecks': proc_data['bottleneck']
        },
        'source': proc_data['source']
    }
    return json.dumps(config, indent=2)


def generate_readme(proc_id: str, proc_data: dict) -> str:
    """Generate README file."""
    timing_table = "| Category | Cycles | Weight | Description |\n"
    timing_table += "|----------|--------|--------|-------------|\n"
    for cat_name, cat_data in proc_data['categories'].items():
        timing_table += f"| {cat_name} | {cat_data['cycles']} | {cat_data['weight']:.2f} | {cat_data['desc']} |\n"

    return f"""# {proc_data['name']} Performance Model

Grey-box queueing model for the {proc_data['name']} microprocessor.

## Overview

| Specification | Value |
|--------------|-------|
| Year | {proc_data['year']} |
| Clock | {proc_data['clock_mhz']} MHz |
| Bus Width | {proc_data['bus_width']}-bit |
| Transistors | {proc_data['transistors']:,} |

## Timing Categories

{timing_table}

## Performance Targets

- **IPS Range**: {proc_data['ips_min']:,} - {proc_data['ips_max']:,}
- **CPI Range**: {proc_data['cpi_min']} - {proc_data['cpi_max']}
- **Primary Bottleneck**: {', '.join(proc_data['bottleneck'])}

## Usage

```python
from {proc_id}_model import analyze, validate

# Run analysis
result = analyze('typical')
print(f"IPS: {{result.ips:,.0f}}")
print(f"CPI: {{result.cpi:.2f}}")

# Validate model
val_result = validate()
print(val_result)
```

## Source

{proc_data['source']}
"""


def generate_all_models():
    """Generate all processor models."""
    base_dir = Path(__file__).parent
    
    for family, processors in PROCESSORS.items():
        family_dir = base_dir / family
        family_dir.mkdir(exist_ok=True)
        
        # Create family __init__.py
        init_content = f'"""{family.upper()} processor family models."""\n'
        (family_dir / '__init__.py').write_text(init_content)
        
        for proc_id, proc_data in processors.items():
            proc_dir = family_dir / proc_id
            proc_dir.mkdir(exist_ok=True)
            
            # Create __init__.py
            (proc_dir / '__init__.py').write_text(
                f'"""Model for {proc_data["name"]}."""\nfrom .{proc_id}_model import *\n'
            )
            
            # Generate model files
            model_py = generate_model_py(family, proc_id, proc_data)
            (proc_dir / f'{proc_id}_model.py').write_text(model_py)
            
            model_json = generate_model_json(proc_id, proc_data)
            (proc_dir / f'{proc_id}_model.json').write_text(model_json)
            
            readme = generate_readme(proc_id, proc_data)
            (proc_dir / 'README.md').write_text(readme)
            
            print(f"Generated: {family}/{proc_id}")
    
    print(f"\nGenerated {sum(len(p) for p in PROCESSORS.values())} processor models")


if __name__ == '__main__':
    generate_all_models()
