w32 opA;
w32 opB;
w32 prevResult;
int lastinstruction;
int currentinstruction;

macro pipeline_operands_leak(w32 rs1rs2result, w32 rs1, w32 rs2)
{
    if (lastinstruction == 1) { // only leak if a xor is followed by an and 
        if (currentinstruction == 2) {
            leak XorAndOpA (rs1 ^w32 opA);
            leak XorAndrOpB (rs2 ^w32 opB);
            leak XorAndResult (rs2 ^w32 opB);
        }
    }
    if (currentinstruction == 2) {
        // leak nothing 
    }

    opA <- rs1;
    opB <- rs2;
    prevResult <- rs1rs2result;
    lastinstruction <- currentinstruction;
}

macro nop0_leak()
{
    currentinstruction <- 0;
    lastinstruction <- 1;
    pipeline_operands_leak((w32) 0, (w32) 0, (w32) 0);
}

macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{   
    currentinstruction <- 1;
    pipeline_operands_leak(rs1 ^w32 rs2, rs1, rs2);
    leak resultTransition(rd, rs1 ^w32 rs2);
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
    currentinstruction <- 2;
    pipeline_operands_leak(rs1 &w32 rs2, rs1, rs2);
    leak resultTransition(rd, rs1 &w32 rs2);
}

macro sw3_leak(w32 val, w32 adr, w32 ofs)
{
    // we assume stores do not leak
}

macro lw3_leak(w32 dst, w32 adr, w32 ofs)
    w32 val
{
    val <- [w32 mem (int) (adr +w32 ofs)];
    leak loadTransition(dst, val);
}
