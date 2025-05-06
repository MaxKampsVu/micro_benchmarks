w32 result0;
w32 OpA0;
w32 OpB0;
w32 result1;
w32 OpA1;
w32 OpB1;

macro leak_pipeline(w32 OpANew, w32 OpBNew, w32 resultNew)
{
   OpA0 <- OpA1;
   OpB0 <- OpB1;
   result0 <- result1;
   OpA1 <- OpANew;
   OpB1 <- OpBNew;
   result1 <- resultNew;
   leak pip (OpA0 ^w32 OpA1);
   leak pip (OpB0 ^w32 OpB1);
   leak pip (OpA0 ^w32 OpB1);
   leak pip (OpB0 ^w32 OpA1);
   leak pip (result0 ^w32 result1);
}

macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{
   leak_pipeline(rs1, rs2, rs1 ^w32 rs2);
   leak resultTransition(rd, rs1 ^w32 rs2);
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
   leak_pipeline(rs1, rs2, rs1 &w32 rs2);
   leak resultTransition(rd, rs1 &w32 rs2);
}

macro nop0_leak()
{

}

macro mov2_leak(w32 dst, w32 adr)
{
   
}

macro lw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 val
{
  val <- [w32 mem (int) (adr +w32 ofs)];
   
   
   leak loadTransition(dst, val);
}

macro sw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 val
{
  val <- [w32 mem (int) (adr +w32 ofs)];   
   
   leak storeTransition(dst, val);
}

