import argparse

LEAKY_REMNANT_FILE = "micro_benchmarks/sram_remnant/setup_scripts/sram_remnant_registers.txt"
LEAKY_ISA_FILE = "micro_benchmarks/sram_remnant/leakyisa-ibex-pres-rv32i.il"

mov2_leak_macro = """
macro lw3_leak(w32 dst, w32 adr, w32 ofs)
    w32 val
{
    val <- [w32 mem (int) (adr +w32 ofs)];
    leak_remnant(adr, val);
    leak loadTransition(dst, val);
}
"""

def truncate_leaky_isa():
    """Truncate the file from 'macro leak_remnant(w32 adr, w32 val)' to the end."""
    try:
        with open(LEAKY_ISA_FILE, 'r') as file:
            lines = file.readlines()

        with open(LEAKY_ISA_FILE, 'w') as file:
            for line in lines:
                if line.strip().startswith("macro leak_remnant(w32 adr, w32 val)"):
                    break
                file.write(line)
    except FileNotFoundError:
        pass

def process_file(filename):
    truncate_leaky_isa()

    with open(filename, 'r') as infile:
        registers = [line.strip() for line in infile if line.strip()]

    # Append register remnant declarations to the beginning of the file
    with open(LEAKY_ISA_FILE, 'a') as outfile:
        for reg in registers:
            outfile.write(f'w32 {reg}RemnantVal;\n')

        outfile.write("\nmacro leak_remnant(w32 adr, w32 val)\n")
        outfile.write("{\n")
        for reg in registers:
            outfile.write(f'    if (adr =name= {reg})\n')
            outfile.write("    {\n")
            outfile.write(f'        leak {reg}Remnant (val ^w32 {reg}RemnantVal);\n')
            outfile.write(f'        {reg}RemnantVal <- val;\n')
            outfile.write("    }\n")
        outfile.write("}\n\n")

        outfile.write(mov2_leak_macro)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create leak macro for sram remnant effect.")
    parser.add_argument("filename", nargs='?', default=LEAKY_REMNANT_FILE, help="Path to the input text file")
    args = parser.parse_args()

    process_file(args.filename)
