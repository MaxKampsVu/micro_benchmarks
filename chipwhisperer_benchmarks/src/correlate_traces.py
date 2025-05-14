import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

HammingWeightFn = lambda x: bin(x).count('1')

traces = np.load('trace_files/traces.npy')
textins = np.load('trace_files/textins.npy')

num_traces = np.shape(traces)[0]
num_samples = np.shape(traces)[1]


def calculate_hypothetical_power():
    print("Calculating hypothetical power...")
    hypothetical_power = np.zeros(num_traces)
    for trace_index in range(0, num_traces):
        x = int.from_bytes(textins[trace_index][0:4], 'big')
        y = int.from_bytes(textins[trace_index][4:8], 'big')
        hypothetical_power[trace_index] = HammingWeightFn((x ^ y))
    return hypothetical_power


def calculate_power():
    print("Calculating mean power for samples...")
    power = np.zeros(num_samples)
    for sample in range(0, num_samples):
        T_j_list = np.zeros(num_traces + 1)
        for trace_index in range(0, num_traces):
            T_j_list[trace_index] = traces[trace_index][sample]
        power[sample] = np.mean(T_j_list, dtype=np.float64)
    return power


def calculate_correlation():
    H_list = calculate_hypothetical_power()
    H_mean = np.mean(H_list, dtype=np.float64)

    mean_samples = calculate_power()

    correlations = np.zeros(num_samples)

    for sample in trange(num_samples, desc="Computing correlation for each sample"):
        sum_q = 0
        for trace_index in range(0, num_traces):
            sum_q += (H_list[trace_index] - H_mean) * (traces[trace_index][sample] - mean_samples[sample])

        sum_d1 = 0
        sum_d2 = 0
        for trace_index in range(0, num_traces):
            sum_d1 += np.power((H_list[trace_index] - H_mean), 2)
            sum_d2 += np.power(traces[trace_index][sample] - mean_samples[sample], 2)
        sqrt_d = np.sqrt(sum_d1 * sum_d2)

        correlations[sample] = sum_q / sqrt_d
    return correlations


def correlate(benchmark_name, target_dir):
    cor = calculate_correlation()

    plt.plot(cor)
    plt.title(f"{benchmark_name}")

    plt.text(0.5, 1.02, f"traces = {num_traces}, samples = {num_samples}",
             transform=plt.gca().transAxes, ha='center', fontsize=10)

    plt.xlabel("sample")
    plt.ylabel("correlation")

    save_path = f"{target_dir}/{benchmark_name}.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
