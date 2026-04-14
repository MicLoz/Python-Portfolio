import json
import pandas as pd

def open_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

def json_to_df(json_file):
    data = open_json(json_file)
    return pd.DataFrame(data)