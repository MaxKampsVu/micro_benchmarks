import re 
operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD)
: "r" (&sharea0_mem), "r" (&sharea1_mem), "r" (&shareb0_mem), "r" (&shareb1_mem), "r" (&mem0), "r" (&mem1), "r" (&r01_mem), "r" (&r10_mem), "r" (zero), "r" (&zero)
:
"""

reg_index_map = {
  "r1": "%0",
  "r2": "%1",
  "r3": "%2",
  "r5": "%3",
  "sharea0_mem": "%4",
  "sharea1_mem": "%5",
  "shareb0_mem": "%6",
  "shareb1_mem": "%7",
  "mem0": "%8",
  "mem1": "%9",
  "r01_mem": "%10",
  "r10_mem": "%11",
  "zero": "%12",
  "zero_mem": "%13"
}
   
def replace_reg_by_index(match):
    key = match.group(0)
    return reg_index_map.get(key, key) 

def clean(inline_asm):
    # Remove prefix
    inline_asm = re.sub(r'^\s*\d+:\s*[0-9a-fA-F]{8}\s*', '', inline_asm, flags=re.MULTILINE)

    inline_asm = inline_asm.replace("00000000 <micro_benchmark>:\n", "")
    inline_asm = inline_asm.replace("ld  zero, a2, #4", "")
    inline_asm = inline_asm.replace("ld  zero, a2, #0", "")
    inline_asm = inline_asm.replace("is", "")
    

    return inline_asm

def init_state(inline_asm):
    # Add instruction to move 0 to register 0
    inline_asm = "ld  zero, a2, #4" + inline_asm
    # Load zero to zero memory
    inline_asm = "ld  zero, a2, #0" + inline_asm
    # Add instruction to init state of simulation
    inline_asm = "is\n" + inline_asm
    return inline_asm

def rename_operands(inline_asm):
    # Reformat a
    inline_asm = inline_asm.replace("a0, #0", "[sharea0_mem]")
    inline_asm = inline_asm.replace("a0, #4", "[sharea1_mem]")
    # Reformat b
    inline_asm = inline_asm.replace("a1, #0", "[shareb0_mem]")
    inline_asm = inline_asm.replace("a1, #4", "[shareb1_mem]")
    # Reformat access to zero in memory
    inline_asm = inline_asm.replace("a2, #0", "[zero_mem]")

    inline_asm = inline_asm.replace("a3, #0", "[mem0]")
    inline_asm = inline_asm.replace("a3, #4", "[mem1]")
    inline_asm = inline_asm.replace("a4, #0", "[r01_mem]")
    inline_asm = inline_asm.replace("a4, #4", "[r10_mem]")

    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, reg_index_map.keys())) + r')\b')
    inline_asm = pattern.sub(replace_reg_by_index, inline_asm)

    inline_asm = inline_asm.replace("ld", "ldr")
    inline_asm = inline_asm.replace("st", "str")
    inline_asm = inline_asm.replace("xor", "eor")
    return inline_asm;

def qoute_lines(inline_asm):
    lines = inline_asm.splitlines()
    quoted_lines = []

    for line in lines:
        if '//' in line:
            code, comment = line.split('//', 1)
            code = code.rstrip()
            quoted_line = f'"{code}\\\\n"  // {comment.strip()}'
        else:
            quoted_line = f'"{line.rstrip()}\\\\n"'
        quoted_lines.append(quoted_line)

    return "\n".join(quoted_lines)


def convert(objdump):
    # clear BENCHMARKS_DIR
    print("scVerif -> inline_asm:")

    inline_asm = clean(objdump)
    inline_asm = rename_operands(inline_asm)
    inline_asm = qoute_lines(inline_asm)
    inline_asm = inline_asm + "\n" + operands

    print(inline_asm)