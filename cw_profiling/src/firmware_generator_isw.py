import subprocess

MAKEFILE_PATH = "firmware_files"
FIRMWARE_FILE_PATH = f"{MAKEFILE_PATH}/simpleserial-benchmark-template.c"

TEMPLATE_FIRST_HALF = """
#include <stdint.h>
#include <stdlib.h> // Required for malloc/free if used, but we'll use stack buffers

// Include HAL and SimpleSerial headers
#include "hal.h"
#include "simpleserial.h"

uint8_t get_pt(uint8_t* data, uint8_t len) {
    if (len != 16) { // We expect 8 bytes (16 hex chars) converted by simpleserial
        return 1; 
    }

    volatile uint32_t sharea0_mem  = (uint32_t)data[0] << 24 | (uint32_t)data[1] << 16 | (uint32_t)data[2] << 8 | data[3];
    volatile uint32_t sharea1_mem = (uint32_t)data[4] << 24 | (uint32_t)data[5] << 16 | (uint32_t)data[6] << 8 | data[7];
    volatile uint32_t shareb0_mem = 0;
    volatile uint32_t shareb1_mem = 1;
    volatile uint32_t r01_mem = (uint32_t)data[8] << 24 | (uint32_t)data[9] << 16 | (uint32_t)data[10] << 8 | data[11];
    volatile uint32_t r10_mem = (uint32_t)data[12] << 24 | (uint32_t)data[13] << 16 | (uint32_t)data[14] << 8 | data[15];
    volatile uint32_t mem0 = 0;
    volatile uint32_t mem1 = 0;
    volatile register uint32_t regA   asm("r1"); 
    volatile register uint32_t regB   asm("r3"); 
    volatile register uint32_t regC   asm("r5"); 
    volatile register uint32_t regD   asm("r7"); 
    volatile uint32_t zero = (uint32_t) 0;
    // --- Start of power trace capture ---
    trigger_high();
    
    // Microbenchmark
    asm volatile (
"""

TEMPLATE_SECOND_HALF = """
    );
    
    // --- End of power trace capture ---
    trigger_low();

    uint8_t result_buf[8];

    // 'r' command, 8 bytes of data
    simpleserial_put('r', 8, result_buf);

    return 0; // Indicate success
}


int main(void) {
    platform_init();

    init_uart();

    trigger_setup();
    simpleserial_init();

    // Register the SimpleSerial command 'p'
    // 'p': command character
    // 8: expected number of data bytes (16 hex characters input)
    // get_pt: callback function pointer
    simpleserial_addcmd('p', 16, get_pt);

    // Main loop: continuously check for and process incoming SimpleSerial data
    while (1) {
        simpleserial_get();
    }

    return 0;
}
"""


def create_firmware(microbenchmark_asm):
    with open(FIRMWARE_FILE_PATH, 'w') as f:
        indented_asm = '\n'.join('\t\t' + line for line in microbenchmark_asm.splitlines())
        firmware_str = TEMPLATE_FIRST_HALF + indented_asm + TEMPLATE_SECOND_HALF
        f.write(firmware_str)

    subprocess.run(["make", "-C", MAKEFILE_PATH])#,
           # stdout=subprocess.DEVNULL,
            #    stderr=subprocess.DEVNULL)
