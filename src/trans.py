import numpy as np
import pandas as pd

def transform_data(data, stimuli, observers, score):
    """From the 3 necessary attributes given by the user,
    transform the dataset into a formalized form who can
    be used by our statistical tools"""

    nameOfStimulus = stimuli
    nameOfObserver = observers
    #prefix_observers = "Obs"
    nameOfScore = score

    # Check how many observers there are
    observer_list = data[nameOfObserver].unique()

    # Column labels are prepared according to the number of observers(The last column is MOS)
    column1 = observer_list
    column2 = ['MOS']
    columns = np.append(column1, column2)

    # Use stimulus name as line label
    row = data[nameOfStimulus].copy()

    """To avoid problems if different labs used different path, we only retrieve
        the name of the file"""

    i = 0
    for stimulus in data[nameOfStimulus]:
        split_path(stimulus, row, i)
        i += 1

    #row = row.sort_values()  # Sort lexicographically
    #row = row.reset_index()  # reset the index
    row = row.unique()  # Only keep unique linemarks


    # prepare an empty array
    rowLen = row.shape[0]
    colLen = columns.shape[0] #add 1 for the "MOS" column
    data_list = [[0.0] * colLen] * rowLen

    # create dataframe
    data_return = pd.DataFrame(data_list, index=row, columns=columns)
    # Fill in the scores to the corresponding position
    for index, row in data.iterrows():
        colIndex = row[nameOfObserver]
        rowIndex = row[nameOfStimulus]
        rowIndex = split_path(rowIndex)
        data_return.loc[rowIndex, colIndex] = row[nameOfScore]

    # Fill in the MOS
    for index, row in data_return.iterrows():
        sum = 0
        count = 0
        for x in column1:
            if int(row[x]) != 0:
                sum += int(row[x])
                count += 1
            else:
                continue

        row['MOS'] = sum / count

    # reset Column labels
    column1 = list(range(1, observer_list.shape[0]+1))
    column1 = [str(x) for x in column1]
    column2 = ['MOS']
    columns = np.append(column1, column2)
    #data_return.columns = columns

    #data_return.to_csv(path_or_buf=finalPath)
    #print(data_return)

    return data_return

def split_path(stimulus, row = None, i = None):
    if i is not None and row is not None:
        if stimulus.split("/")[0] != stimulus:
            row[i] = stimulus.split("/").pop()
        elif stimulus.split("\\")[0] != stimulus:
            row[i] = stimulus.split("\\").pop()
        return
    else:
        if stimulus.split("/")[0] != stimulus:
            stimulus = stimulus.split("/").pop()
        elif stimulus.split("\\")[0] != stimulus:
            stimulus = stimulus.split("\\").pop()
        return stimulus