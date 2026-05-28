

## Project 1 — RTL IPC Tracker

### What is this?
A 5-stage pipelined CPU implemented in SystemVerilog. Three different workloads are tested to measure IPC (Instructions Per Cycle) and analyze the impact of pipeline hazards.

### Pipeline Stages
| Stage | Full Name | Function |
|---|---|---|
| IF | Instruction Fetch | Fetches instruction from memory |
| ID | Instruction Decode | Decodes instruction and reads registers |
| EX | Execute | Performs ALU computation |
| MEM | Memory Access | Reads or writes RAM |
| WB | Write Back | Saves result back to register file |

### IPC Results
| Workload | IPC | Stall Cycles | Root Cause |
|---|---|---|---|
| ALU-Heavy | 0.93 | 0 | No hazards — near ideal throughput |
| Branch-Heavy | 0.65 | 0 | Branch flush wastes 2 cycles per branch |
| Memory-Heavy | 0.46 | 30 | RAW hazards cause pipeline stalls |

### Key Insight
IPC dropped 51% from ALU-heavy to Memory-heavy workload.
Root cause: RAW (Read After Write) data hazards — a LOAD result is needed
by the very next instruction before it is ready in the pipeline.

### Fix
- Add a Forwarding Unit to bypass EX/MEM results directly → IPC recovers to ~0.80
- Add a 2-bit Branch Predictor to reduce flush penalty → IPC recovers to ~0.85

### How to Run
cd p1_ipc_tracker && python3 analyze_ipc.py

---

## Skills Demonstrated
VLSI · RTL Design · ASIC · SystemVerilog · EDA · Verilog · IPC Analysis ·
Functional Verification · Constrained-Random Testing · Isolation Forest ·
CPU Microarchitecture · Performance Analysis · Python · Yosys
