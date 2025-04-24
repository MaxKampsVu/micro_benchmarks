// registers

w32 zero;
w32 ra;
w32 sp;
w32 gp;
w32 tp;
w32 t0;
w32 t1;
w32 t2;
w32 s0;
w32 s1;
w32 a0;
w32 a1;
w32 a2;
w32 a3;
w32 a4;
w32 a5;
w32 a6;
w32 a7;
w32 s2;
w32 s3;
w32 s4;
w32 s5;
w32 s6;
w32 s7;
w32 s8;
w32 s9;
w32 s10;
w32 s11;
w32 t3;
w32 t4;
w32 t5;
w32 t6;

mem [];

/**** Instructions ****/
macro xor3 (w32 rd, w32 rs1, w32 rs2)
{
    rd <- rs1 ^w32 rs2;
}

macro and3 (w32 rd, w32 rs1, w32 rs2)
{
    rd <- rs1 &w32 rs2;
}

macro nop()
{

}

macro sw3 (w32 val, w32 adr, w32 ofs)
{
    [w32 mem (int) (adr +w32 ofs)] <- val;
}

macro lw3 (w32 dst, w32 adr, w32 ofs)
{
    dst <- [w32 mem (int) (adr +w32 ofs)];
}

macro mov2 (w32 dst, w32 adr)
{
    dst <- adr;
}

macro not1 (w32 adr)
{
    adr <- adr ^w32 (w32) 4294967295; // adr xor FFFFFFFF
}


