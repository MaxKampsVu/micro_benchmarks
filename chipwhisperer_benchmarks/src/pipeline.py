import firmware_generator
import capture_traces
import correlate_traces


def process(num_traces, num_samples, micro_benchmark_asm, micro_benchmark_name, target_dir):
    firmware_generator.create_firmware(micro_benchmark_asm)
    capture_traces.capture(num_traces, num_samples)
    correlate_traces.correlate(micro_benchmark_name, target_dir)
