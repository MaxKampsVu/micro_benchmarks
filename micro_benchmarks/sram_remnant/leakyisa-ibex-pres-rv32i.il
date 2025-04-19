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

w32 t0RemnantVal;
w32 t1RemnantVal;
w32 t2RemnantVal;

macro leak_remnant(w32 adr, w32 val)
{
    if (adr =name= t0)
    {
        leak t0Remnant (val ^w32 t0RemnantVal);
        t0RemnantVal <- val;
    }
    if (adr =name= t1)
    {
        leak t1Remnant (val ^w32 t1RemnantVal);
        t1RemnantVal <- val;
    }
    if (adr =name= t2)
    {
        leak t2Remnant (val ^w32 t2RemnantVal);
        t2RemnantVal <- val;
    }
}


macro lw3_leak(w32 dst, w32 adr, w32 ofs)
    w32 val
{
    val <- [w32 mem (int) (adr +w32 ofs)];
    leak_remnant(adr, val);
    leak loadTransition(dst, val);
}
