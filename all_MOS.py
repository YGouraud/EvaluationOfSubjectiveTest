def all_means(df):
    for i in range(len(df.index)):
        a = df.index[i]
        b = df.loc[a]
        print('MOS of ' + str(a) + ' : ' + str(b.mean()))