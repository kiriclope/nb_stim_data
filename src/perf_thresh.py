from christos_errors import get_drift_off_on
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from bootstrap import my_boots_ci

sns.set_context("poster")
sns.set_style("ticks")
plt.rc("axes.spines", top=False, right=False)

golden_ratio = (5**.5 - 1) / 2
width = 7.5
matplotlib.rcParams['figure.figsize'] = [width, width * golden_ratio ]

pal = [sns.color_palette("tab10")[0], sns.color_palette("tab10")[1]]

if __name__ == "__main__":

    THRESH_LIST = np.linspace(0, 20, 20)
    TASK = "first"
    CUT_OFF = [0, 0]
    IF_CORRECT = False

    drift_off_list = []
    drift_on_list = []

    per_off_list = []
    per_on_list = []

    drift_off = get_drift_off_on('off', TASK, 360, CUT_OFF, IF_CORRECT)
    drift_on = get_drift_off_on('on', TASK, 360, CUT_OFF, IF_CORRECT)

    for thresh in THRESH_LIST:

        off = np.nansum(np.abs(drift_off)<thresh) / drift_off.shape[0]
        drift_off_list.append(off)
        on = np.nansum(np.abs(drift_on)<thresh) / drift_on.shape[0]
        drift_on_list.append(on)

        _, ci_off = my_boots_ci(np.abs(drift_off)<thresh, np.nansum, verbose=0, n_samples=1000)
        _, ci_on = my_boots_ci(np.abs(drift_on)<thresh, np.nansum, verbose=0, n_samples=1000)

        per_off_list.append(ci_off[0] / drift_off.shape[0])
        per_on_list.append(ci_on[0] / drift_on.shape[0])


    per_off_list = np.array(per_off_list).T
    per_on_list = np.array(per_on_list).T

    plt.plot(THRESH_LIST, drift_off_list, color=pal[0])
    plt.plot(THRESH_LIST, drift_on_list, color=pal[1])

    plt.fill_between(THRESH_LIST, drift_off_list-per_off_list[0], drift_off_list+per_off_list[1], alpha=0.2)

    plt.fill_between(THRESH_LIST, drift_on_list-per_on_list[0], drift_on_list+per_on_list[1], alpha=0.2)

    plt.xlabel('Threshold (°)')
    plt.ylabel('Performance')
    plt.yticks([0, .25, .5, .75, 1])

