import re

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

registers = [regC, regD, regE, regF, regG]

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

def reg_name(op): 
    match = re.search(r"\d+", op)
    return f"r{int(match.group())+1}"

def make_benchmark(op1, op2): 
    return f'''
{secure_load_share0}
{clear_pipeline}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
{nop_slide}
"eor {op1}, {regB}, {zero}\\n"
{operands}
'''

benchmarks = {}


"""
for i in range(0, len(registers)):
    op1 = registers[i]
    op2 = "0"
    new_benchmark = make_benchmark(op1, op2)
    benchmarks = benchmarks | {f"{reg_name(op1)}-{reg_name(op2)}": new_benchmark}
"""


one = f'''
{secure_load_share0}
{clear_pipeline}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
{nop_slide}
"eor {regD}, {regA}, {zero}\\n"
"mov {regA}, {zero}\\n"
{clear_pipeline}
"eor {regE}, {regB}, {zero}\\n"
{operands}
'''

two =  f'''
{secure_load_share0}
{clear_pipeline}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regA}, {regA}, {zero}\\n"
{clear_pipeline}
"eor {regB}, {regG}, {zero}\\n"
{operands}
'''

three =  f'''
{secure_load_share0}
{clear_pipeline}
{secure_load_share1}
{clear_pipeline}
{nop_slide}
"eor {regA}, {regA}, {zero}\\n"
{clear_pipeline}
"eor {regG}, {regG}, {zero}\\n"
{operands}
'''

benchmarks = {"two": three, "three": three}