"""
Ad-hoc script to pretty print JSON.
"""

import json

with open(r"C:\Users\Mikel\PycharmProjects\Portfolio\Project1_DataPipeline\data\testdata.JSON") as f:
    data = json.load(f)

print(json.dumps(data, indent=4))