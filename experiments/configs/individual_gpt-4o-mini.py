import os

os.sys.path.append("..")
from configs.template import get_config as default_config

def get_config():
    
    config = default_config()

    config.model_path = "gpt-4o-mini"
    config.train_data = "../data/advbench/harmful_behaviors.csv"
    config.vis_dict_path = "cache/scores_gpt-4o-mini.json"
    config.noun_wordgame = True
    config.noun_sub = True
    config.verb_sub = True

    return config
