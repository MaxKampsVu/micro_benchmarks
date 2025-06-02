import argparse
import importlib.util
import os
from datetime import datetime
import shutil
import pipeline
BENCHMARK_PLOT_DIR = "../benchmark_plots"
NUM_SAMPLES = 500
NUM_TRACES = 2000

def load_py_module(py_file_path):
    """Dynamically load a Python file as a module."""
    module_name = os.path.splitext(os.path.basename(py_file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, py_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inline assembly parser.")
    parser.add_argument("-asm_file", type=str, help="Optional path to the .py file with inline asm")
    args = parser.parse_args()

    if args.asm_file:
        if not args.asm_file.endswith(".py"):
            raise ValueError("asm_file must be a .py file")

        asm_module = load_py_module(args.asm_file)
        asm_benchmarks = getattr(asm_module, 'benchmarks', None)
        if asm_benchmarks is None:
            raise AttributeError("benchmarks object not found in the ASM file")


    device_name = "STMF32F303" 

    banner = f"""
 ▗▄▄▖▗▖ ▗▖    ▗▖  ▗▖▗▄▄▄▖ ▗▄▄▖▗▄▄▖  ▗▄▖     ▗▄▄▖ ▗▄▄▖  ▗▄▖ ▗▄▄▄▖▗▄▄▄▖▗▖   ▗▄▄▄▖▗▄▄▖ 
▐▌   ▐▌ ▐▌    ▐▛▚▞▜▌  █  ▐▌   ▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌     █  ▐▌   ▐▌   ▐▌ ▐▌
▐▌   ▐▌ ▐▌    ▐▌  ▐▌  █  ▐▌   ▐▛▀▚▖▐▌ ▐▌    ▐▛▀▘ ▐▛▀▚▖▐▌ ▐▌▐▛▀▀▘  █  ▐▌   ▐▛▀▀▘▐▛▀▚▖
▝▚▄▄▖▐▙█▟▌    ▐▌  ▐▌▗▄█▄▖▝▚▄▄▖▐▌ ▐▌▝▚▄▞▘    ▐▌   ▐▌ ▐▌▝▚▄▞▘▐▌   ▗▄█▄▖▐▙▄▄▖▐▙▄▄▖▐▌ ▐▌                                                                                                 
"""
    print(banner)  

    print(f"Starting microbenchmark profiling for device: {device_name}")                             
                                                     

    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    dir_path = f"{BENCHMARK_PLOT_DIR}/{device_name}_{timestamp}"
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created: {dir_path}")

    shutil.copy(args.asm_file, dir_path)
    print(f"Copied '{args.asm_file}' to directory '{dir_path}'")

    benchmarks_failed = 0
    for i, (name, asm) in enumerate(asm_benchmarks.items()):
        print(f"Executing benchmark: {i+1}/{len(asm_benchmarks)}")
        try:
            pipeline.process(NUM_TRACES, NUM_SAMPLES, asm, name, dir_path)
            print(f"Benchmark '{name}' was successful!")
        except Exception as e:
            benchmarks_failed += 1
            print(e)
            print(f"Benchmark '{name}' failed!")

    print(f"{benchmarks_failed} benchmarks failed")

