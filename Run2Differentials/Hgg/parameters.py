from collections import OrderedDict as od
import yaml
from yaml import Loader

# model_file = "/work/gallim/DifferentialCombination_home/DifferentialCombinationRun2/metadata/SMEFT/220823Atlas2DScans.yml"
model_file = "/work/gallim/DifferentialCombination_home/DifferentialCombinationRun2/metadata/SMEFT/220823Atlas2DScans_chg.yml"
with open(model_file) as f:
    dct = yaml.load(f, Loader=Loader)

pois = od()
for coeff in dct.keys():
    pois[coeff] = {
        "factor": 1,
        "multiplier": 1,
        "range": [dct[coeff]["min"], dct[coeff]["max"]],
        "nominal": 0,
    }
# print(pois)
