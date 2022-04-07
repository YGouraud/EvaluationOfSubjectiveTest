#Code translated from Matlab file made by Margaret Pinson

import numpy as np

def sign_diff(bew, lbin, ubin, cnt, deltaS):
    r = []
    n = 0
    for i in deltaS:
        if lbin[cnt] <= i < ubin[cnt]:
            r = np.append(r, bew[n])
        n = n + 1
    return r


def bew_to_curve_100(bew=None, deltaS=None):
    # Compute fraction of MOS comparisons that are significantly different for
    # different MOS deltas, based on Student's t-test better/equivalent/worse
    # this code is intended for a 100 point scale, instead of a 5-level scale.

    delta = 1
    bins = np.arange(0, 51, delta)

    bin_lower = bins - delta / 2
    bin_upper = bins + delta / 2
    bin_upper[len(bin_upper) - 1] = 4

    better = np.empty(len(bins))
    better[:] = np.nan

    # all data
    for cnt in range(len(bins)):
        better[cnt] = np.nanmean(sign_diff(bew, bin_lower, bin_upper, cnt, deltaS))

    print(better)

    # print results just below and just above 95%.
    # let the user choose which is closer.


    v = np.where(better > 0.95)
    tmp = v[0][0]

    print(100*better[tmp], "% at ", bins[tmp])
    tmp = tmp - 1

    if np.isnan(better[tmp]):
        tmp = tmp - 1

    print(100*better[tmp], "% at ", bins[tmp])

    return better, bins
