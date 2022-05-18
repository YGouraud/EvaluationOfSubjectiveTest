import pandas as pd


def transform_data(stimuli, observers, scores):

    if stimuli is None or observers is None or scores is None:
        return None
    else:
        # Check how many observers there are
        observers = observers.iloc[:, 0]
        observer_list = observers.iloc[:, 0].unique(observers)
        observer_list = pd.unique(observers)

        # Column labels are prepared according to the number of observers(The last column is MOS)
        column2 = ['MOS']
        column1 = list(range(1, observer_list.shape[0] + 1))
        column1 = [str(x) for x in column1]
        columns = column1 + column2

        # Use stimulus name as line label
        row = stimuli.copy()
        # row = row.sort_values() Sort lexicographically

        # rows = row.reset_index()#reset the index
        rows = row.unique()  # Only keep unique linemarks

        # prepare an empty array
        rowLen = row.shape[0]
        coluLen = observer_list.shape[0] + 1
        data_list = [[0.0] * coluLen] * rowLen

        # create dataframe
        data_return = pd.DataFrame(data_list, index=row, columns=column1)

        k = 0
        for i in rows:
            for j in column1:
                data_return.loc[i, j] = scores[k]
                k += 1

        """
        #Fill in the scores to the corresponding position
        for index, row in data_return.iterrows():
            sum = 0
            for x in column1:
                sum += int(row[x])
    
            row['MOS'] = sum/len(column1)
        """

        print(data_return)

        return data_return
