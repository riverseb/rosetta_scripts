import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rmsd_vs_score import scatter_plot
import argparse

def main(data, x, y, style=None, hue=None):
    df = pd.read_csv(data, sep=',', header=0)
    scatter_plot(df, x, y, style, hue)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str, help="data file")
    parser.add_argument("x", type=str, help="x label")
    parser.add_argument("y", type=str, help="y label")
    parser.add_argument("--style", type=str, default=None, help="column to use for style")
    parser.add_argument("--hue", type=str, default=None, help="column to use for hue")
    args = parser.parse_args()
    main(**vars(args))