import json

import leak_generation.remnant_leak_macro as remnant_gen
import leak_generation.pipeline_overwrite_leak_macro as pipeline_gen

file_path = "/Users/maximiliankamps/Desktop/Gadgets-Tools/micro-benchmarks/device_config.json"

file = open(file_path, 'r')

with open(file_path, 'r') as file:
    data = json.load(file)  


def print_effects(json_config_data):
    remnant_parameters = json_config_data["remnant effect"]["parameters"]

    pipeline_parameters = json_config_data["pipeline overwrite effect"]["parameters"]
    
    print(remnant_gen.macro_from_json(remnant_parameters))    
    # print(pipeline_gen.macro_from_json(pipeline_parameters))

print_effects(data)