regA =       "%0"
regB =       "%1"
regC =       "%2"
regD =       "%3"
share0_mem = "%4"
share1_mem = "%5"
zero =       "%6"
zero_mem =   "%7"

B_NUM_SAMPLES = 1000
B_NUM_TRACES = 5000

operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
"""

### helper operations 

secure_load_share0 = f'''
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"'''


secure_load_share1 = f'''
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regB}, [{share1_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"'''

nop_slide = f'''"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"nop\\n"'''

clear_pipeline = f'''"eor {regC}, {zero}, {zero}\\n"
"eor {regC}, {zero}, {zero}\\n"
"eor {regC}, {zero}, {zero}\\n"'''


### sram remnant effect 

sanity_check = f'''
{nop_slide}
{operands}
'''

sram_remnant_ld_ld = f'''
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"ldr {regB}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_ld = f'''
{secure_load_share0}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"ldr {regB}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_ld_st = f'''
{secure_load_share1}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"str {regB}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_st = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"str {regB}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_ld_ld_zero_ld = f'''
{secure_load_share0}
{secure_load_share1}
{operands}
'''

sram_remnant_st_ld_zero_st = f'''
{secure_load_share0}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
"str {zero}, [{zero_mem}]\\n"
{clear_pipeline}
"ldr {regB}, [{share1_mem}]\\n"
{operands}
'''

print(sram_remnant_st_ld_zero_st)

sram_remnant_ld_st_zero_ld = f'''
{secure_load_share1}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
{clear_pipeline}
"str {regB}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_st_zero_st = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
"str {zero}, [{zero_mem}]\\n"
{clear_pipeline}
"str {regB}, [{share1_mem}]\\n"
{operands}
'''

### register overwrite effect 

reg_mov_overwrite = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"mov {regA}, {regB}\\n"
{operands}
'''

reg_ld_overwrite = f'''
{secure_load_share0}
{nop_slide}
"ldr {regA}, [{share1_mem}]\\n"
{operands}
'''


reg_mov_overwrite_zero = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"mov {regA}, {regB}\\n"
{operands}
'''

reg_ld_overwrite_zero = f'''
{secure_load_share0}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"ldr {regA}, [{share1_mem}]\\n"
{operands}
'''


### sram overwrite effect 

sram_overwrite = f'''
{secure_load_share0}
{nop_slide}
"str {regA}, [{share1_mem}]\\n"
{operands}
'''

sram_overwrite_zero = f'''
{secure_load_share0}
{nop_slide}
"str {zero}, [{share1_mem}]\\n"
"str {regA}, [{share1_mem}]\\n"
{operands}
'''

### pipeline register overwrite effect 

benchmarks = {#"nop-slide-sanity-check": nop_slide,
              ### sram remnant effect 
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
