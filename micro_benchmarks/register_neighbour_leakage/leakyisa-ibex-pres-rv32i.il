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

// Micro benchmark instruction 


macro leak_neighbours (w32 adr)
{
    if (adr =name= t0)
    {
        leak t0Neighbour (adr ^w32 t1);
        leak t0Neighbour (adr ^w32 t4);
    }
    if (adr =name= t1)
    {
        leak t1Neighbour (adr ^w32 t0);
        leak t1Neighbour (adr ^w32 t6);
    }
}

macro mov2_leak(w32 dst, w32 adr)
    int val
{   
    leak_neighbours(dst);
    
    leak overwrite (dst ^w32 adr);
}
