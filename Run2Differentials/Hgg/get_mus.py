"""
To be run with python3 and https://github.com/maxgalli/DifferentialCombinationPostProcess
"""
import argparse
import os
import json
import ROOT
from itertools import product

from differential_combination_postprocess.scan import DifferentialSpectrum
from differential_combination_postprocess.matrix import MatricesExtractor
from differential_combination_postprocess.utils import (
    setup_logging,
    extract_from_yaml_file,
)


def parse_arguments():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--input-dir",
        type=str,
        default="inputs",
        help="Directory where the .root files with 'limit' trees are stored",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory where output files will be stored",
    )

    parser.add_argument(
        "--corr-matrix-file", type=str, help="File with the correlation matrix"
    )

    parser.add_argument("--debug", action="store_true", help="Print debug messages")

    return parser.parse_args()


def main(args):
    if args.debug:
        logger = setup_logging(level="DEBUG")
    else:
        logger = setup_logging(level="INFO")

    observable = "smH_PTH"

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

    values = {}
    for category in ["Hgg", "Hgg_asimov"]:
        logger.info(f"Category {category}")
        values[category] = {}
        categories_numbers = [
            directory
            for directory in os.listdir(args.input_dir)
            if directory.startswith(f"{category}-")
        ]
        category_input_dirs = [
            f"{args.input_dir}/{directory}" for directory in categories_numbers
        ]

        diff_spectrum = DifferentialSpectrum(
            observable, category, pois, category_input_dirs, from_singles=False
        )

        for poi in pois:
            values[category][poi] = {}
            values[category][poi]["bestfit"] = diff_spectrum.scans[poi].minimum[0]
            values[category][poi]["Up01Sigma"] = diff_spectrum.scans[poi].up68_unc
            values[category][poi]["Down01Sigma"] = diff_spectrum.scans[poi].down68_unc

        logger.info(f"Values for {category}: {values[category]}")

    final_dct = {}
    for key in values["Hgg"]:
        final_dct[key] = {}
        final_dct[key]["bestfit"] = values["Hgg"][key]["bestfit"]
        final_dct[key]["Up01Sigma"] = values["Hgg"][key]["Up01Sigma"]
        final_dct[key]["Down01Sigma"] = values["Hgg"][key]["Down01Sigma"]
        final_dct[key]["Up01SigmaExp"] = values["Hgg_asimov"][key]["Up01Sigma"]
        final_dct[key]["Down01SigmaExp"] = values["Hgg_asimov"][key]["Down01Sigma"]
        final_dct[key]["merged"] = False
    logger.info(f"Final dictionary: {final_dct}")

    with open(f"{args.output_dir}/mus.json", "w") as f:
        json.dump(final_dct, f)

    # Now get the correlation matrix
    if args.corr_matrix_file:
        me = MatricesExtractor(pois)
        me.extract_from_roofitresult(args.corr_matrix_file, "fit_mdf")
    matrix_values = {}
    for poi in pois:
        matrix_values[poi] = {}
    for pair, value in zip(
        product(pois, repeat=2), me.matrices["rfr_correlation"].flatten()
    ):
        matrix_values[pair[0]][pair[1]] = float(value)
    logger.info(f"Matrix values: {matrix_values}")
    with open(f"{args.output_dir}/correlation_matrix.json", "w") as f:
        json.dump(matrix_values, f)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
