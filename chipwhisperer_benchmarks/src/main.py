import os
from datetime import datetime
import shutil
from benchmark_asm import benchmarks, B_NUM_SAMPLES, B_NUM_TRACES
import pipeline
BENCHMARK_PLOT_DIR = "benchmark_plots"
BENCHMARK_FILE = "benchmark_asm.py"
NUM_SAMPLES = 0
NUM_TRACES = 0


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    dir_path = f"{BENCHMARK_PLOT_DIR}/benchmark_{timestamp}"
    os.makedirs(dir_path, exist_ok=True)
    print(f"Directory created: {dir_path}")

    shutil.copy(BENCHMARK_FILE, dir_path)
    print(f"Copied '{BENCHMARK_FILE}' to directory '{dir_path}'")

    NUM_SAMPLES = B_NUM_SAMPLES
    NUM_TRACES = B_NUM_TRACES
    for i, (name, asm) in enumerate(benchmarks.items()):
        print(f"Executing benchmark: {i+1}/{len(benchmarks)}")
        try:
            pipeline.process(NUM_TRACES, NUM_SAMPLES, asm, name, dir_path)
            print(f"Benchmark '{name}' was successful!")
        except Exception as e:
            print(f"Benchmark '{name}' failed!")

