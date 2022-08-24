# EFT-Fitter

Here the information necessary to run the check for differentials interpretation.

Example to run fit:
```
python runFit.py --pois Run2Differentials.Hgg.parameters --functions Run2Differentials.Hgg.functions --inputs Run2Differentials.Hgg.inputs --doAsimov --doReset --differentials
```
Example to plot:
```
for par in chg chgtil; do python makeChi2Plot.py --poi $par --inputPkl results_asimov_reset.pkl --outputDir /eos/home-g/gallim/www/plots/DifferentialCombination/CombinationRun2/EFT-Fitter; done
```

A few things to remember:
- ```Run2Differentials/Hgg/inputs``` relies on the presence inside ```Run2Differentials/Hgg``` of ```mus.json``` and ```correlation_matrix.json```; they are both produced with ```get_mus.py```
- about ```get_mus.py```, note that it has to be run with python 3 in an environment where the differential combination postprocessing package is installed; for what concerns the mus, it needs as input the scans (both observed and Asimov) performed in the usual way; the correlation matrix is in the file produced running the scans with ```--saveFitResult```
- both in ```inputs.py``` and ```functions.py``` the paths are hardcoded and depending on the model to fit/plot they need to be changed by hand