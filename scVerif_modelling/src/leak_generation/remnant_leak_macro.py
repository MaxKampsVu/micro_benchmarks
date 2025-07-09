LD_LD = "ld_ld"
ST_ST = "st_st"
ST_LD = "st_ld"
LD_ST = "ld_st"
LD_LD_ID = 0
ST_ST_ID = 1
ST_LD_ID = 2
LD_ST_ID = 3
ST_ID = 0
LD_ID = 1


def macro_from_json(remnant_config):
    macros_str = ""
    if remnant_config["ld-ld"]:
        macros_str += gen_remnant_macro(LD_LD_ID)
    if remnant_config["st-st"]:
        macros_str += gen_remnant_macro(ST_ST_ID)
    if remnant_config["st-ld"]:
        macros_str += gen_remnant_macro(ST_LD_ID)
    if remnant_config["ld-st"]:
        macros_str += gen_remnant_macro(LD_ST_ID)

    return macros_str


def gen_remnant_macro(ID):
    mem_op_name = 0  # name for the remnant leak effect
    op_last_id = 0  # id for the last memory operation (ld/st)
    op_current_id = 0  # id for the current memory operation (ld/st)
    clear_by_ld = -1  # the remnant can be cleared by a load (set to LD_ID if true)
    clear_by_st = -1  # the remnant can be cleared by a store (set to ST_ID if true)

    if ID == LD_LD_ID:
        mem_op_name = LD_LD
        op_last_id = LD_ID
        op_current_id = LD_ID
        clear_by_ld = LD_ID
    if ID == ST_ST_ID:
        mem_op_name = ST_ST
        op_last_id = ST_ID
        op_current_id = ST_ID
        clear_by_st = ST_ID
    if ID == ST_LD_ID:
        mem_op_name = ST_LD
        op_last_id = ST_ID
        op_current_id = LD_ID
        clear_by_st = ST_ID
        clear_by_ld = LD_ID
    if ID == LD_ST_ID:
        mem_op_name = LD_ST
        op_last_id = LD_ID
        op_current_id = ST_ID
        clear_by_st = ST_ID

    return (
        f"w32 remnantVal_{mem_op_name};\n"
        f"w32 lastInstructionId_{mem_op_name};\n\n"
        f"// Leak remnant for sequence: {mem_op_name}\n"
        f"macro leak_remnant_{mem_op_name}(w32 newVal, w32 currentInstructionId)\n"
        "{\n"
        f"   if (lastInstructionId_{mem_op_name} == (w32) {op_last_id}) \n"
        "   {\n"
        f"      if (currentInstructionId == (w32) {op_current_id}) \n"
        "      {\n"
        f"         leak remnant (newVal ^w32 remnantVal_{mem_op_name});\n"
        "      }\n"
        "   }\n"
        # update remnant and last instruction if remnant can be cleared by st
        f"   if (currentInstructionId == (w32) {clear_by_st}) \n"
        "   {\n"
        f"      lastInstructionId_{mem_op_name} <- currentInstructionId;\n"
        f"      remnantVal_{mem_op_name} <- newVal;\n"
        "   }\n"
        # update remnant and last instruction if remnant can be cleared by ld
        f"   if (currentInstructionId == (w32) {clear_by_ld}) \n"
        "   {\n"
        f"      lastInstructionId_{mem_op_name} <- currentInstructionId;\n"
        f"      remnantVal_{mem_op_name} <- newVal;\n"
        "   }\n"
        "}\n"
    )


# create triggers for ld3_leak and st3_leak to call the leak_remnant macros
def trigger_from_json(remnant_config, is_ld):
    trigger_str = ""
    if remnant_config["ld-ld"]:
        trigger_str += f"   leak_remnant_{LD_LD}(remnantVal, (w32) {int(is_ld)});\n"
    if remnant_config["st-st"]:
        trigger_str += f"   leak_remnant_{ST_ST}(remnantVal, (w32) {int(is_ld)});\n"
    if remnant_config["st-ld"]:
        trigger_str += f"   leak_remnant_{ST_LD}(remnantVal, (w32) {int(is_ld)});\n"
    if remnant_config["ld-st"]:
        trigger_str += f"   leak_remnant_{LD_ST}(remnantVal, (w32) {int(is_ld)});\n"
    return trigger_str


def ld_trigger_from_json(remnant_config):
    return trigger_from_json(remnant_config, True)


def st_trigger_from_json(remnant_config):
    return trigger_from_json(remnant_config, False)


# initialize the remnant state
def init_variables(remnant_config):
    init_str = ""
    if remnant_config["ld-ld"]:
        init_str += f"   lastInstructionId_{LD_LD} <- (w32) 0;\n"
    if remnant_config["st-st"]:
        init_str += f"   lastInstructionId_{ST_ST} <- (w32) 0;\n"
    if remnant_config["st-ld"]:
        init_str += f"   lastInstructionId_{ST_LD} <- (w32) 0;\n"
    if remnant_config["ld-st"]:
        init_str += f"   lastInstructionId_{LD_ST} <- (w32) 0;\n"
    return init_str
