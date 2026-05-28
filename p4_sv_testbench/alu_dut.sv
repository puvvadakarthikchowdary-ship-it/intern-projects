module alu_dut #(parameter W = 8) (
    input  logic [W-1:0] a, b,
    input  logic [2:0]   opcode,
    output logic [W-1:0] result,
    output logic         zero, carry, negative
);

logic [W:0] ext;

always_comb begin
    carry = 0;
    unique case (opcode)
        3'b000: begin ext = {1'b0,a} + {1'b0,b}; result = ext[W-1:0]; carry = ext[W]; end
        3'b001: begin ext = {1'b0,a} - {1'b0,b}; result = ext[W-1:0]; carry = ext[W]; end
        3'b010: result = a & b;
        3'b011: result = a | b;
        3'b100: result = a ^ b;
        3'b101: result = a << b[2:0];
        3'b110: result = a >> b[2:0];
        3'b111: result = ~a;
        default: result = '0;
    endcase
    zero     = (result == '0);
    negative = result[W-1];
end

endmodule
