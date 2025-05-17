DEPTH = None 
CROSS_OP_LEAK = None 
CROSS_OP_TARGET_LEAK = None 
ADJ_DEPTH = None 

# TODO: Leak everything
# TODO: nop instruction does not clear (only something like xor-xor)
# TODO: sw leaks dst, adr, offset  

def macro_from_json(pipeline_config):
    global DEPTH, CROSS_OP_LEAK, CROSS_OP_TARGET_LEAK, ADJ_DEPTH


    leak_macros_str = ""
    DEPTH = pipeline_config["depth"]
    CROSS_OP_LEAK = pipeline_config["cross operand leakage"]
    CROSS_OP_TARGET_LEAK = pipeline_config["cross operand target leakage"]
    ADJ_DEPTH = pipeline_config["adjacent leakage depth"]

    if DEPTH < ADJ_DEPTH: 
        raise("Adjacent leakage depth is larger then pipeline depth!")

    return gen_pipeline_macro()

def gen_pipeline_macro(): 
    stage_variables_str = stage_variables()
    stage_shift_str = shift_stages()
    leak_str = ""

    stage_i = 0
    for stage_j in range(1, ADJ_DEPTH):
        leak_str += leak_stages(stage_i, stage_j)

    return (
        f"{stage_variables_str}\n"
        "macro leak_pipeline(w32 resultNew, w32 OpANew, w32 OpBNew)\n"
        "{\n"
        f"{stage_shift_str}" 
        f"{leak_str}"
        "}\n"
    )

def stage_variables():
    stage_variables_str = "// Pipeline stage variables\n"
    for s in range(0, DEPTH):
        stage_variables_str += f"w32 result{s};\n"
        stage_variables_str += f"w32 OpA{s};\n"
        stage_variables_str += f"w32 OpB{s};\n"
    return stage_variables_str

def leak_stages(i, j):
    leak_str = f"\n   // Leak stages {i}, {j}\n"

    leak_str += f"   leak pip (OpA{i} ^w32 OpA{j});\n"
    leak_str += f"   leak pip (OpB{i} ^w32 OpB{j});\n"
    leak_str += f"   leak pip (result{i} ^w32 result{j});\n"

    if CROSS_OP_LEAK:
        leak_str += f"\n   // Leak stages {i}, {j} cross op op\n"
        leak_str += f"   leak pip (OpA{i} ^w32 OpB{j});\n"
        leak_str += f"   leak pip (OpB{i} ^w32 OpA{j});\n"

    if CROSS_OP_TARGET_LEAK: 
        leak_str += f"\n   // Leak stages {i}, {j} cross op target\n"
        leak_str += f"   leak pip (result{i} ^w32 OpB{j});\n"
        leak_str += f"   leak pip (result{i} ^w32 OpA{j});\n"
        leak_str += f"   leak pip (result{j} ^w32 OpB{i});\n"
        leak_str += f"   leak pip (result{j} ^w32 OpA{i});\n"

    return leak_str

def shift_stages():
    first_stage = 0 
    move_values_str = "   // Shift pipeline stage variables\n"

    # shift stage values in pipeline variables
    for s in range(0, DEPTH-1):
        move_values_str += f"   OpA{s+1} <- OpA{s};\n"
        move_values_str += f"   OpB{s+1} <- OpB{s};\n"
        move_values_str += f"   result{s+1} <- result{s};\n"
    # write new values to first stage 
    move_values_str += "   // Insert new values into first stage of pipeline\n"
    move_values_str += f"   OpA{first_stage} <- OpANew;\n"
    move_values_str += f"   OpB{first_stage} <- OpBNew;\n"
    move_values_str += f"   result{first_stage} <- resultNew;\n"

    return move_values_str;
