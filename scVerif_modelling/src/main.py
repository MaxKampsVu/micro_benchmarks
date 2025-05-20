from instructions import write_leaky_isa
import json
import subprocess
LEAKY_ISA_PATH = "../scVerif_files/leakyisa-ibex-pres-rv32i.il"

file_path = "../device_config.json"

file = open(file_path, 'r')

with open(file_path, 'r') as file:
    data = json.load(file)

write_leaky_isa(LEAKY_ISA_PATH, data)

cmd = ["scverif", "--il", "../scVerif_files/prev_risv.il"]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print("Command output:\n", result.stdout)
except subprocess.CalledProcessError as e:
    print("Command failed with return code:", e.returncode)
    print("Error output:\n", e.stderr)
except FileNotFoundError:
    print("Command not found: make sure 'scverif' is in your PATH.")
