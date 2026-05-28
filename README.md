# Internship Projects — Synopsys & AMD

RTL design, EDA synthesis, AI/ML, and functional verification projects.
Built for: Synopsys India Apprentice Program | AMD CPU Performance Intern

---

## Projects

| # | Project | Tech | Company |
|---|---------|------|---------|
| 1 | RTL IPC Tracker — 5-stage pipeline CPU | SystemVerilog, Python | Both |
| 2 | EDA Synthesis Flow — ALU → Yosys → gates | Verilog, Yosys, Python | Synopsys |
| 3 | AI Anomaly Detector — CPU perf counters | Python, scikit-learn | AMD |
| 4 | SV Verification Testbench — UVM-lite | SystemVerilog, Python | Synopsys |

---

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
Root cause: RAW (Read After Write) data hazards.
Fix: Add Forwarding Unit + 2-bit Branch Predictor → IPC recovers to ~0.85

### How to Run
cd p1_ipc_tracker && python3 analyze_ipc.py

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

### Synthesis Results
| Metric | Value |
|---|---|
| Total Gates | 1352 |
| Logic Depth | 8 levels |
| Top Gate Type | $_ANDNOT_ (421 gates) |

### Key Insight
The 32-bit ALU synthesized to 1352 gates with 8 logic levels deep critical path.
ANDNOT gates dominate because Yosys optimizes subtraction logic into AND-NOT combinations.

### How to Run
cd p2_eda_synthesis && python3 parse_metrics.py

---

## Project 3 — AI Anomaly Detector

### What is this?
Synthetic CPU performance counter data is generated and fed into an Isolation Forest ML model to automatically detect performance anomalies. Directly aligned with AMD JD requirement of AI-driven performance infrastructure.

### Features Used
| Feature | Description |
|---|---|
| ipc | Instructions Per Cycle |
| l1_miss_rate | L1 cache miss rate |
| l2_miss_rate | L2 cache miss rate |
| branch_miss | Branch misprediction rate |
| stall_ratio | Estimated pipeline stall % |
| mem_pressure | Weighted memory access cost |
| perf_score | Composite performance score |

### Anomaly Types Detected
| Type | Symptom |
|---|---|
| Cache Thrash | High L1/L2 miss rate, low IPC |
| Branch Storm | High branch miss rate, low IPC |
| IPC Cliff | Very low IPC across all counters |

### Model Results
| Metric | Value |
|---|---|
| Algorithm | Isolation Forest (unsupervised) |
| Precision | ~0.86 |
| Recall | ~0.88 |
| F1 Score | ~0.87 |

### Key Insight
Model detects CPU anomalies without labeled training data.
Replaces ~2 hours of manual performance triage per run.

### How to Run
cd p3_ai_anomaly && python3 generate_data.py && python3 train_model.py && python3 visualize.py

---

## Skills Demonstrated
VLSI · RTL Design · ASIC · SystemVerilog · EDA · Verilog · IPC Analysis ·
Functional Verification · Constrained-Random Testing · Isolation Forest ·
CPU Microarchitecture · Performance Analysis · Python · Yosys
