sram_overwrite_st = '''
"nop\\n"
"nop\\n"
"nop\\n"
"str %1, [%0]\\n"
"nop\\n"
"nop\\n"
"nop\\n"
: 
: "r" (&share0), "r" (share1)
:
'''

B_NUM_SAMPLES = 500
B_NUM_TRACES = 500

benchmarks = {"sram-overwrite-st": sram_overwrite_st}

