def macro_from_json(sram_overwrite_config):
    return (
        "macro leak_sram_overwrite(w32 dst, w32 val)\n"
        "{\n"
        "   leak sramOverwrite(dst ^w32 val);\n"
        "}\n"
    )