regA =       "%0"
regB =       "%1"
regC =       "%2"
regD =       "%3"
regE =       "%4"
regF =       "%5"
regG =       "%6"
regH =       "%7"
share0_mem = "%8"
share1_mem = "%9"
zero =       "%10"
zero_mem =   "%11"

B_NUM_SAMPLES = 1000
B_NUM_TRACES = 5000

### sram remnant effect 

nop_slide = f'''
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_ld_ld = f'''
"nop\\n"
"nop\\n"
"ldr {regA}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {regB}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_st_ld = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"           
"nop\\n"
"nop\\n"
"str {regA}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_ld_st = f'''
"ldr {regA}, [{share1_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"nop\\n"
"nop\\n"
"ldr {regC}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"str {regA}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_st_st = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"ldr {regC}, [{share1_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"nop\\n"
"str {regA}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"str {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_ld_ld_zero_ld = f'''
"nop\\n"
"nop\\n"
"ldr {regA}, [{share0_mem}]\\n"
"nop\\n"
"ldr {regB}, [{zero_mem}]\\n"
"nop\\n"
"ldr {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_st_ld_zero_st = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"           
"nop\\n"
"nop\\n"
"str {regA}, [{share0_mem}]\\n"
"nop\\n"
"str {zero}, [{zero_mem}]\\n"
"nop\\n"
"ldr {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_ld_st_zero_ld = f'''
"ldr {regA}, [{share1_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"nop\\n"
"nop\\n"
"ldr {regC}, [{share0_mem}]\\n"
"nop\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"nop\\n"
"str {regA}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_remnant_st_st_zero_st = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"ldr {regC}, [{share1_mem}]\\n"
"ldr {regB}, [{zero_mem}]\\n"   
"nop\\n"
"str {regA}, [{share0_mem}]\\n"
"nop\\n"
"str {zero}, [{zero_mem}]\\n"
"nop\\n"
"str {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

### register overwrite effect 

reg_mov_overwrite = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regB}, [{share1_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"mov {regA}, {regB}\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

reg_ld_overwrite = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {regA}, [{share1_mem}]\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

reg_mov_overwrite_zero = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regB}, [{share1_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"mov {regA}, {zero}\\n"
"mov {regA}, {regB}\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

reg_ld_overwrite_zero = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"mov {regA}, {zero}\\n"
"ldr {regA}, [{share1_mem}]\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

### sram overwrite effect 

sram_overwrite = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"str {regA}, [{share1_mem}]\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

sram_overwrite_zero = f'''
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
"nop\\n"
"nop\\n"
"str {zero}, [{share1_mem}]\\n"
"str {regA}, [{share1_mem}]\\n"
"nop\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD), "r=" (regE), "r=" (regF), "r=" (regG), "r=" (regH)
: "r" (&share1), "r" (&share2), "r" (zero), "r" (&zero)
:
'''

### pipeline register overwrite effect 

benchmarks = {### sram remnant effect 
              "sram-remnant-ld-ld": sram_remnant_ld_ld,
              "sram-remnant-st-ld": sram_remnant_st_ld,
              "sram-remnant-ld-st": sram_remnant_ld_st,
              "sram-remnant-st-st": sram_remnant_st_st,
              "sram-remnant-ld-ld-zero": sram_remnant_ld_ld_zero_ld,
              "sram-remnant-st-ld-zero": sram_remnant_st_ld_zero_st,
              "sram-remnant-ld-st-zero": sram_remnant_ld_st_zero_ld,
              "sram-remnant-st-st-zero": sram_remnant_st_st_zero_st,
              ### register overwrite effect 
              "reg-mov-overwrite": reg_mov_overwrite, 
              "reg-ld-overwrite": reg_ld_overwrite, 
              "reg-mov-overwrite-zero": reg_mov_overwrite_zero, 
              "reg-ld-overwrite-zero": reg_ld_overwrite_zero, 
              ### sram overwrite effect 
              "sram-overwrite": sram_overwrite, 
              "sram-overwrite-zero":sram_overwrite_zero
              ### pipeline register overwrite 
              }
