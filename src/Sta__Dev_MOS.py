import scipy.stats as stats
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


def select_number_of_score(rawdata, n, nbofcombination = 10):

    # Change name of columns to numbers going from 1 to the number of subject
    a = [str(i) for i in range(1, rawdata.shape[1] + 1)]
    rawdata.columns = a

    number_of_stimulus = rawdata.shape[0]
    number_of_observers = rawdata.shape[1] - 2  # 去掉列标和MOS
    # column1 = list(range(1,observer_list.shape[0]+1))

    # prepare a matrics
    newdata = np.ones((number_of_stimulus, n))#双层括号是必要的，我们只需要这个方程的第一个参数。
    datalist = []

    # generate random obsercers 产生随机数并复制数据
    observer_list = []
    combination = []
    temp = random.randint(1, number_of_observers)

    for i in range(nbofcombination):
        for j in range(n):
            while temp in observer_list:
                temp = random.randint(1, number_of_observers)
            observer_list.append(temp)
            temp = random.randint(1, number_of_observers)

        observer_list.sort()
        if observer_list not in combination:
            combination.append(observer_list.copy())
            observer_list.clear()
        else:
            observer_list.clear()
            i -= 1
            continue

  #  for i in range(nbofcombination):
    for i in range(len(combination)):
        for j in range(n):
            newdata[:, j] = rawdata[str(combination[i][j])].copy()
        datalist.append(newdata.copy())

    return datalist

#选择合适的分组数让图像显示15个点以内
def determine_groups(nbObserver):
    nbBegin = 3
    interval = int(nbObserver/10)
    lista = list(range(nbBegin,nbObserver,interval))
    if nbObserver not in lista:
        lista.append(nbObserver)
    return lista
#计算组合数
def calcul_nbcomb(nbObserver, groups):
    result = []
    nbO = np.math.factorial(nbObserver)
    for i in groups:
        nbG = np.math.factorial(i)
        nbdif = np.math.factorial(abs(i-nbObserver))
        f = int(nbO / (nbG * nbdif))
        if f < 300:
            result.append(f)
        else:
            result.append(300)
    return result

def calcul_mos(datamatrix):
    r = datamatrix.shape[0]
    c = datamatrix.shape[1]
    # print(r,c)

    sum = 0
    mos_list = []
    for i in range(r):
        for j in range(c):
            sum += datamatrix[i, j]
        mos_list.append(sum / c)
        sum = 0
    return mos_list


def calcul_deviation(datamatrix, mos):
    # print(datamatrix)
    # print(mos)
    r = datamatrix.shape[0]
    c = datamatrix.shape[1]

    sum = 0
    deviation_list = []

    for i in range(r):
        for j in range(c):
            sum += pow(datamatrix[i, j] - mos[i], 2)

        deviation_list.append(pow(sum / c, 0.5))
        sum = 0

    return deviation_list

def calcul_SD_MOS(datamatrix):
    layer = len(datamatrix)  # 记录有多少组采样
    nbstimu = datamatrix[0].shape[0]
    total = (nbstimu - 1) * nbstimu / 2
    min = 0
    max = 0
    sumnb = 0
    nbobserver = datamatrix[0].shape[1]

    for i in range(layer):
        mos = calcul_mos(datamatrix[i])
        deviation = calcul_deviation(datamatrix[i], mos)
        result = np.mean(deviation)
        sumnb += result

        if min == 0:
            min = result

        if result <min:
            min = result
        if result >max:
            max = result

    sumnb = sumnb/layer
    return [sumnb, min, max]



def standard_deviation(data):
    #origiPath = "D:/workspace/pythonWorkSpace/ptran/dataFin/IRCCyN_IVC_DIBR_Videos_Scores.csv"
    #origiPath= "C:/Users/chama/OneDrive/Bureau/4A/PTrans/Tests/EvaluationOfSubjectiveTest/datasets/CS_rawdata.csv"
    #data = pd.read_csv(origiPath) #行标不算一行
    print(data)
    nbObserver = data.shape[1] - 2
    print(nbObserver)
    #选择合适的分组数让图像显示15个点以内
    groups = determine_groups(nbObserver)
    print(groups)
    #计算组合数 计算在特定人数下有多少种抽样方式
    comb = calcul_nbcomb(nbObserver,groups)
    print(comb)

    SD_MOS = []
    for i in range(len(groups)):
        #返回的是最大排列数下， 分好组的数据
        datamatrix = select_number_of_score(data, groups[i], comb[i])
        #按分组数据计算accurary
        SD_MOS.append(calcul_SD_MOS(datamatrix))

    print(SD_MOS)

    SD_MOS = np.mat(SD_MOS)
    yy0 = SD_MOS[:, 0].T.tolist()[0]
    yy1 = SD_MOS[:, 1].T.tolist()[0]
    yy2 = SD_MOS[:, 2].T.tolist()[0]

    """
    fig, ax = plt.subplots()
    plt.xticks(groups)
    plt.fill_between(groups, y1=yy1, y2=yy2, alpha=0.3, color='c', linestyle="--")
    plt.plot(groups, yy0, "o-", markersize=2, linewidth=1.0)
    plt.xlabel('Nb of subjects')
    plt.ylabel('Standard Deviation of MOS')
    plt.show()
    """

    fig = plt.figure(figsize=(10, 10), dpi=80)
    ax = fig.add_subplot(111)
    ax.fill_between(groups, y1=yy1, y2=yy2, alpha=0.3, color='c', linestyle="--")
    ax.set_xticklabels(groups)
    ax.set_xlabel('Nb of subjects')
    ax.set_ylabel('Standard Deviation of MOS')
    ax.plot(groups, yy0, "o-", markersize=2, linewidth=1.0)

    return fig
