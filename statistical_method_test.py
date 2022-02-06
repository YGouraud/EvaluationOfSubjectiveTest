import pandas as pd
from ratings_to_bew import *
from bew_to_curve import *
import matplotlib.pyplot as plt



df1 = pd.read_excel('datasets/IRCCyN_IVC_1080i_Database_Score.xls', sheet_name=0, usecols='B:AD', index_col=0, header=1, keep_default_na=True)
df2 = pd.read_excel('datasets/IRCCyN_IVC_1080i_Database_Score.xls', sheet_name=1, usecols='B:AO', index_col=0, header=1, keep_default_na=True)
df3 = pd.read_excel('datasets/IRCCyN_IVC_DIBR_Videos_Scores.xls', sheet_name=1, usecols='A:AG', index_col=0, header=1, keep_default_na=True)

# Give the MOS of all videos
def all_means(df):
    for i in range(len(df.index)):
        a = df.index[i]
        b = df.loc[a]
        print('MOS of ' + str(a) + ' : ' + str(b.mean()))

#all_means(df)

'''
print(df3)
B, C = ratings_to_bew('inf',df3)
D, E = bew_to_curve(B,C)
plt.plot(E,D)
plt.show()
'''

