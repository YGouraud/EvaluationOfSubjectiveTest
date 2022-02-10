import pandas as pd

#read original data
data = pd.read_csv("./dataSource/VR_rawdata.csv")

#Check how many observers there are
observer_list = data['Observer'].unique()

#Column labels are prepared according to the number of observers(The last column is MOS)
column2 = ['MOS']
column1 = list(range(1,observer_list.shape[0]+1))
column1 = [str(x) for x in column1]
columns = column1 + column2

#Use stimulus name as line label
row = data.stimulus.copy()
row = row.sort_values()#Sort lexicographically

rows = row.reset_index()#reset the index
rows = rows.stimulus.copy().unique()#Only keep unique linemarks

#prepare an empty array
rowLen = rows.shape[0]
coluLen = observer_list.shape[0]+1
data_list = [[0.0] * coluLen] * rowLen

#create datafeame
data_return = pd.DataFrame( data_list,index = rows,columns = columns)


for index, row in data.iterrows():
    colIndex = row['Observer'].replace('user', '')
    #Since there is no observer No. 19, the people behind move forward in sequence
    #This step is not required for all datasets
    if(int(colIndex)>19):
        colIndex = str(int(colIndex)-1)
  
    rowIndex = row['stimulus']
    data_return.loc[rowIndex,colIndex] = row['score']

#Fill in the scores to the corresponding position
for index, row in data_return.iterrows():
    sum = 0
    for x in column1 :
        sum+=int(row[x])

    row['MOS'] =sum/len(column1)
   
data_return.to_csv(path_or_buf = "./dataFin/VR_rawdataF.csv");    
print(data_return)


