import pandas as pd

#Return a dataframe containing the MOS of all stimuli
def all_means(df):
    result = pd.DataFrame()
    for i in range(len(df.index)):
        a = df.index[i]
        b = df.loc[a]
        data = pd.DataFrame({b.mean()}, index=[a])
        result = result.append(data, ignore_index = False)
        print('MOS of ' + str(a) + ' : ' + str(b.mean()))

    return result
    #Must create a file with the result