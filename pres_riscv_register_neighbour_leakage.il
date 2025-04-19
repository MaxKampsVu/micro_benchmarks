include il "isa-ibex-rv32i.il"
include il "micro_benchmarks/register_neighbour_leakage/leakyisa-ibex-pres-rv32i.il"
include asm "micro_benchmarks/register_neighbour_leakage/pres_riscv_register_overwrite.objdump"

annotate register_neighbour
    region mem w32 x[0:1]
    region mem w32 z[0:1]
    init a0 [x 0]
    init a1 [z 0]
    input sharing x
    output sharing z;

---
addleakage:
  target: register_neighbour;

print:
  kind: macrodef
  target: register_neighbour
  verbosity: 1;

inlinecall:
  target: register_neighbour;

partialeval:
  target: register_neighbour;

print:
  kind: evaltrace
  target: register_neighbour
  verbosity: 1;

infertaint:
  inputsAsPublic: true
  outputsAsPublic: true
  memoryAsPublicOut: true
  target: register_neighbour;
  
check:
  kind: "NI"
  target: register_neighbour;
...
