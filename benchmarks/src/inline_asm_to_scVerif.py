import re
import shutil, os;

BENCHMARKS_DIR = "../scVerif_benchmarks"

operands = """
: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD)
: "r" (&sharea0_mem), "r" (&sharea1_mem), "r" (&shareb0_mem), "r" (&shareb1_mem), "r" (&mem0), "r" (&mem1), "r" (&r01_mem), "r" (&r10_mem), "r" (zero), "r" (&zero)
:
"""

index_reg_map = {
    "%0": "r1",
    "%1": "r2",
    "%2": "r3",
    "%3": "r5",
    "%4": "sharea0_mem",
    "%5": "sharea1_mem",
    "%6": "shareb0_mem",
    "%7": "shareb1_mem",
    "%8": "mem0",
    "%9": "mem1",
    "%10": "r01_mem",
    "%11": "r10_mem",
    "%12": "zero",
    "%13": "zero_mem",
    "%14": "zero_mem"
}

def replace_index_by_reg(match):
    key = match.group(0)
    return index_reg_map.get(key, key)  # fallback to original if not found


def clean(inline_asm):
    # Remove register specification
    inline_asm = inline_asm.replace(operands, "")
    inline_asm = inline_asm.replace('"', "")
    # Replace indices by their register names
    inline_asm = re.sub(r"%\d+", replace_index_by_reg, inline_asm)
    # Remove empty lines
    inline_asm = '\n'.join(filter(str.strip, inline_asm.splitlines()))

    inline_asm = inline_asm.replace("\\n", "")
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
    inline_asm = inline_asm.replace("[sharea0_mem]", "a0, #0")
    # Reformat share1
    inline_asm = inline_asm.replace("[sharea1_mem]", "a0, #4")
    # Reformat share0
    inline_asm = inline_asm.replace("[shareb0_mem]", "a1, #0")
    # Reformat share1
    inline_asm = inline_asm.replace("[shareb1_mem]", "a1, #4")
    # Reformat access to zero in memory
    inline_asm = inline_asm.replace("[zero_mem]", "a2, #0")

    inline_asm = inline_asm.replace("[mem0]", "a3, #0")
    inline_asm = inline_asm.replace("[mem1]", "a3, #4")
    inline_asm = inline_asm.replace("[r01_mem]", "a4, #0")
    inline_asm = inline_asm.replace("[r10_mem]", "a5, #4")

    inline_asm = inline_asm.replace("ldr", "ld")
    inline_asm = inline_asm.replace("str", "st")
    inline_asm = inline_asm.replace("eor", "xor")
    return inline_asm;

def annotate_lines(inline_asm):
    lines = inline_asm.splitlines()
    prefixed_lines = [f"    {i * 4}: b5f0b5f0 {line}" for i, line in enumerate(lines)]
    inline_asm = "\n".join(prefixed_lines)
    return inline_asm


def convert(asm_benchmarks):
    # clear BENCHMARKS_DIR
    for item in os.listdir(BENCHMARKS_DIR):
        item_path = os.path.join(BENCHMARKS_DIR, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  
        except Exception as e:
            print(f"Failed to delete {item_path}: {e}")


    print("inline_asm -> scVerif:")
    for (name, asm) in asm_benchmarks.items():
        print(f"    - {name}")
        objdump = clean(asm)
        objdump = init_state(objdump)
        objdump = rename_operands(objdump)
        objdump = annotate_lines(objdump)
        objdump = "00000000 <micro_benchmark>:\n" + objdump
        
        with open(f"{BENCHMARKS_DIR}/{name}.objdump", 'w') as f:
                f.write(objdump)