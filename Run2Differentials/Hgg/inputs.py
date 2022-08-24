import json
from collections import OrderedDict as od

name = "HggDiff"
decay_channel = "hgg"

with open("Run2Differentials/Hgg/mus.json", "r") as f:
    dct = json.load(f)

pois = [
    "r_smH_PTH_0_5",
    "r_smH_PTH_5_10",
    "r_smH_PTH_10_15",
    "r_smH_PTH_15_20",
    "r_smH_PTH_20_25",
    "r_smH_PTH_25_30",
    "r_smH_PTH_30_35",
    "r_smH_PTH_35_45",
    "r_smH_PTH_45_60",
    "r_smH_PTH_60_80",
    "r_smH_PTH_80_100",
    "r_smH_PTH_100_120",
    "r_smH_PTH_120_140",
    "r_smH_PTH_140_170",
    "r_smH_PTH_170_200",
    "r_smH_PTH_200_250",
    "r_smH_PTH_250_350",
    "r_smH_PTH_350_450",
    "r_smH_PTH_GT450",
]

X = od()
for poi in pois:
    X["{}_{}".format(decay_channel, poi)] = dct[poi]

# print(X)

with open("Run2Differentials/Hgg/correlation_matrix.json", "r") as f:
    dct = json.load(f)
rho = od()
for poi in pois:
    for poi_int in pois:
        if poi != poi_int:
            rho[
                (
                    "{}_{}".format(decay_channel, poi),
                    "{}_{}".format(decay_channel, poi_int),
                )
            ] = dct[poi][poi_int]
# print(rho)
