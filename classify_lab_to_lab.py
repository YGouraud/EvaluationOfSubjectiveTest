#Code translated from Matlab file made by Margaret Pinson

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def classify_lab_to_lab(testname, labA, labB, save):
# labA and labB list the ratings for each lab on the identical sequences,
# rated by different subjects.
# calculate the different results of conclusions by the two labs for all
# pairs of sequences.

    num_pvs = labA.shape[0]

    conclude = np.empty(5)
    conclude[0] = 0 #both tests conclude that A > B or A < B
    conclude[1] = 0 #both tests conclude that A == B
    conclude[2] = 0 #test A can tell a difference, but test B cannot
    conclude[3] = 0 #test B can tell a difference, but test A cannot
    conclude[4] = 0 #opposite ranking

    for cnt1 in range(num_pvs) :
        for cnt2 in range(cnt1+1, num_pvs):
            ans1 = (ttest_ind(labA.iloc[cnt1,:], labA.iloc[cnt2,:], nan_policy='omit')[1] <= 0.05)
            ans2 = (ttest_ind(labB.iloc[cnt1,:], labB.iloc[cnt2,:], nan_policy='omit')[1] <= 0.05)
            mosA1 = np.nanmean(labA.iloc[cnt1,:],)
            mosA2 = np.nanmean(labA.iloc[cnt2,:],)
            mosB1 = np.nanmean(labB.iloc[cnt1,:],)
            mosB2 = np.nanmean(labB.iloc[cnt2,:],)
            if ans1 == 1 and ans2 == 1 and mosA1 > mosA2 and mosB1 > mosB2 :
                conclude[0] += 1
            elif ans1 == 1 and ans2 == 1 and mosA1 < mosA2 and mosB1 < mosB2:
                conclude[0] += 1
            elif ans1 == 0 and ans2 == 0:
                conclude[1] += 1
            elif ans1 == 1 and ans2 == 0:
                conclude[2] += 1
            elif ans1 == 0 and ans2 == 1:
                conclude[3] += 1
            else: conclude[4] += 1

    print('\n\n' + testname + ', ')
    print(str(labA.shape[0]) + ' PVSs, ')
    print('Subjects: ' + str(labA.shape[1]) + ' vs ' + str(labB.shape[1]) + '\n')

    print(str(round(100*conclude[0]/sum(conclude))) + '% Agree Rank, ')
    print(str(round(100*conclude[1]/sum(conclude))) + '% Agree Tie, ')
    print(str(round(100*conclude[2]/sum(conclude))) + '% Unconfirmed (labA), ')
    print(str(round(100*conclude[3]/sum(conclude))) + '% Unconfirmed (labB), ')
    print(str(100*conclude[4]/sum(conclude)) + '% Disagree\n')

    # Giving the possibility to get the result in a table ?
    if save==True:
        result = pd.DataFrame({"Agree Rank": round(100*conclude[0]/sum(conclude)),
                               "Agree Tie": round(100*conclude[1]/sum(conclude)),
                               "Unconfirmed (labA)": round(100*conclude[2]/sum(conclude)),
                               "Unconfirmed (labB)": round(100*conclude[3]/sum(conclude)),
                               "Disagree": round(100*conclude[4]/sum(conclude), ndigits=3)}, index=["Pourcentage"])
        result.to_excel("Lab2lab.xlsx")
        print("Saved result in Lab2lab.xlsx !")
        #change the name of the file according to the datasets used ?



labA = pd.read_excel('datasets/CCRIQ_Primary_Study_data_3labs(1).xlsx', sheet_name=0, usecols='A,P:X', nrows=111, index_col=0, header=2, keep_default_na=True)
labB = pd.read_excel('datasets/CCRIQ_Primary_Study_data_3labs(1).xlsx', sheet_name=0, usecols='A,AZ:BG', nrows=111, index_col=0, header=2, keep_default_na=True)
classify_lab_to_lab("Test", labA, labB, True)
print(" ")