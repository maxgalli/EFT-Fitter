"""
Here the convention is slightly different from the STXS one. We don't have a giant string but already 
a dictionary with keys:
A_poi: linear
B_poi_2: quadratic
B_poi_kpoi: mixed
"""
import json
import os
from collections import OrderedDict as od

edges = [
    0.0,
    5.0,
    10.0,
    15.0,
    20.0,
    25.0,
    30.0,
    35.0,
    45.0,
    60.0,
    80.0,
    100.0,
    120.0,
    140.0,
    170.0,
    200.0,
    250.0,
    350.0,
    450.0,
    10000.0,
]
decay_file_conversions = {"gamgam": "hgg"}
input_dir = "/work/gallim/DifferentialCombination_home/EFTScalingEquations/equations/CMS-prelim-SMEFT-topU3l_22_05_05"

functions = od()
for decay_channel_dir in os.listdir(os.path.join(input_dir, "differentials")):
    with open(
        os.path.join(
            input_dir, "differentials", decay_channel_dir, "ggH_SMEFTatNLO_pt_gg.json"
        ),
        "r",
    ) as f:
        tmp_dct = json.load(f)
        for edge, next_edge in zip(edges[:-1], edges[1:]):
            functions[
                "{}_{}".format(
                    str(edge).replace(".0", ""), str(next_edge).replace(".0", "")
                )
            ] = tmp_dct[str(edge)]

with open("{}/decay.json".format(input_dir), "r") as f:
    decay_terms = json.load(f)
for decay_channel in decay_terms:
    functions[decay_channel] = decay_terms[decay_channel]


# print(functions)
# print(functions.keys())
