w32 remnantVal_st_st;
w32 lastInstructionId_st_st;

// Leak remnant for sequence: st_st
macro leak_remnant_st_st(w32 newVal, w32 currentInstructionId)
{
   if (lastInstructionId_st_st == (w32) 0) 
   {
      if (currentInstructionId == (w32) 0) 
      {
         leak remnant (newVal ^w32 remnantVal_st_st);
      }
   }
   lastInstructionId_st_st <- currentInstructionId;
   remnantVal_st_st <- newVal;
}

macro is0_leak()
{
   lastInstructionId_st_st <- (w32) 0;
}

macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{
   
   
   leak resultTransition(rd, rs1 ^w32 rs2);
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
   
   
   leak resultTransition(rd, rs1 &w32 rs2);
}

macro nop0_leak()
{
   
}

macro mov2_leak(w32 dst, w32 adr)
{
   
   
}

macro lw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- [w32 mem (int) (adr +w32 ofs)];
   val <- [w32 mem (int) (adr +w32 ofs)];
   
   leak_remnant_st_st(remnantVal, (w32) 1);

   
   leak loadTransition(dst, val);
}

macro sw3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- dst;
   val <- [w32 mem (int) (adr +w32 ofs)];
   
      leak_remnant_st_st(remnantVal, (w32) 0);

   
   leak storeTransition(dst, val);
}

