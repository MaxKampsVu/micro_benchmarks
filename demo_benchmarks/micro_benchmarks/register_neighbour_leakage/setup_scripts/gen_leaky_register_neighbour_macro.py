import argparse

LEAKY_MATRIX_FILE = "micro_benchmarks/register_neighbour_leakage/setup_scripts/leaky_register_matrix.txt"
LEAKY_ISA_FILE = "micro_benchmarks/register_neighbour_leakage/leakyisa-ibex-pres-rv32i.il"

macro = """
macro mov2_leak(w32 dst, w32 adr)
    int val
{   
    leak_neighbours(dst);
    
    leak overwrite (dst ^w32 adr);
}
"""

def truncate_leaky_isa():
    """Removes everything from 'macro leak_neighbours (w32 adr)' to the end of the file."""
    try:
        with open(LEAKY_ISA_FILE, 'r') as file:
            lines = file.readlines()

        with open(LEAKY_ISA_FILE, 'w') as file:
            for line in lines:
                if line.strip().startswith("macro leak_neighbours (w32 adr)"):
                    break
                file.write(line)
    except FileNotFoundError:
        pass

def process_file(filename):
    truncate_leaky_isa()
    
    with open(filename, 'r') as infile, open(LEAKY_ISA_FILE, 'a') as outfile:
        outfile.write("macro leak_neighbours (w32 adr)\n")
        outfile.write("{\n")
        for line in infile:
            line = line.strip()
            if not line or ':' not in line:
                continue  # skip empty lines or malformed ones
            reg, neighbours = line.split(':', 1)
            reg = reg.strip()
            neighbours_list = neighbours.strip().split()

            outfile.write(f'    if (adr =name= {reg})\n')
            outfile.write("    {\n")
            for neighbour in neighbours_list:
                outfile.write(f'        leak {reg}Neighbour (adr ^w32 {neighbour});\n')
            outfile.write("    }\n")
        outfile.write("}\n")

        outfile.write(macro)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create leak macro for register matrix.")
    parser.add_argument("filename", nargs='?', help="Path to the input text file")
    args = parser.parse_args()
    
    process_file(args.filename)
