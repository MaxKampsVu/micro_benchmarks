include il "isa-ibex-rv32i.il"
include il "leakyisa-ibex-pres-rv32i.il"
include asm "micro_benchmarks/sram_remnant/ld-ld.objdump"

annotate micro_benchmark
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
  target: micro_benchmark;

print:
  kind: macrodef
  target: micro_benchmark
  verbosity: 1;

inlinecall:
  target: micro_benchmark;

partialeval:
  target: micro_benchmark;

print:
  kind: evaltrace
  target: micro_benchmark
  verbosity: 1;

infertaint:
  inputsAsPublic: true
  outputsAsPublic: true
  memoryAsPublicOut: true
  target: micro_benchmark;
  
check:
  kind: "NI"
  target: micro_benchmark;
...
