// Pipeline stage variables
w32 result0;
w32 OpA0;
w32 OpB0;
w32 result1;
w32 OpA1;
w32 OpB1;
w32 result2;
w32 OpA2;
w32 OpB2;

macro leak_pipeline(w32 resultNew, w32 OpANew, w32 OpBNew)
{
   // Shift pipeline stage variables
   OpA1 <- OpA0;
   OpB1 <- OpB0;
   result1 <- result0;
   OpA2 <- OpA1;
   OpB2 <- OpB1;
   result2 <- result1;
   // Insert new values into first stage of pipeline
   OpA0 <- OpANew;
   OpB0 <- OpBNew;
   result0 <- resultNew;

   // Leak stages 0, 1
   leak pip (OpA0 ^w32 OpA1);
   leak pip (OpB0 ^w32 OpB1);
   leak pip (result0 ^w32 result1);
}

macro is0_leak()
{
}

macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{
   leak_pipeline(rs1 ^w32 rs2, rs1, rs2);
   
   leak resultTransition(rd, rs1 ^w32 rs2);
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
   
   leak_pipeline(rs1 &w32 rs2, rs1, rs2);
   leak resultTransition(rd, rs1 &w32 rs2);
}

macro nop0_leak()
{

}

macro mov2_leak(w32 dst, w32 adr)
{
   leak_pipeline(dst, adr, (w32) 0);
   
}

macro lw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- [w32 mem (int) (adr +w32 ofs)];
   val <- [w32 mem (int) (adr +w32 ofs)];
   leak_pipeline(val, adr, ofs);

   
   leak loadTransition(dst, val);
}

macro sw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- dst;
   val <- [w32 mem (int) (adr +w32 ofs)];
   leak_pipeline(dst, adr, ofs);
   
   
   leak storeTransition(dst, val);
}

