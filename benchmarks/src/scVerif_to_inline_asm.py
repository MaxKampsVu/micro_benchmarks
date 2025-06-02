import re 
operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD), "+r" (regE), "+r" (regF), "+r" (regG)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
"""

reg_index_map = {
    "r1": "%0",
    "r2": "%1",
    "r3": "%2",
    "r4": "%3",
    "r5": "%4",
    "r6": "%5",
    "r7": "%6",
    "share0_mem": "%7",
    "share1_mem": "%8",
    "r0": "%9",
    "zero_mem": "%10"
}

def replace_reg_by_index(match):
    key = match.group(0)
    return reg_index_map.get(key, key) 

def clean(inline_asm):
    # Remove prefix
    inline_asm = re.sub(r'^\s*\d+:\s*[0-9a-fA-F]{8}\s*', '', inline_asm, flags=re.MULTILINE)

    inline_asm = inline_asm.replace("00000000 <micro_benchmark>:\n", "")
    inline_asm = inline_asm.replace("ld  zero, a2, #4\n", "")
    inline_asm = inline_asm.replace("ld  zero, a2, #0\n", "")
    inline_asm = inline_asm.replace("is\n", "")
    

    return inline_asm

def init_state(inline_asm):
    # Add instruction to move 0 to register 0
    inline_asm = "ld  zero, a2, #4\n" + inline_asm
    # Load zero to zero memory
    inline_asm = "ld  zero, a2, #0\n" + inline_asm
    # Add instruction to init state of simulation
    inline_asm = "is\n" + inline_asm
    return inline_asm

def rename_operands(inline_asm):
    # Reformat share0
    inline_asm = inline_asm.replace("a0, #0", "[share0_mem]")
    # Reformat share1
    inline_asm = inline_asm.replace("a0, #4", "[share1_mem]")
    # Reformat access to zero in memory
    inline_asm = inline_asm.replace("a1, #0", "[zero_mem]")

    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, reg_index_map.keys())) + r')\b')
    inline_asm = pattern.sub(replace_reg_by_index, inline_asm)

    inline_asm = inline_asm.replace("ld", "ldr")
    inline_asm = inline_asm.replace("st", "str")
    inline_asm = inline_asm.replace("xor", "eor")
    return inline_asm;

def qoute_lines(inline_asm):
    lines = inline_asm.splitlines()
    quoted_lines = ['"' + line + '"' for line in lines]

    return "\n".join(quoted_lines)


def convert(objdump):
    # clear BENCHMARKS_DIR
    print("scVerif -> inline_asm:")

    inline_asm = clean(objdump)
    inline_asm = rename_operands(inline_asm)
    inline_asm = qoute_lines(inline_asm)
    inline_asm = inline_asm + "\n" + operands

    print(inline_asm)