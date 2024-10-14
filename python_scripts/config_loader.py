# /Users/cassielu/Documents/myprogram/projects/AIST_Analyzer/python_scripts/config_loader.py

import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()

# 使用示例
# output_path = config['data']['output_path']
# window_length = config['analysis']['velocity_calculation']['window_length']