include il "isa-ibex-rv32i.il"
include il "micro_benchmarks/sram_remnant/leakyisa-ibex-pres-rv32i.il"
include asm "micro_benchmarks/sram_remnant/pres_riscv_sram_remnant.objdump"

annotate sram_remnant
    region mem w32 x[0:1]
    region mem w32 mem[0:1]
    region mem w32 z[0:1]
    init a0 [x 0]
    init a1 [mem 0]
    init a2 [z 0]
    input sharing x
    output sharing z;

---
addleakage:
  target: sram_remnant;

print:
  kind: macrodef
  target: sram_remnant
  verbosity: 1;

inlinecall:
  target: sram_remnant;

partialeval:
  target: sram_remnant;

print:
  kind: evaltrace
  target: sram_remnant
  verbosity: 1;

infertaint:
  inputsAsPublic: true
  outputsAsPublic: true
  memoryAsPublicOut: true
  target: sram_remnant;
  
check:
  kind: "NI"
  target: sram_remnant;
...
