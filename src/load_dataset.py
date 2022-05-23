import pandas
import os

def load_dataset():
    dataset_dict = dict()
    print(os.getcwd())

    path = os.getcwd() + r'\datasets'
    list_of_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root,file))

    for name in list_of_files:
        #add putting data into pandas dataframe
        ft = name.split(".").pop()
        ft_name = name.split("\\").pop()
        ft_name = ft_name.split(".")[0]

        if ft == 'csv':
            dataset_dict[ft_name] = pandas.read_csv(name, index_col=0, keep_default_na=True)
        elif ft == "xls" or ft == "xlsx":
            dataset_dict[ft_name] = pandas.read_excel(name, index_col=0, sheet_name=1, header=1,
                               keep_default_na=True)
        elif ft == 'json':
            dataset_dict[ft_name] = pandas.read_json(name)
        elif ft == 'xml':
            dataset_dict[ft_name] = pandas.read_xml(name)

    return dataset_dict