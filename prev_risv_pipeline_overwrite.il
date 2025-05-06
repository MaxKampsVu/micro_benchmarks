include il "isa-ibex-rv32i.il"
include il "leakyisa-ibex-pres-rv32i.il"
include asm "micro_benchmarks/pipeline_overwrite/xor-xor-depth-2-cleared.objdump"

annotate pipeline_overwrite
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
  target: pipeline_overwrite;

print:
  kind: macrodef
  target: pipeline_overwrite
  verbosity: 1;

inlinecall:
  target: pipeline_overwrite;

partialeval:
  target: pipeline_overwrite;

print:
  kind: evaltrace
  target: pipeline_overwrite
  verbosity: 1;

infertaint:
  inputsAsPublic: true
  outputsAsPublic: true
  memoryAsPublicOut: true
  target: pipeline_overwrite;
  
check:
  kind: "NI"
  target: pipeline_overwrite;
...
