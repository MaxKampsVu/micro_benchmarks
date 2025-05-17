target0 = "%0"
target1 = "%1"
target2 = "%2"
target3 = "%3"
share0_mem = "%4"
share1_mem = "%5"
zero = "%6"
zero_mem = "%7"
random_mem = "%8"

sram_overwrite_ld_ld_one_share = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_ld_ld = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {target1}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_ld_st = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {target1}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_st_ld = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {target1}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_st_st = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"nop\\n"
"ldr {target1}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_ld_ld_zero = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"ldr {target1}, [{zero_mem}]\\n"
"nop\\n"
"ldr {target2}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
:
'''

sram_overwrite_ld_random = f'''
"nop\\n"
"nop\\n"
"ldr {target0}, [{share0_mem}]\\n"
"nop\\n"
"ldr {target1}, [{random_mem}]\\n"
"nop\\n"
"ldr {target2}, [{share1_mem}]\\n"
"nop\\n"
: "r=" (target0), "r=" (target1), "r=" (target2), "r=" (target3)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero), "r" (&random)
: "memory"
'''

B_NUM_SAMPLES = 1000
B_NUM_TRACES = 5000

benchmarks = {"sram-overwrite-ld-ld-one-share": sram_overwrite_ld_ld_one_share,
              "sram-overwrite-ld-ld": sram_overwrite_ld_ld,
              "sram-overwrite-ld-ld-zero": sram_overwrite_ld_ld_zero}
