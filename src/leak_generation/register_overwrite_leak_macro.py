def macro_from_json(register_overwrite_configg):
    return (
        "macro leak_register_overwrite(w32 dst, w32 adr)\n"
        "{\n"
        "   leak registerOverwrite(dst ^w32 adr);\n"
        "}\n"
    )
