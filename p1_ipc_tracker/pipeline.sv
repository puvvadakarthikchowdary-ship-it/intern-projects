// 5-Stage Pipelined CPU — IPC Tracker
module pipeline_cpu (
    input  logic        clk,
    input  logic        rst,
    input  logic [31:0] instruction,
    output logic [63:0] ipc_x100,
    output logic [63:0] total_instructions,
    output logic [63:0] total_cycles,
    output logic [63:0] stall_cycles
);

logic [31:0] IF_ID_instr, ID_EX_instr, EX_MEM_instr, MEM_WB_instr;
logic        IF_ID_valid, ID_EX_valid, EX_MEM_valid, MEM_WB_valid;
logic stall;
logic branch_taken;
logic [4:0]  rs1, rs2, rd_ex, rd_mem;
logic [2:0]  opcode;

assign opcode = IF_ID_instr[31:29];
assign rs1    = IF_ID_instr[28:24];
assign rs2    = IF_ID_instr[23:19];
assign rd_ex  = ID_EX_instr[18:14];
assign rd_mem = EX_MEM_instr[18:14];

assign stall = (ID_EX_valid  && rd_ex  != 0 && (rd_ex  == rs1 || rd_ex  == rs2)) ||
               (EX_MEM_valid && rd_mem != 0 && (rd_mem == rs1 || rd_mem == rs2));

assign branch_taken = (ID_EX_valid && ID_EX_instr[31:29] == 3'b110);

always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
        IF_ID_instr  <= 32'b0; IF_ID_valid  <= 0;
        ID_EX_instr  <= 32'b0; ID_EX_valid  <= 0;
        EX_MEM_instr <= 32'b0; EX_MEM_valid <= 0;
        MEM_WB_instr <= 32'b0; MEM_WB_valid <= 0;
    end else begin
        if (!stall) begin
            IF_ID_instr <= (branch_taken) ? 32'b0 : instruction;
            IF_ID_valid <= !branch_taken;
        end
        ID_EX_instr  <= stall ? 32'b0 : IF_ID_instr;
        ID_EX_valid  <= stall ? 1'b0  : IF_ID_valid;
        EX_MEM_instr <= ID_EX_instr;
        EX_MEM_valid <= ID_EX_valid;
        MEM_WB_instr <= EX_MEM_instr;
        MEM_WB_valid <= EX_MEM_valid;
    end
end

always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
        total_cycles       <= 0;
        total_instructions <= 0;
        stall_cycles       <= 0;
        ipc_x100           <= 0;
    end else begin
        total_cycles <= total_cycles + 1;
        if (stall)
            stall_cycles <= stall_cycles + 1;
        if (MEM_WB_valid)
            total_instructions <= total_instructions + 1;
        if (total_cycles > 0)
            ipc_x100 <= (total_instructions * 100) / total_cycles;
    end
end

endmodule
