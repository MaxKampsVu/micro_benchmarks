regA =       "%0"
regB =       "%1"
regC =       "%2"
regD =       "%3"
share0 =     "%4"
share1 =     "%5"
share0_mem = "%6"
share1_mem = "%7"
zero =       "%8"
zero_mem =   "%9"

B_NUM_SAMPLES = 1000
B_NUM_TRACES = 500

sram_overwrite_ld_ld = f'''
"nop\\n"
"nop\\n"
"ldr {regA}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {regB}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD)
: "r" (share0), "r" (share1), "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
'''

sram_overwrite_ld_ld_zero_ld = f'''
"nop\\n"
"nop\\n"
"ldr {regA}, [{share0_mem}]\\n"
"nop\\n"
"ldr {regB}, [{zero_mem}]\\n"
"nop\\n"
"ldr {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD)
: "r" (share0), "r" (share1), "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
'''

sram_overwrite_ld_ld_zero_st = f'''
"nop\\n"
"nop\\n"
"ldr {regA}, [{share0_mem}]\\n"
"nop\\n"
"str {zero}, [{zero_mem}]\\n"
"nop\\n"
"ldr {regC}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (regA), "r=" (regB), "r=" (regC), "r=" (regD)
: "r" (share0), "r" (share1), "r" (&share0), "r" (&share1)‚, "r" (zero), "r" (&zero)
:
'''

benchmarks = {"sram-overwrite-ld": sram_overwrite_ld_ld,
              "sram-overwrite-ld-zero": sram_overwrite_ld_ld_zero_ld,
              "sram-overwrite-st-zero": sram_overwrite_ld_ld_zero_st}
