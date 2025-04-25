import argparse
import os
from instructions import write_leaky_isa

LEAKY_ISA_PATH = "leakyisa-ibex-pres-rv32i.il"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create leak macro for register matrix.")

    parser.add_argument(
        "ilfile",              
        type=str,                
        default=None,          
        help="Path to the input .il file"
    )

    parser.add_argument(
        "objdump",              
        type=str,                
        default=None,          
        help="Path to micro benchmark"
    )


    parser.add_argument(
        "-oR", 
        action="store_true", 
        help="Flag to enable the register overwrite effect (default: False)"
    )

    parser.add_argument(
        "-oS", 
        action="store_true", 
        help="Flag to enable the sram overwrite effect (default: False)"
    )

    parser.add_argument(
        "-r", 
        action="store_true", 
        help="Flag to enable the sram remnant effect (default: False)"
    )

    args = parser.parse_args()

    # Create the leaky isa model based on flahs 
    write_leaky_isa(args.oR, args.oS, args.r, LEAKY_ISA_PATH)

    with open(args.ilfile, 'r') as file:
        lines = file.readlines()

    if len(lines) >= 3:
        # Replace the third line using a pattern match
        if 'include asm' in lines[2]:
            lines[2] = f'include asm "{args.objdump}"\n'

    with open(args.ilfile, 'w') as file:
        file.writelines(lines)

    # Execute the il file with scVerif and the leaky isa model
    os.system(f"scverif --il {args.ilfile}")    

