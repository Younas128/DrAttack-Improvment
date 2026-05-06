import os

os.sys.path.append("..")
from configs.template import get_config as default_config

def get_config():
    
    config = default_config()

    config.model_path = "gemini-2.0-flash"
    config.vis_dict_path = "../../experiments/cache/scores_gemini-2.0-flash.json"
    
    return config
