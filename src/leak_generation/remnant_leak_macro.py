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

# TODO: Meetings at 11, skip next meeting 20 May

# TODO: sw leaks adr (what we want to write to memory)
# TODO: ld-ld is only cleared by ld 
# TODO: ld-st is only cleared by ld and st (same for st-ld)
# TODO: st-st is only cleared by st

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

    if ID == LD_LD_ID:
        mem_op_name = LD_LD
        op_last_id = LD_ID
        op_current_id = LD_ID
    if ID == ST_ST_ID:
        mem_op_name = ST_ST
        op_last_id = ST_ID
        op_current_id = ST_ID
    if ID == ST_LD_ID:
        mem_op_name = ST_LD
        op_last_id = ST_ID
        op_current_id = LD_ID
    if ID == LD_ST_ID:
        mem_op_name = LD_ST
        op_last_id = LD_ID
        op_current_id = ST_ID


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
        f"   lastInstructionId_{mem_op_name} <- currentInstructionId;\n"
        f"   remnantVal_{mem_op_name} <- newVal;\n"
        "}\n"
    )

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
