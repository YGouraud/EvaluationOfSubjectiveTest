#Code translated from Matlab file made by Margaret Pinson

import numpy as np
from scipy.stats import ttest_ind

def ratings_to_bew(max_subjects, ratings):
    # take raw subjective ratings, one media per row, subjects in columns
    # for each pair of media, compute and return:
    #    bew = 0 for equivalent, 1 for better or worse
    #    deltaS = distance between the two medias' MOSs
    # set max_subjects to inf normally
    # can set to smaller number to limit the number of subjects considered in
    # this calculation.
    # THE RATING MUST BE ACR [1..5]

    # num is the number of subjects
    num = ratings.shape[1]

    if not (max_subjects.isnumeric()):
        print('max_subjects must be a number, >= 1, inf suggested as a default')
        # choose at most number of subjects available
        max_subjects = num
    else:
        if max_subjects > num:
            max_subjects = num

    # bew and deltaS are vectors of length equal to the sum of every positive number up to num
    bew = np.empty((num*(num-1))//2)
    bew[:] = np.nan
    deltaS = np.empty((num*(num-1))//2)
    deltaS[:] = np.nan
    curr = 0

    for cnt1 in np.arange(0, num):
        for cnt2 in np.arange(cnt1 + 1, num):
            # a Student t-test is realised between the ratings of two stimuli
            if (ttest_ind(ratings.iloc[cnt1,:max_subjects], ratings.iloc[cnt2,:max_subjects], nan_policy='omit')[1] <= 0.05):
                bew[curr] = 1
            else:
                bew[curr] = 0
            deltaS[curr] = abs(np.nanmean(ratings.iloc[cnt1,:max_subjects]) - np.nanmean(ratings.iloc[cnt2,:max_subjects]))
            curr = curr + 1

    return bew, deltaS