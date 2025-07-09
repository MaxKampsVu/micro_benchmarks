regA =       "%0"
regB =       "%1"
regC =       "%2"
regD =       "%3"
regE =       "%4"
regF =       "%5"
regG =       "%6"
share0_mem = "%7"
share1_mem = "%8"
zero =       "%9"
zero_mem =   "%10"

operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD), "+r" (regE), "+r" (regF), "+r" (regG)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
"""

### helper operations 

secure_load_share0_to_regA = f'''
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"'''


secure_load_share1_to_regG = f'''
"ldr {regC}, [{zero_mem}]\\n"
"ldr {regG}, [{share1_mem}]\\n"
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
"ldr {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_ld = f'''
{secure_load_share0_to_regA}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"ldr {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_ld_st = f'''
{secure_load_share1_to_regG}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"str {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_st = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
{clear_pipeline}
"str {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_ld_ld_zero_ld = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{operands}
'''

sram_remnant_st_ld_zero_st = f'''
{secure_load_share0_to_regA}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
"str {zero}, [{zero_mem}]\\n"
{clear_pipeline}
"ldr {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_ld_st_zero_ld = f'''
{secure_load_share1_to_regG}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"ldr {regC}, [{zero_mem}]\\n"
{clear_pipeline}
"str {regG}, [{share1_mem}]\\n"
{operands}
'''

sram_remnant_st_st_zero_st = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"str {regA}, [{share0_mem}]\\n"
"str {zero}, [{zero_mem}]\\n"
{clear_pipeline}
"str {regG}, [{share1_mem}]\\n"
{operands}
'''

### register overwrite effect 

reg_mov_overwrite = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"mov {regA}, {regG}\\n"
{operands}
'''

reg_ld_overwrite = f'''
{secure_load_share0_to_regA}
{nop_slide}
"ldr {regA}, [{share1_mem}]\\n"
{operands}
'''

reg_eor_overwrite = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"eor {regA}, {regG}, {zero}\\n"
{operands}
'''

reg_and_overwrite = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"and {regA}, {regG}, {zero}\\n"
{operands}
'''

reg_mov_overwrite_zero = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"mov {regA}, {regG}\\n"
{operands}
'''

reg_ld_overwrite_zero = f'''
{secure_load_share0_to_regA}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"ldr {regA}, [{share1_mem}]\\n"
{operands}
'''

reg_eor_overwrite_zero = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"eor {regA}, {regG}, {zero}\\n"
{operands}
'''

reg_and_overwrite_zero = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"and {regA}, {regG}, {zero}\\n"
{operands}
'''


### sram overwrite effect 

sram_overwrite = f'''
{secure_load_share0_to_regA}
{nop_slide}
"str {regA}, [{share1_mem}]\\n"
{operands}
'''

sram_overwrite_zero = f'''
{secure_load_share0_to_regA}
{nop_slide}
"str {zero}, [{share1_mem}]\\n"
"str {regA}, [{share1_mem}]\\n"
{operands}
'''

### pipeline register overwrite effect 

pipeline_eor_eor_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_and_and_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"and {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_and_eor_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {zero}, {regA}\\n"
"eor {regD}, {zero}, {regG}\\n"
{operands}
'''

pipeline_and_and_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {zero}, {regA}\\n"
"and {regD}, {zero}, {regG}\\n"
{operands}
'''

pipeline_and_eor_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {zero}, {regA}\\n"
"eor {regD}, {zero}, {regG}\\n"
{operands}
'''


pipeline_eor_eor_cross_op = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regD}, {zero}, {regG}\\n"
{operands}
'''

pipeline_and_and_cross_op = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {regG}, {zero}\\n"
"and {regD}, {zero}, {regG}\\n"
{operands}
'''

pipeline_and_eor_cross_op = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regD}, {zero}, {regG}\\n"
{operands}
'''

pipeline_ldr_eor_result = f'''
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regG}, {zero}, {zero}\\n"
{operands}
'''

pipeline_ldr_eor_opA = f'''
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regC}, {regG}, {zero}\\n"
{operands}
'''

pipeline_ldr_eor_opB = f'''
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regC}, {zero}, {regG}\\n"
{operands}
'''

pipeline_str_eor_result = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regG}, {zero}, {zero}\\n"
{operands}
'''

pipeline_str_eor_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regC}, {regG}, {zero}\\n"
{operands}
'''

pipeline_str_eor_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regC}, {zero}, {regG}\\n"
{operands}
'''

pipeline_mov_eor_result = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regC}, {regA}\\n"
"eor {regG}, {zero}, {zero}\\n"
{operands}
'''

pipeline_mov_eor_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regC}, {regA}\\n"
"eor {regC}, {regG}, {zero}\\n"
{operands}
'''

pipeline_mov_eor_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regC}, {zero}, {regG}\\n"
{operands}
'''

pipeline_mov_dest_eor_result = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regG}, {zero}, {zero}\\n"
{operands}
'''

pipeline_mov_dest_eor_opA = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regC}, {regG}, {zero}\\n"
{operands}
'''

pipeline_mov_dest_eor_opB = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regC}, {zero}, {regG}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth1 = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth2 = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"nop\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth3 = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_eor = f'''
{secure_load_share0_to_regA}
{secure_load_share1_to_regG}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regE}, {regE}, {regE}\\n"
"eor {regD}, {regG}, {zero}\\n"
{operands}
'''


sram_remnant_bencharks = {
    "sram-remnant-ld-ld": sram_remnant_ld_ld,
    "sram-remnant-st-ld": sram_remnant_st_ld,
    "sram-remnant-ld-st": sram_remnant_ld_st,
    "sram-remnant-st-st": sram_remnant_st_st,
    "sram-remnant-ld-ld-zero": sram_remnant_ld_ld_zero_ld,
    "sram-remnant-st-ld-zero": sram_remnant_st_ld_zero_st,
    "sram-remnant-ld-st-zero": sram_remnant_ld_st_zero_ld,
    "sram-remnant-st-st-zero": sram_remnant_st_st_zero_st,
}

register_overwrite_benchmarks = {
    "reg-mov-overwrite": reg_mov_overwrite,
    "reg-ld-overwrite": reg_ld_overwrite,
    "reg-eor-overwrite": reg_eor_overwrite,
    "reg-and-overwrite": reg_and_overwrite,
    "reg-mov-overwrite-zero": reg_mov_overwrite_zero,
    "reg-ld-overwrite-zero": reg_ld_overwrite_zero,
    "reg-eor-overwrite-zero": reg_eor_overwrite_zero,
    "reg-and-overwrite-zero": reg_and_overwrite_zero,
}

sram_overwrite_benchmarks = {
    "sram-overwrite": sram_overwrite, 
    "sram-overwrite-zero":sram_overwrite_zero
}

pipeline_benchmarks = {
              ### pipeline register overwrite 
              "pipeline-eor-eor-opA": pipeline_eor_eor_opA, 
              "pipeline-and-and-opA": pipeline_and_and_opA,
              "pipeline-and-eor-opA": pipeline_and_eor_opA,
              "pipeline-eor-eor-opB": pipeline_eor_eor_opB,
              "pipeline-and-and-opB": pipeline_and_and_opB,
              "pipeline-and-eor-opB": pipeline_and_eor_opB,
              "pipeline-eor-eor-cross-op": pipeline_eor_eor_cross_op,
              "pipeline-and-and-cross-op": pipeline_and_and_cross_op,
              "pipeline-and-eor-cross-op": pipeline_and_eor_cross_op,
              "pipeline-ldr-eor-result": pipeline_ldr_eor_result,
              "pipeline-ldr-eor-opA": pipeline_ldr_eor_opA,
              "pipeline-ldr-eor-opB": pipeline_ldr_eor_opB,
              "pipeline-str-eor-result": pipeline_str_eor_result,
              "pipeline-str-eor-opA": pipeline_str_eor_opA,
              "pipeline-str-eor-opB": pipeline_str_eor_opB,
              "pipeline-mov-eor-result": pipeline_mov_eor_result,
              "pipeline-mov-eor-opA": pipeline_mov_eor_opA,
              "pipeline-mov-eor-opB": pipeline_mov_eor_opB,
              "pipeline-mov-dest-eor-result": pipeline_mov_dest_eor_result,
              "pipeline-mov-dest-eor-opA": pipeline_mov_dest_eor_opA,
              "pipeline-mov-dest-eor-opB": pipeline_mov_dest_eor_opB,
              "pipeline-eor-eor-clear-nop-depth1": pipeline_eor_eor_clear_nop_depth1,
              "pipeline-eor-eor-clear-nop-depth2": pipeline_eor_eor_clear_nop_depth2,
              "pipeline-eor-eor-clear-nop-depth3": pipeline_eor_eor_clear_nop_depth3,
              "pipeline-eor-eor-clear-eor-depth1": pipeline_eor_eor_clear_eor
              }

benchmarks = { "sram-remnant-ld-ld": sram_remnant_ld_ld, "sram-remnant-ld-ld-zero": sram_remnant_ld_ld_zero_ld}#sram_remnant_bencharks | register_overwrite_benchmarks | sram_overwrite_benchmarks | pipeline_benchmarks