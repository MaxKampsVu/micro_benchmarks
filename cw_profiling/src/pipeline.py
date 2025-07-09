import firmware_generator_isw
import capture_traces_isw
import correlate_traces


def process(num_traces, num_samples, micro_benchmark_asm, micro_benchmark_name, target_dir):
    print(f"Executing benchmark: '{micro_benchmark_name}'")
    print("Modifying firmware...")
    firmware_generator_isw.create_firmware(micro_benchmark_asm)
    print("Capturing traces...")
    capture_traces_isw.capture(num_traces, num_samples)
    print("Correlating traces..")
    correlate_traces.correlate(micro_benchmark_name, target_dir)
