w32 remnantVal_ld_ld;
w32 lastInstructionId_ld_ld;

// Leak remnant for sequence: ld_ld
macro leak_remnant_ld_ld(w32 newVal, w32 currentInstructionId)
{
   if (lastInstructionId_ld_ld == (w32) 1) 
   {
      if (currentInstructionId == (w32) 1) 
      {
         leak remnant (newVal ^w32 remnantVal_ld_ld);
      }
   }
   if (currentInstructionId == (w32) -1) 
   {
      lastInstructionId_ld_ld <- currentInstructionId;
      remnantVal_ld_ld <- newVal;
   }
   if (currentInstructionId == (w32) 1) 
   {
      lastInstructionId_ld_ld <- currentInstructionId;
      remnantVal_ld_ld <- newVal;
   }
}
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
   if (currentInstructionId == (w32) 0) 
   {
      lastInstructionId_st_st <- currentInstructionId;
      remnantVal_st_st <- newVal;
   }
   if (currentInstructionId == (w32) -1) 
   {
      lastInstructionId_st_st <- currentInstructionId;
      remnantVal_st_st <- newVal;
   }
}
w32 remnantVal_st_ld;
w32 lastInstructionId_st_ld;

// Leak remnant for sequence: st_ld
macro leak_remnant_st_ld(w32 newVal, w32 currentInstructionId)
{
   if (lastInstructionId_st_ld == (w32) 0) 
   {
      if (currentInstructionId == (w32) 1) 
      {
         leak remnant (newVal ^w32 remnantVal_st_ld);
      }
   }
   if (currentInstructionId == (w32) 0) 
   {
      lastInstructionId_st_ld <- currentInstructionId;
      remnantVal_st_ld <- newVal;
   }
   if (currentInstructionId == (w32) 1) 
   {
      lastInstructionId_st_ld <- currentInstructionId;
      remnantVal_st_ld <- newVal;
   }
}
w32 remnantVal_ld_st;
w32 lastInstructionId_ld_st;

// Leak remnant for sequence: ld_st
macro leak_remnant_ld_st(w32 newVal, w32 currentInstructionId)
{
   if (lastInstructionId_ld_st == (w32) 1) 
   {
      if (currentInstructionId == (w32) 0) 
      {
         leak remnant (newVal ^w32 remnantVal_ld_st);
      }
   }
   if (currentInstructionId == (w32) 0) 
   {
      lastInstructionId_ld_st <- currentInstructionId;
      remnantVal_ld_st <- newVal;
   }
   if (currentInstructionId == (w32) -1) 
   {
      lastInstructionId_ld_st <- currentInstructionId;
      remnantVal_ld_st <- newVal;
   }
}

// Pipeline stage variables
w32 dst0;
w32 OpA0;
w32 OpB0;
w32 dst1;
w32 OpA1;
w32 OpB1;

macro leak_pipeline(w32 dstNew, w32 OpANew, w32 OpBNew)
{
   // Shift pipeline stage variables
   OpA1 <- OpA0;
   OpB1 <- OpB0;
   dst1 <- dst0;
   // Insert new values into first stage of pipeline
   OpA0 <- OpANew;
   OpB0 <- OpBNew;
   dst0 <- dstNew;

   // Leak stages 0, 1
   leak pip (OpA0 ^w32 OpA1);
   leak pip (OpB0 ^w32 OpB1);
   leak pip (dst0 ^w32 dst1);

   // Leak stages 0, 1 cross op op
   leak pip (OpA0 ^w32 OpB1);
   leak pip (OpB0 ^w32 OpA1);

   // Leak stages 0, 1 cross op target
   leak pip (dst0 ^w32 OpB1);
   leak pip (dst0 ^w32 OpA1);
   leak pip (dst1 ^w32 OpB0);
   leak pip (dst1 ^w32 OpA0);
}

macro is0_leak()
{
   lastInstructionId_ld_ld <- (w32) 0;
   lastInstructionId_st_st <- (w32) 0;
   lastInstructionId_st_ld <- (w32) 0;
   lastInstructionId_ld_st <- (w32) 0;
}

macro xor3_leak(w32 rd, w32 rs1, w32 rs2)
{
   leak_pipeline(rd, rs1, rs2);
   
}

macro and3_leak(w32 rd, w32 rs1, w32 rs2)
{
   
   leak_pipeline(rd, rs1, rs2);
}

macro nop0_leak()
{

}

macro mov2_leak(w32 dst, w32 adr)
{
   leak_pipeline(dst, adr, (w32) 0);
   
}

macro ld3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- [w32 mem (int) (adr +w32 ofs)];
   val <- [w32 mem (int) (adr +w32 ofs)];
   leak_pipeline(dst, adr, ofs);
   leak_remnant_ld_ld(remnantVal, (w32) 1);
   leak_remnant_st_st(remnantVal, (w32) 1);
   leak_remnant_st_ld(remnantVal, (w32) 1);
   leak_remnant_ld_st(remnantVal, (w32) 1);

   
}

macro st3_leak(w32 dst, w32 adr, w32 ofs)
   w32 remnantVal,
   w32 val
{
   remnantVal <- dst;
   val <- [w32 mem (int) (adr +w32 ofs)];
   leak_pipeline(dst, adr, ofs);
      leak_remnant_ld_ld(remnantVal, (w32) 0);
   leak_remnant_st_st(remnantVal, (w32) 0);
   leak_remnant_st_ld(remnantVal, (w32) 0);
   leak_remnant_ld_st(remnantVal, (w32) 0);

   
}

