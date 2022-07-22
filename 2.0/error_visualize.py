import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk
import seaborn as sns


def visualize(jdata: str, ifile: str):

    error = json.load(open(jdata, 'r'))

    intra = error['intra']
    inter = error['inter']

    intra_unit = np.ones(len(intra)) / len(intra)
    inter_unit = np.ones(len(inter)) / len(inter)

    plt.hist(intra, bins=10, weights=intra_unit, rwidth=0.7, alpha=0.7)
    plt.hist(inter, bins=20, weights=inter_unit, rwidth=0.7, alpha=0.7)
    plt.xticks([0.25, 0.5, 0.75])
    plt.legend(['Intra', 'Inter'])

    plt.gca().yaxis.set_major_formatter(mtk.PercentFormatter(1))
    plt.savefig(ifile)


def visualize_The(jdata: str, ifile: str, bin_range: float, bin_width: float, xmax: float, ymax: float):

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()

    error = json.load(open(jdata, 'r'))

    intra = error['intra']
    inter = error['inter']

    sns.set(style="darkgrid", rc={
            'axes.edgecolor': 'black', 'axes.linewidth': 0.25})
    sns.histplot(intra, binrange=(0, bin_range), binwidth=bin_width,
                 ax=ax, kde=False, stat='probability', label='Intra-class', color='blue')
    sns.histplot(inter, binrange=(0, bin_range), binwidth=bin_width,
                 ax=ax, kde=False, stat='probability', label='Inter-class', color='crimson')

    plt.legend()
    plt.xlabel("Hamming Distance Threshold")
    plt.grid(True)

    ax.set_xlim([0, xmax])
    ax.set_ylim([0, ymax])

    plt.savefig(ifile)
