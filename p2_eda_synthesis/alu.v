// 32-bit ALU — synthesizable Verilog
module alu #(
    parameter WIDTH = 32
) (
    input  [WIDTH-1:0] a,
    input  [WIDTH-1:0] b,
    input  [2:0]       opcode,
    output reg [WIDTH-1:0] result,
    output reg         zero,
    output reg         carry,
    output reg         negative
);

localparam ADD = 3'b000;
localparam SUB = 3'b001;
localparam AND = 3'b010;
localparam OR  = 3'b011;
localparam XOR = 3'b100;
localparam SHL = 3'b101;
localparam SHR = 3'b110;
localparam NOT = 3'b111;

reg [WIDTH:0] extended;

always @(*) begin
    carry = 0;
    case (opcode)
        ADD: begin
            extended = {1'b0, a} + {1'b0, b};
            result   = extended[WIDTH-1:0];
            carry    = extended[WIDTH];
        end
        SUB: begin
            extended = {1'b0, a} - {1'b0, b};
            result   = extended[WIDTH-1:0];
            carry    = extended[WIDTH];
        end
        AND:    result = a & b;
        OR:     result = a | b;
        XOR:    result = a ^ b;
        SHL:    result = a << b[4:0];
        SHR:    result = a >> b[4:0];
        NOT:    result = ~a;
        default: result = {WIDTH{1'b0}};
    endcase
    zero     = (result == {WIDTH{1'b0}});
    negative = result[WIDTH-1];
end

endmodule
