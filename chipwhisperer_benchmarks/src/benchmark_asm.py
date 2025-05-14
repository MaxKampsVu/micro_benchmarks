sram_overwrite_st = """
"nop"
"nop"
"nop"
"str %1, [%0]"
"nop"
"nop"
"nop"
: 
: "r" (&share0), "r" (share1)
:
"""

benchmarks = {"sram-overwrite-st": sram_overwrite_st}

