"""
Data Utilities: Load and process harmful behavior datasets

This module provides utilities for:
- Loading AdvBench harmful behaviors CSV file
- Parsing goals and target descriptions
- Managing data offset for batch processing
- Preparing data for attack experiments

Supported Datasets: AdvBench (CSV format with goal/target columns)
"""

import pandas as pd

def get_goals_and_targets(params):

    train_goals = getattr(params, 'goals', [])
    train_targets = getattr(params, 'targets', [])
    offset = getattr(params, 'data_offset', 0)

    if params.train_data:
        train_data = pd.read_csv(params.train_data)
        train_targets = train_data['target'].tolist()[offset:offset+params.n_train_data]
        if 'goal' in train_data.columns:
            train_goals = train_data['goal'].tolist()[offset:offset+params.n_train_data]
        else:
            train_goals = [""] * len(train_targets)

    assert len(train_goals) == len(train_targets)
    print('Loaded {} pompts'.format(len(train_goals)))

    return train_goals, train_targets