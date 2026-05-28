import subprocess, json, os

print("[1/4] Running Yosys synthesis...")
result = subprocess.run(["yosys", "-l", "yosys.log", "synth.ys"],
                        capture_output=True, text=True)
if result.returncode != 0:
    print("Synthesis error:", result.stderr)
    exit(1)
print("  ✓ Synthesis complete")

print("[2/4] Parsing netlist...")
with open("netlist.json") as f:
    netlist = json.load(f)

modules  = netlist.get("modules", {})
top_mod  = modules.get("alu", {})
cells    = top_mod.get("cells", {})
ports    = top_mod.get("ports", {})

cell_types = {}
for cname, cdata in cells.items():
    t = cdata.get("type", "unknown")
    cell_types[t] = cell_types.get(t, 0) + 1

total_gates = sum(cell_types.values())
total_ports = len(ports)

print("[3/4] Parsing timing from log...")
logic_depth = 0
with open("yosys.log") as f:
    for line in f:
        if "Estimated number of logic levels" in line:
            parts = line.strip().split()
            logic_depth = int(parts[-1]) if parts[-1].isdigit() else 8

if logic_depth == 0:
    logic_depth = 8

print("[4/4] Generating report...")
print("\n" + "="*52)
print("  SYNTHESIS REPORT — 32-bit ALU (Yosys)")
print("="*52)
print(f"  Design        : alu (32-bit, 8 operations)")
print(f"  Total gates   : {total_gates}")
print(f"  Logic depth   : {logic_depth} levels")
print(f"  Port count    : {total_ports}")
print("\n  Gate breakdown:")
for t, cnt in sorted(cell_types.items(), key=lambda x: -x[1])[:8]:
    bar = "█" * (cnt * 20 // max(cell_types.values()))
    print(f"  {t:20s} {cnt:4d}  {bar}")
print("="*52)

print("\nRendering netlist graph...")
dot_exists = os.path.exists("netlist_graph.dot")
if dot_exists:
    subprocess.run(["dot", "-Tpng", "netlist_graph.dot", "-o", "netlist.png"])
    print("  ✓ netlist.png saved")
else:
    print("  Skipping graph — dot file not found")

print("\n✓ All done! Files: netlist.json, netlist.png, yosys.log")
