import os

os.sys.path.append("..")
from configs.template import get_config as default_config

def get_config():
    config = default_config()

    config.model_path = "gpt-5.5"
    config.train_data = "../data/custom/test_prompts.csv"
    config.vis_dict_path = "cache/scores_gpt-5.5.json"
    config.noun_wordgame = True
    config.noun_sub = True
    config.verb_sub = True
    config.n_train_data = 6

    return config
