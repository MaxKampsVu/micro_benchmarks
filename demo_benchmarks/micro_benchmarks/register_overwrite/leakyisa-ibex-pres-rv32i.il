w32 opA;
w32 opB;


macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{   
    leak resultTransition(rd, rs1 ^w32 rs2);
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
    leak resultTransition(rd, rs1 &w32 rs2);
}

macro sw3_leak(w32 val, w32 adr, w32 ofs)
{
    // we assume stores do not leak
}

macro lw3_leak(w32 dst, w32 adr, w32 ofs)
    w32 val
{
    leak loadTransition(dst, val);
}

macro mov2_leak(w32 dst, w32 adr)
{
    leak overwrite(dst ^w32 adr);
}
