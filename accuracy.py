import scipy.stats as stats
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


def select_number_of_score(rawdata, n, nbofcombination = 10):
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
        if f < 5:
            result.append(f)
        else:
            result.append(5)
    return result

#计算accuracy
def calcul_Accuracy(datamatrix):
    layer = len(datamatrix)  # 记录有多少组采样
    nbstimu = datamatrix[0].shape[0]
    total = (nbstimu-1)*nbstimu/2
    nb_pairs_sig_diff = 0
    min = 0
    max = 0
    sumnb = 0
    nbobserver = datamatrix[0].shape[1]

    for i in range(layer):
        for j in range(nbstimu-1):
            x = datamatrix[i][j]
            for k in range(j+1, nbstimu):
                y = datamatrix[0][k]
                if((x == y).all()):
                    continue
                result = stats.wilcoxon(x, y, correction=True, alternative='two-sided')
                if result[1] <= 0.05:
                    nb_pairs_sig_diff += 1
       # print("layer:" + str(i)+"            "+str(nb_pairs_sig_diff))
        if min == 0:
          #  print("(((((((((((((((((((((((")
            min = nb_pairs_sig_diff

        if nb_pairs_sig_diff < min:
            min = nb_pairs_sig_diff

        if nb_pairs_sig_diff > max:
            max = nb_pairs_sig_diff

        sumnb += nb_pairs_sig_diff
        nb_pairs_sig_diff =0

    accmin = min/total
    accmax = max / total
    acc = sumnb/ layer / total
    return [nbobserver, acc, accmin, accmax]



def accuracy(data):
    #origiPath = "D:/workspace/pythonWorkSpace/ptran/dataFin/IRCCyN_IVC_DIBR_Videos_Scores.csv"
    #data = pd.read_csv(origiPath) #行标不算一行
    #print(data)
    nbObserver = data.shape[1] - 2
    #print(nbObserver)
    #选择合适的分组数让图像显示15个点以内
    groups = determine_groups(nbObserver)
    print(groups)

    #计算组合数 计算在特定人数下有多少种抽样方式
    comb = calcul_nbcomb(nbObserver,groups)
    print(comb)

    #按照分组数计算置信区间向量
    ACC = []
    for i in range(len(groups)):
        print("number: " + str(i))
        #返回的是最大排列数下， 分好组的数据
        datamatrix = select_number_of_score(data, groups[i], comb[i])
        #按分组数据计算accurary
        ACC.append(calcul_Accuracy(datamatrix))


    ACC = np.mat(ACC)
    yy0 = ACC[:,1].T.tolist()[0]
    yy1 = ACC[:,2].T.tolist()[0]
    yy2 = ACC[:,3].T.tolist()[0]

    fig, ax = plt.subplots()
    plt.xticks(groups)
    plt.fill_between(groups, y1 = yy1, y2= yy2, alpha = 0.5, color = 'c', linestyle = "--")
    plt.plot(groups,yy0,"o-",markersize=2,linewidth=1.0)
    plt.xlabel('Nb of subjects')
    plt.ylabel('Accuracy')

    plt.show()

