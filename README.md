---

## Project 2 — EDA Synthesis Flow

### What is this?
A 32-bit ALU written in Verilog is synthesized using Yosys (open-source equivalent of Synopsys Design Compiler). Gate count, logic depth, and netlist metrics are automatically extracted using Python.

### Tools Used
| Tool | Purpose |
|---|---|
| Verilog | RTL design of 32-bit ALU |
| Yosys | Open-source synthesis tool |
| Python | Metric extraction and reporting |
| Graphviz | Netlist visualization |

### ALU Operations
| Opcode | Operation |
|---|---|
| 000 | ADD |
| 001 | SUB |
| 010 | AND |
| 011 | OR |
| 100 | XOR |
| 101 | SHL (Shift Left) |
| 110 | SHR (Shift Right) |
| 111 | NOT |

### Synthesis Results
| Metric | Value |
|---|---|
| Total Gates | 1352 |
| Logic Depth | 8 levels |
| Port Count | 7 |
| Top Gate Type | $_ANDNOT_ (421 gates) |

### Gate Breakdown
| Gate Type | Count |
|---|---|
| $_ANDNOT_ | 421 |
| $_OR_ | 339 |
| $_MUX_ | 291 |
| $_NOR_ | 80 |
| $_XOR_ | 55 |
| $_NAND_ | 48 |

### Key Insight
The 32-bit ALU synthesized to 1352 gates with 8 logic levels deep critical path.
ANDNOT gates dominate because Yosys optimizes subtraction and comparison logic into AND-NOT combinations for area efficiency.

### How to Run
cd p2_eda_synthesis && python3 parse_metrics.py
