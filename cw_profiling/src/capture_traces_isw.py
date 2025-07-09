import chipwhisperer as cw
from chipwhisperer.capture.api.programmers import STM32FProgrammer
from tqdm import trange
import random
import numpy as np
import logging

MICRO_BENCHMARK_HEX_PATH = "firmware_files/simpleserial-benchmark-template-CW308_STM32F3.hex"


def random_payload():
    share0_val = random.getrandbits(32)
    share1_val = random.getrandbits(32)
    r0_val = random.getrandbits(32)
    r1_val = random.getrandbits(32)

    share0_bytes = share0_val.to_bytes(4, 'big')
    share1_bytes = share1_val.to_bytes(4, 'big')
    r0_bytes = r0_val.to_bytes(4, 'big')
    r1_bytes = r1_val.to_bytes(4, 'big')

    return share0_bytes + share1_bytes + r0_bytes + r1_bytes


def capture(num_traces, num_samples):
    textins = []
    traces = []
    cw.set_all_log_levels(logging.CRITICAL) # reduce logging
    scope = cw.scope()
    scope.default_setup()
    target = cw.target(scope)
    program = STM32FProgrammer
    scope.adc.samples = num_samples
    cw.program_target(scope, program, MICRO_BENCHMARK_HEX_PATH) 

    # Loop through all traces
    for i in trange(num_traces, desc="Capturing traces"):
        payload = random_payload()

        scope.arm()
        target.simpleserial_write('p', payload)
        ret = scope.capture()

        if ret:
            print("Timeout during capture")
            exit()

        target.simpleserial_read_witherrors('r', 8, timeout=1000)

        textins.append(payload[:8]) # only append share value 
        traces.append(scope.get_last_trace())

    np_traces = np.asarray(traces)
    np_textins = np.asarray(textins)

    np.save('trace_files/traces.npy', np_traces)
    np.save('trace_files/textins.npy', np_textins)

    scope.dis()
    target.dis()
