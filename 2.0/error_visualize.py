
import json, numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk


def visualize(jdata: str, ifile: str):

    error = json.load(open(jdata, 'r'))

    intra = error['intra']
    inter = error['inter']

    intra_unit = np.ones(len(intra)) / len(intra)
    inter_unit = np.ones(len(inter)) / len(inter)

    plt.hist(intra, bins = 10, weights = intra_unit, rwidth = 0.7, alpha = 0.7)
    plt.hist(inter, bins = 20, weights = inter_unit, rwidth = 0.7, alpha = 0.7)
    plt.xticks([0.25, 0.5, 0.75])
    plt.legend(['Intra', 'Inter'])

    plt.gca().yaxis.set_major_formatter(mtk.PercentFormatter(1))
    plt.savefig(ifile)