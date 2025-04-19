include il "isa-ibex-rv32i.il"
include il "micro_benchmarks/register_overwrite/leakyisa-ibex-pres-rv32i.il"
include asm "micro_benchmarks/register_overwrite/pres_riscv_register_overwrite.objdump"

annotate register_overwrite
    region mem w32 x[0:1]
    region mem w32 z[0:1]
    init a0 [x 0]
    init a1 [z 0]
    input sharing x
    output sharing z;

---
addleakage:
  target: register_overwrite;

print:
  kind: macrodef
  target: register_overwrite
  verbosity: 1;

inlinecall:
  target: register_overwrite;

partialeval:
  target: register_overwrite;

print:
  kind: evaltrace
  target: register_overwrite
  verbosity: 1;

infertaint:
  inputsAsPublic: true
  outputsAsPublic: true
  memoryAsPublicOut: true
  target: register_overwrite;
  
check:
  kind: "NI"
  target: register_overwrite;
...
