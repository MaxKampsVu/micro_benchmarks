# Target specific defines
TARGET ?= simpleserial-benchmark-template
SRC = simpleserial-benchmark-template.c

PLATFORM ?= CW308_STM32F3

# Build SimpleSerial V1.1 (ASCII Hex based)
SS_VER = SS_VER_1_1

CRYPTO_TARGET = NONE

# Include common SimpleSerial and build rules
include /home/max/chipwhisperer/firmware/mcu/simpleserial/Makefile.simpleserial

FIRMWAREPATH = /home/max/chipwhisperer/firmware/mcu
include $(FIRMWAREPATH)/Makefile.inc
