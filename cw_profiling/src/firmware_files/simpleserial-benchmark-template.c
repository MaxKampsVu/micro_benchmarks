
#include <stdint.h>
#include <stdlib.h> // Required for malloc/free if used, but we'll use stack buffers

// Include HAL and SimpleSerial headers
#include "hal.h"
#include "simpleserial.h"

uint32_t rand_uint32() {
    return ((uint32_t)rand() << 16) | ((uint32_t)rand() & 0xFFFF);
}

// Helper function to convert a single hex character to its integer value
static uint8_t hex_to_int(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    } else if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    }
    return 0; // Should not happen with valid input
}

// Helper function to convert 8 (big-endian) hex characters (representing 4 bytes) to a uint32_t
static uint32_t hex_to_uint32(const uint8_t* hex_chars) {
    uint32_t val = 0;
    for (int i = 0; i < 8; ++i) {
        val = (val << 4) | hex_to_int((char)hex_chars[i]);
    }
    return val;
}

// Helper function to convert a uint32_t to 8 (big-endian) hex characters 
static void uint32_to_hex(uint32_t val, uint8_t* hex_buf) {
    for (int i = 7; i >= 0; --i) {
        uint8_t nibble = (val >> (i * 4)) & 0x0F;
        if (nibble < 10) {
            hex_buf[7 - i] = '0' + nibble;
        } else {
            hex_buf[7 - i] = 'A' + (nibble - 10);
        }
    }
}



// SimpleSerial command handler for 'p' (process/plain) command
// Input 'data' contains 16 hex characters (8 bytes total)
// representing r0 (first 8 chars) and share0 (next 8 chars).
// Returns 0 on success.
uint8_t get_pt(uint8_t* data, uint8_t len) {
    if (len != 8) { // We expect 8 bytes (16 hex chars) converted by simpleserial
        return 1; 
    }

    volatile uint32_t share0  = (uint32_t)data[0] << 24 | (uint32_t)data[1] << 16 | (uint32_t)data[2] << 8 | data[3];
    volatile uint32_t share1 = (uint32_t)data[4] << 24 | (uint32_t)data[5] << 16 | (uint32_t)data[6] << 8 | data[7];
    volatile register uint32_t regA   asm("r1"); 
    volatile register uint32_t regB   asm("r2"); 
    volatile register uint32_t regC   asm("r3"); 
    volatile register uint32_t regD   asm("r4"); 
    volatile register uint32_t regE   asm("r5"); 
    volatile register uint32_t regF   asm("r6"); 
    volatile register uint32_t regG   asm("r7");
    volatile uint32_t zero = (uint32_t) 0;
    // --- Start of power trace capture ---
    trigger_high();
    
    // Microbenchmark
    asm volatile (
		
		
		"ldr %2, [%10]\n"
		"ldr %0, [%7]\n"
		"ldr %2, [%10]\n"
		
		"ldr %2, [%10]\n"
		"ldr %6, [%8]\n"
		"ldr %2, [%10]\n"
		"eor %2, %9, %9\n"
		"eor %2, %9, %9\n"
		"eor %2, %9, %9\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"nop\n"
		"eor %2, %0, %9\n"
		"eor %4, %4, %4\n"
		"eor %3, %6, %9\n"
		
		: "+r" (regA), "+r" (regB), "+r" (regC), "+r" (regD), "+r" (regE), "+r" (regF), "+r" (regG)
		: "r" (&share0), "r" (&share1), "r" (zero), "r" (&zero)
		:
		
    );
    
    // --- End of power trace capture ---
    trigger_low();

    uint8_t result_buf[4];

    // 'r' command, 4 bytes of data
    simpleserial_put('r', 4, result_buf);

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
    simpleserial_addcmd('p', 8, get_pt);

    // Main loop: continuously check for and process incoming SimpleSerial data
    while (1) {
        simpleserial_get();
    }

    return 0;
}
