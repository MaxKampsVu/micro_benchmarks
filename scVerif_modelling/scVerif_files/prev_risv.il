include il "../scVerif_files/isa-ibex-rv32i.il"
include il "../scVerif_files/leakyisa-ibex-pres-rv32i.il"
include asm "../scVerif_files/testfile_no_nothing.objdump"

annotate micro_benchmark
    region mem w32 sharea_mem[0:1]
    region mem w32 shareb_mem[0:1]
    region mem w32 zero_mem[0:1]
    region mem w32 memory[0:1]
    region mem w32 random[0:1]
    region mem w32 z[0:1]
    init a0 [sharea_mem 0]
    init a1 [shareb_mem 0]
    init a2 [zero_mem 0]
    init a3 [memory 0]
    init a4 [random 0]
    init a5 [z 0]
    input sharing sharea_mem
    input urandom random
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