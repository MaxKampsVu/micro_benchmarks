import re

code = f'''
"ldr %2, [%7]\n"
"ldr %0, [%4]\n"
"ldr %2, [%7]\n"
"nop\n"
"nop\n"
"nop\n"
"nop\n"
"nop\n"
"nop\n"
"nop\n"
"nop\n"
"str %0, [%4]\n"
"str %6, [%7]\n"
"eor %2, %6, %6\n"
"eor %2, %6, %6\n"
"eor %2, %6, %6\n"
"ldr %1, [%5]\n"

: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
'''

operands = '''
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD)
: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
:
'''

index_reg_map = {
    "%0": "r1",
    "%1": "r2",
    "%2": "r3",
    "%3": "r4",
    "%4": "share0_mem",
    "%5": "share1_mem",
    "%6": "r0",
    "%7": "zero_mem"
}


def replace_index_by_reg(match):
    key = match.group(0)
    return index_reg_map.get(key, key)  # fallback to original if not found


def clean(inline_asm):
    # Remove register specification
    inline_asm = inline_asm.replace(operands, "")
    inline_asm = inline_asm.replace('"', "")
    # Replace indices by their register names
    inline_asm = re.sub(r"%\d", replace_index_by_reg, inline_asm)
    # Remove empzy lines
    inline_asm = '\n'.join(filter(str.strip, inline_asm.splitlines()))
    return inline_asm


def init_state(inline_asm):
    # Add instruction to move 0 to register 0
    inline_asm = "mov r0, zero              // init register r0 with 0\n" + inline_asm
    # Load zero to zero memory
    inline_asm = "ldr r1, r0, #0            // init zero_mem with 0\n" + inline_asm
    # Add instruction to init state of simulation
    inline_asm = "is                        // init leakage effects state\n" + inline_asm
    # Reformat share0
    inline_asm = inline_asm.replace("[share0_mem]", "a0, #0           // access x0 in memory")
    # Reformat share1
    inline_asm = inline_asm.replace("[share1_mem]", "a0, #1           // access x1 in memory")
    # Reformat access to zero in memory
    inline_asm = inline_asm.replace("[zero_mem]", "zero_mem, #0")
    return inline_asm


def annotate_lines(inline_asm):
    lines = inline_asm.splitlines()
    prefixed_lines = [f"    {i * 4}: b5f0b5f0: {line}" for i, line in enumerate(lines)]
    inline_asm = "\n".join(prefixed_lines)
    return inline_asm


def inline_asm_to_scVerif(inline_asm):
    inline_asm = clean(inline_asm)
    inline_asm = init_state(inline_asm)
    inline_asm = annotate_lines(inline_asm)
    inline_asm = "00000000 <micro_benchmark>:\n" + inline_asm
    return inline_asm


print(inline_asm_to_scVerif(code))
