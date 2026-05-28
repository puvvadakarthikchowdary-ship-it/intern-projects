`timescale 1ns/1ps

module tb_pipeline;
    reg         clk = 0, rst = 1;
    reg  [31:0] instruction;
    wire [63:0] ipc_x100, total_instr, total_cycles, stall_cyc;

    integer i, wl;
    reg [31:0] prog [0:2][0:31];
    integer pc;

    pipeline_cpu dut (
        .clk(clk), .rst(rst),
        .instruction(instruction),
        .ipc_x100(ipc_x100),
        .total_instructions(total_instr),
        .total_cycles(total_cycles),
        .stall_cycles(stall_cyc)
    );

    always #5 clk = ~clk;

    initial begin
        $dumpfile("pipeline.vcd");
        $dumpvars(0, tb_pipeline);

        for (i=0; i<32; i=i+1)
            prog[0][i] = {3'b000, 5'd1, 5'd2, 5'd3, 14'b0};

        for (i=0; i<32; i=i+1) begin
            if (i%3 == 2)
                prog[1][i] = {3'b110, 29'b0};
            else
                prog[1][i] = {3'b000, 5'd1, 5'd2, 5'd3, 14'b0};
        end

        for (i=0; i<32; i=i+2) begin
            prog[2][i]   = {3'b001, 5'd1, 5'd2, 5'd4, 14'b0};
            prog[2][i+1] = {3'b000, 5'd4, 5'd2, 5'd5, 14'b0};
        end

        for (wl=0; wl<3; wl=wl+1) begin
            rst = 1; pc = 0;
            repeat(3) @(posedge clk);
            rst = 0;

            for (i=0; i<60; i=i+1) begin
                instruction = prog[wl][pc % 32];
                pc = pc + 1;
                @(posedge clk);
            end

            instruction = 32'b0;
            repeat(5) @(posedge clk);

            $display("WL%0d CYCLES=%0d INSTRS=%0d STALLS=%0d IPC_X100=%0d",
                     wl, total_cycles, total_instr, stall_cyc, ipc_x100);
        end

        $finish;
    end
endmodule
