import argparse
import importlib.util
import os

import inline_asm_to_scVerif
import scVerif_to_inline_asm

def asm_to_scverif(asm_benchmarks):
    inline_asm_to_scVerif.convert(asm_benchmarks)

def load_py_module(py_file_path):
    """Dynamically load a Python file as a module."""
    module_name = os.path.splitext(os.path.basename(py_file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, py_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optional ASM and objdump processor.")
    parser.add_argument("-asm_file", type=str, help="Optional path to the .py file with ASM objects")
    parser.add_argument("-objdump_file", type=str, help="Optional path to the .objdump file")
    args = parser.parse_args()

    # If asm_file is provided, load and process it
    if args.asm_file:
        if not args.asm_file.endswith(".py"):
            raise ValueError("asm_file must be a .py file")

        asm_module = load_py_module(args.asm_file)
        asm_benchmarks = getattr(asm_module, 'benchmarks', None)
        if asm_benchmarks is None:
            raise AttributeError("benchmarks object not found in the ASM file")

        asm_to_scverif(asm_benchmarks)

    # If objdump_file is provided, use or process it
    if args.objdump_file:
        if not args.objdump_file.endswith(".objdump"):
            raise ValueError("objdump_file must be a .objdump file")
        
        with open(args.objdump_file, "r") as f:
            scVerif_to_inline_asm.convert(f.read())

