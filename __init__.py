import os
from src.auth import *
from src.commands import *

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(PROJECT_PATH, "env.json")
check_config = os.path.isfile(config_path)

cfg_template = { "AA": {
    "default_cr": "sbx",
    "env_list": [
        {
        "name": "sbx",
        "auth_type": "token",
        "endpoint": "https://<<control_room>>.<<env>>.automationanywhere.digital",
        "userid": "<<userid>>",
        "api_key": "<<api_key>>"
        }
      ]
}}

if check_config:
    with open(config_path, "r") as f:
        cfg = json.load(f)
else:
    print(f"Config file not found at {config_path}")
    print(f"Creating template at {PROJECT_PATH}/craapy_template.json")
    with open(os.path.join(PROJECT_PATH, "craapy_template.json"), "w") as f:
        # Writing tepmlate to PROJECT_PATH
        f.write(json.dumps(cfg_template, indent=2))

CFG_FILE = cfg
    