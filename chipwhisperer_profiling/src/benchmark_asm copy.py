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

B_NUM_SAMPLES = 500
B_NUM_TRACES = 5000

operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD), "+r" (regE), "+r" (regF), "+r" (regG)
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

reg_xor_overwrite = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"eor {regA}, {regB}, {zero}\\n"
{operands}
'''

reg_and_overwrite = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"and {regA}, {regB}, {zero}\\n"
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

reg_xor_overwrite_zero = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"eor {regA}, {regB}, {zero}\\n"
{operands}
'''

reg_and_overwrite_zero = f'''
{secure_load_share0}
{secure_load_share1}
{nop_slide}
"eor {regA}, {zero}, {zero}\\n"
"and {regA}, {regB}, {zero}\\n"
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

pipeline_eor_eor_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_and_and_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"and {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_and_xor_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {zero}, {regA}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {zero}, {regB}\\n"
{operands}
'''

pipeline_and_and_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {zero}, {regA}\\n"
"eor {regE}, {regF}, {regG}\\n"
"and {regD}, {zero}, {regB}\\n"
{operands}
'''

pipeline_and_xor_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {zero}, {regA}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {zero}, {regB}\\n"
{operands}
'''


pipeline_eor_eor_cross_op = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {zero}, {regB}\\n"
{operands}
'''

pipeline_and_and_cross_op = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"and {regD}, {zero}, {regB}\\n"
{operands}
'''

pipeline_and_xor_cross_op = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"and {regC}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regD}, {zero}, {regB}\\n"
{operands}
'''

pipeline_ldr_eor_result = f'''
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regB}, {zero}, {zero}\\n"
{operands}
'''

pipeline_ldr_eor_opA = f'''
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {regB}, {zero}\\n"
{operands}
'''

pipeline_ldr_eor_opB = f'''
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"ldr {regA}, [{share0_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {zero}, {regB}\\n"
{operands}
'''

pipeline_str_eor_result = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regB}, {zero}, {zero}\\n"
{operands}
'''

pipeline_str_eor_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {regB}, {zero}\\n"
{operands}
'''

pipeline_str_eor_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"str {regA}, [{zero_mem}]\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {zero}, {regB}\\n"
{operands}
'''

pipeline_mov_eor_result = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regC}, {regA}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regB}, {zero}, {zero}\\n"
{operands}
'''

pipeline_mov_eor_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regC}, {regA}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {regB}, {zero}\\n"
{operands}
'''

pipeline_mov_eor_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {zero}, {regB}\\n"
{operands}
'''

pipeline_mov_dest_eor_result = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regB}, {zero}, {zero}\\n"
{operands}
'''

pipeline_mov_dest_eor_opA = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {regB}, {zero}\\n"
{operands}
'''

pipeline_mov_dest_eor_opB = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"mov {regA}, {regC}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regC}, {zero}, {regB}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth1 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth2 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"nop\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_nop_depth3 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"nop\\n"
"nop\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_xor_depth1 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_xor_depth2 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regC}, {regA}, {zero}\\n"
"nop\\n"
"eor {regD}, {regB}, {zero}\\n"
{operands}
'''

pipeline_eor_eor_clear_xor_depth3 = f'''
{secure_load_share0}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regA}, {regA}, {zero}\\n"
"eor {regE}, {regF}, {regG}\\n"
"eor {regB}, {regB}, {zero}\\n"
{operands}
'''


sram_remnant_bencharks = {
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
    "reg-xor-overwrite": reg_xor_overwrite,
    "reg-and-overwrite": reg_and_overwrite,
    "reg-mov-overwrite-zero": reg_mov_overwrite_zero,
    "reg-ld-overwrite-zero": reg_ld_overwrite_zero,
    "reg-xor-overwrite-zero": reg_xor_overwrite_zero,
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
              "pipeline-and-xor-opA": pipeline_and_xor_opA,
              "pipeline-eor-eor-opB": pipeline_eor_eor_opB,
              "pipeline-and-and-opB": pipeline_and_and_opB,
              "pipeline-and-xor-opB": pipeline_and_xor_opB,
              "pipeline-eor-eor-cross-op": pipeline_eor_eor_cross_op,
              "pipeline-and-and-cross-op": pipeline_and_and_cross_op,
              "pipeline-and-xor-cross-op": pipeline_and_xor_cross_op,
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
              #"pipeline-eor-eor-clear-nop-depth1": pipeline_eor_eor_clear_nop_depth1,
              #"pipeline-eor-eor-clear-nop-depth2": pipeline_eor_eor_clear_nop_depth2,
              #"pipeline-eor-eor-clear-nop-depth3": pipeline_eor_eor_clear_nop_depth3,
              #"pipeline-eor-eor-clear-xor-depth1": pipeline_eor_eor_clear_xor_depth1,
              #"pipeline-eor-eor-clear-xor-depth2": pipeline_eor_eor_clear_xor_depth2,
              #"pipeline-eor-eor-clear-xor-depth3": pipeline_eor_eor_clear_xor_depth3
              }

benchmarks = pipeline_benchmarks
