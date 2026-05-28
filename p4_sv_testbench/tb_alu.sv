`timescale 1ns/1ps

module tb_alu;

parameter W = 8;
parameter NUM_TESTS = 2000;

logic [W-1:0] a, b, result;
logic [2:0]   opcode;
logic         zero, carry, negative;

alu_dut #(.W(W)) dut (.*);

integer pass_count = 0, fail_count = 0;
integer op_count[0:7];
logic [W-1:0] exp_result;
integer i;

function automatic [W-1:0] golden_result(
    input [W-1:0] ia, ib,
    input [2:0]   op
);
    case (op)
        3'b000: return ia + ib;
        3'b001: return ia - ib;
        3'b010: return ia & ib;
        3'b011: return ia | ib;
        3'b100: return ia ^ ib;
        3'b101: return ia << ib[2:0];
        3'b110: return ia >> ib[2:0];
        3'b111: return ~ia;
        default: return 0;
    endcase
endfunction

task automatic check(input string test_name,
                     input [W-1:0] ia, ib, input [2:0] op);
    exp_result = golden_result(ia, ib, op);
    if (result === exp_result) begin
        pass_count++;
    end else begin
        fail_count++;
        if (fail_count <= 5)
            $display("FAIL [%s] op=%b a=%h b=%h got=%h exp=%h",
                     test_name, op, ia, ib, result, exp_result);
    end
endtask

initial begin
    for (i=0; i<8; i++) op_count[i] = 0;

    $display("=== Phase 1: Directed tests ===");
    a=0;      b=0;      opcode=3'b000; #1; check("ADD 0+0", a, b, opcode);
    a=8'hFF;  b=8'hFF;  opcode=3'b000; #1; check("ADD overflow", a, b, opcode);
    a=8'hFF;  b=8'hFF;  opcode=3'b001; #1; check("SUB same", a, b, opcode);
    a=8'hAA;  b=8'h55;  opcode=3'b010; #1; check("AND alternating", a, b, opcode);
    a=0;      b=0;      opcode=3'b100; #1; check("XOR 0^0", a, b, opcode);

    $display("=== Phase 2: Random tests (%0d) ===", NUM_TESTS);
    repeat (NUM_TESTS) begin
        opcode = $urandom_range(0, 7);
        a = ($urandom % 10 == 0) ? 8'($urandom % 2 == 0 ? 8'hFF : 8'h00)
                                 : 8'($urandom_range(0, 255));
        b = 8'($urandom_range(0, 255));
        #1;
        check("", a, b, opcode);
        op_count[opcode]++;
    end

    $display("\n========== VERIFICATION REPORT ==========");
    $display("  Tests run  : %0d", pass_count + fail_count);
    $display("  PASSED     : %0d", pass_count);
    $display("  FAILED     : %0d", fail_count);
    $display("  Pass rate  : %0.1f%%", (pass_count*100.0)/(pass_count+fail_count));
    $display("  Op coverage: ADD=%0d SUB=%0d AND=%0d OR=%0d XOR=%0d SHL=%0d SHR=%0d NOT=%0d",
             op_count[0], op_count[1], op_count[2], op_count[3],
             op_count[4], op_count[5], op_count[6], op_count[7]);
    $display("==========================================");
    $finish;
end

endmodule
