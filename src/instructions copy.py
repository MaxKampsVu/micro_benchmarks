def write_leaky_isa(reg_ow_flag, sram_ow_flag, remnant_flag, pipeline_depth, leaky_isa_file):
    with open(leaky_isa_file, 'w') as f:
        if remnant_flag:
            f.write(gen_remnant_leak() + '\n')
        
        if pipeline_depth != 0:
            f.write(gen_pipeline_leak(pipeline_depth) + '\n')
        
        f.write(gen_xor(reg_ow_flag, pipeline_depth) + '\n')
        f.write(gen_and(reg_ow_flag, pipeline_depth) + '\n')
        f.write(gen_nop() + '\n')
        f.write(gen_mov(reg_ow_flag) + '\n')
        f.write(gen_lw(reg_ow_flag, remnant_flag) + '\n')
        f.write(gen_sw(sram_ow_flag, remnant_flag) + '\n')




def gen_remnant_leak():
    return (
        "w32 remnantVal;\n\n"
        "macro leak_remnant(w32 adr, w32 val)\n"
        "{\n"
        "   leak remnant (val ^w32 remnantVal);\n"
        "   remnantVal <- val;\n"
        "}\n"
    )



def gen_xor(reg_ow_flag, pipeline_depth):
    reg_overwrite_leak = "leak registerOverwrite(rd ^w32 (rs1 ^w32 rs2));\n" if reg_ow_flag else ""
    pipeline_leak = "leak_pipeline(rs1, rs2, rs1 ^w32 rs2);\n" if pipeline_depth != 0 else ""
    return (
        "macro xor3_leak(w32 rd, w32 rs1, w32 rs2)\n"
        "{\n"
        f"   {reg_overwrite_leak}"
        f"{pipeline_leak}"
        "   leak resultTransition(rd, rs1 ^w32 rs2);\n"
        "}\n"
    )

def gen_and(reg_ow_flag, pipeline_depth):
    reg_overwrite_leak = "leak registerOverwrite(rd ^w32 (rs1 &w32 rs2));\n" if reg_ow_flag else ""
    pipeline_leak = "leak_pipeline(rs1, rs2, rs1 &w32 rs2);\n" if pipeline_depth != 0 else ""
    return (
        "macro and3_leak(w32 rd, w32 rs1, w32 rs2)\n"
        "{\n"
        f"   {reg_overwrite_leak}"
        f"{pipeline_leak}"
        "   leak resultTransition(rd, rs1 &w32 rs2);\n"
        "}\n"
    )

def gen_nop():
    return (
        "macro nop0_leak()\n"
        "{\n"
        "\n"
        "}\n"
    )

def gen_mov(reg_ow_flag):
    reg_overwrite_leak = "leak registerOverwrite(dst ^w32 adr);" if reg_ow_flag else ""
    return (
        "macro mov2_leak(w32 dst, w32 adr)\n"
        "{\n"
        f"   {reg_overwrite_leak}\n"
        "}\n"
    )

def gen_lw(reg_ow_flag, remnant_flag):
    # Leak the value loaded from memory xor the target register
    reg_overwrite_leak = "leak registerOverwrite(dst ^w32 val);" if reg_ow_flag else ""
    remnant_leak       = "leak_remnant(adr, val);" if remnant_flag else ""
    return (
        "macro lw3_leak(w32 dst, w32 adr, w32 ofs)\n"
        "   w32 val\n"
        "{\n"
        f"  val <- [w32 mem (int) (adr +w32 ofs)];\n"
        f"   {reg_overwrite_leak}\n"
        f"   {remnant_leak}\n"
        "   leak loadTransition(dst, val);\n"
        "}\n"
    )

def gen_sw(sram_ow_flag, remnant_flag):
    # Leak the value to be written to memory xor the old value in memory 
    sram_overwrite_leak = "leak sramOverwrite(adr ^w32 [w32 mem (int) (adr +w32 ofs)]);" if sram_ow_flag else ""
    remnant_leak        = "leak_remnant(adr, val);" if remnant_flag else ""
    return (
        "macro sw3_leak(w32 dst, w32 adr, w32 ofs)\n"
        "   w32 val\n"
        "{\n"
        f"  val <- [w32 mem (int) (adr +w32 ofs)];"
        f"   {sram_overwrite_leak}\n"
        f"   {remnant_leak}\n"
        "   leak storeTransition(dst, val);\n"
        "}\n"
    )

def gen_pipeline_leak(depth): 
    first_stage = depth - 1 

    stage_variables_str = ""
    for s in range(0, depth):
        stage_variables_str += f"w32 result{s};\n"
        stage_variables_str += f"w32 OpA{s};\n"
        stage_variables_str += f"w32 OpB{s};\n"

    pipeline_leak_str = ""
    # For now just leak adjacent 
    for s in range(1, depth):
        pipeline_leak_str += f"   leak pip (OpA{s-1} ^w32 OpA{s});\n"
        pipeline_leak_str += f"   leak pip (OpB{s-1} ^w32 OpB{s});\n"
        pipeline_leak_str += f"   leak pip (OpA{s-1} ^w32 OpB{s});\n"
        pipeline_leak_str += f"   leak pip (OpB{s-1} ^w32 OpA{s});\n"
        pipeline_leak_str += f"   leak pip (result{s-1} ^w32 result{s});\n"

    move_values_str = ""
    # shift the values in the pipeline when new instructions arrives  
    for s in range(1, depth):
        move_values_str += f"   OpA{s-1} <- OpA{s};\n"
        move_values_str += f"   OpB{s-1} <- OpB{s};\n"
        move_values_str += f"   result{s-1} <- result{s};\n"
    # write new values to first stage 
    move_values_str += f"   OpA{first_stage} <- OpANew;\n"
    move_values_str += f"   OpB{first_stage} <- OpBNew;\n"
    move_values_str += f"   result{first_stage} <- resultNew;\n"

    return (
        f"{stage_variables_str}\n"
        "macro leak_pipeline(w32 OpANew, w32 OpBNew, w32 resultNew)\n"
        "{\n"
        f"{move_values_str}" 
        f"{pipeline_leak_str}"
        "}\n"
    )