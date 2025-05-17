import json
# source ~/.bash_profile
import leak_generation.remnant_leak_macro as remnant_gen
import leak_generation.pipeline_overwrite_leak_macro as pipeline_gen
import leak_generation.register_overwrite_leak_macro as reg_ow_gen 
import leak_generation.sram_overwrite_leak_macro as sram_ow_gen


LEAK_PIPELINE = False 
LEAK_REMNANT = False
LEAK_REG_OVERWRITE = False
LEAK_SRAM_OVERWRITE = False 


def write_leaky_isa(leaky_isa_file, json_config_data):
    global LEAK_PIPELINE, LEAK_REMNANT, LEAK_REG_OVERWRITE, LEAK_SRAM_OVERWRITE
    remnant_parameters = json_config_data["remnant effect"]["parameters"]
    pipeline_parameters = json_config_data["pipeline overwrite effect"]["parameters"]


    with open(leaky_isa_file, 'w') as f:
        LEAK_REMNANT = json_config_data["remnant effect"]["enabled"]
        LEAK_PIPELINE = json_config_data["pipeline overwrite effect"]["enabled"]
        LEAK_REG_OVERWRITE = json_config_data["register overwrite effect"]["enabled"]
        LEAK_SRAM_OVERWRITE = json_config_data["sram overwrite effect"]["enabled"]

        if LEAK_REMNANT:
            f.write(remnant_gen.macro_from_json(remnant_parameters) + '\n')

        if LEAK_PIPELINE:
            f.write(pipeline_gen.macro_from_json(pipeline_parameters) + '\n')

        if LEAK_REG_OVERWRITE:
            f.write(reg_ow_gen.macro_from_json(None) + '\n')

        if LEAK_SRAM_OVERWRITE:
            f.write(sram_ow_gen.macro_from_json(None) + '\n')

        f.write(gen_initState(remnant_parameters) + '\n')
        f.write(gen_xor() + '\n')
        f.write(gen_and() + '\n')
        f.write(gen_nop() + '\n')
        f.write(gen_mov() + '\n')
        f.write(gen_lw(remnant_parameters) + '\n')
        f.write(gen_sw(remnant_parameters) + '\n')

def gen_initState(remnant_parameters):
    remnant_leak = remnant_gen.init_variables(remnant_parameters) if LEAK_REMNANT else ""
    return (
        "macro is0_leak()\n"
        "{\n"
        f"{remnant_leak}"
        "}\n"
    )

def gen_xor():
    pipeline_leak = "leak_pipeline(rs1 ^w32 rs2, rs1, rs2);" if LEAK_PIPELINE != 0 else ""
    reg_overwrite_leak = "leak_register_overwrite(rd, rs1 ^w32 rs2);" if LEAK_REG_OVERWRITE else ""
    return (
        "macro xor3_leak(w32 rd, w32 rs1, w32 rs2)\n"
        "{\n"
        f"   {pipeline_leak}\n"
        f"   {reg_overwrite_leak}\n"
        "   leak resultTransition(rd, rs1 ^w32 rs2);\n"
        "}\n"
    )

def gen_and():
    pipeline_leak = "leak_pipeline(rs1 &w32 rs2, rs1, rs2);" if LEAK_PIPELINE != 0 else ""
    reg_overwrite_leak = "leak_register_overwrite(rd, rs1 &w32 rs2);" if LEAK_REG_OVERWRITE else ""
    return (
        "macro and3_leak(w32 rd, w32 rs1, w32 rs2)\n"
        "{\n"
        f"   {reg_overwrite_leak}\n"
        f"   {pipeline_leak}\n"
        "   leak resultTransition(rd, rs1 &w32 rs2);\n"
        "}\n"
    )

def gen_nop():
    pipeline_leak = "leak_pipeline((w32) 0, (w32) 0, (w32) 0);" if LEAK_PIPELINE else ""
    return (
        "macro nop0_leak()\n"
        "{\n"
        f"   {pipeline_leak}\n"
        "}\n"
    )

def gen_mov():
    pipeline_leak = "leak_pipeline(dst, adr, (w32) 0);" if LEAK_PIPELINE else ""
    reg_overwrite_leak = "leak_register_overwrite(dst, adr);" if LEAK_REG_OVERWRITE else ""
    return (
        "macro mov2_leak(w32 dst, w32 adr)\n"
        "{\n"
        f"   {pipeline_leak}\n"
                f"   {reg_overwrite_leak}\n"
        "}\n"
    )

def gen_lw(remnant_parameters):
    pipeline_leak = "leak_pipeline(val, adr, ofs);" if LEAK_PIPELINE else ""
    remnant_leak = f"{remnant_gen.ld_trigger_from_json(remnant_parameters)}" if LEAK_REMNANT else ""
    reg_overwrite_leak = "leak_register_overwrite(dst, val);" if LEAK_REG_OVERWRITE else ""
    return (
        "macro lw3_leak(w32 dst, w32 adr, w32 ofs)\n"
        "   w32 remnantVal,\n"
        "   w32 val\n"
        "{\n"
        f"   remnantVal <- [w32 mem (int) (adr +w32 ofs)];\n"
        f"   val <- [w32 mem (int) (adr +w32 ofs)];\n"
        f"   {pipeline_leak}\n"
        f"{remnant_leak}\n"
        f"   {reg_overwrite_leak}\n"
        "   leak loadTransition(dst, val);\n"
        "}\n"
    )

# TODO: sw should leak the value stored into memory (not the previous value at the memory address)

def gen_sw(remnant_parameters):
    pipeline_leak = "leak_pipeline(dst, adr, ofs);" if LEAK_PIPELINE else ""
    remnant_leak = f"{remnant_gen.st_trigger_from_json(remnant_parameters)}" if LEAK_REMNANT else ""
    sram_overwrite_leak = "leak_sram_overwrite(dst, val);" if LEAK_SRAM_OVERWRITE else ""
    return (
        "macro sw3_leak(w32 dst, w32 adr, w32 ofs)\n"
        "   w32 remnantVal,\n"
        "   w32 val\n"
        "{\n"
        f"   remnantVal <- dst;\n"
        f"   val <- [w32 mem (int) (adr +w32 ofs)];\n"
        f"   {pipeline_leak}\n"
        f"   {remnant_leak}\n"
        f"   {sram_overwrite_leak}\n"
        "   leak storeTransition(dst, val);\n"
        "}\n"
    )


LEAKY_ISA_PATH = "leakyisa-ibex-pres-rv32i.il"

file_path = "/Users/maximiliankamps/Desktop/Gadgets-Tools/micro-benchmarks/device_config.json"

file = open(file_path, 'r')

with open(file_path, 'r') as file:
    data = json.load(file)  

write_leaky_isa(LEAKY_ISA_PATH, data)