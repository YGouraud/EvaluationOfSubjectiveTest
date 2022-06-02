import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

#从原数rawdata里， 以不重复的方式抽取nbofcombination次 含有n个观察者的组合
#返回值是是nbofcombination层数据，每一层是n个观察者对所有刺激的评分
def select_number_of_score(rawdata, n, nbofcombination = 10):

    #Change name of columns to numbers going from 1 to the number of subject
    a = [str(i) for i in range(1, rawdata.shape[1]+1)]
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

        if observer_list not in combination:
            observer_list.sort()
            combination.append(observer_list.copy())
            observer_list.clear()
        else:
            observer_list.clear()
            i -= 1
            continue

    for i in range(nbofcombination):
        for j in range(n):
            newdata[:, j] = rawdata[str(combination[i][j])].copy()
        datalist.append(newdata.copy())

    return datalist


def calcul_CI(datamatrix):
    layer = len(datamatrix) #记录有多少组采样
    nbobserver = pow(datamatrix[0].shape[1], 0.5)

    CIs = []
    for i in range(layer):
        mos = calcul_mos(datamatrix[i])
        standard_deviation = calcul_deviation(datamatrix[i], mos)
        standard_deviation = [i * 1.96 for i in standard_deviation]
        CI = [j / nbobserver for j in standard_deviation]
        CIs.append(CI.copy())
    CIS = np.average(CIs, axis=0)
    return CIS

    # mos = calcul_mos(datamatrix)
    # standard_deviation = calcul_deviation(datamatrix, mos)
    # standard_deviation = [i * 1.96 for i in standard_deviation]
    # nbobserver = pow(datamatrix.shape[1], 0.5)
    # CI = [i / nbobserver for i in standard_deviation]
    # return CI


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

def determine_groups(nbObserver):
    nbGroup = 10
    memgroup = []

    if nbObserver <= 50:
        interval = 5
    else:
        interval = nbObserver / nbGroup

    x = interval
    while (x < nbObserver):
        memgroup.append(x)
        x += interval

    if x == nbObserver:
        memgroup.append(nbObserver)
    elif abs(nbObserver - x) < interval / 2:
        memgroup.append(nbObserver)
    else:
        memgroup.pop()
        memgroup.append(nbObserver)
    return memgroup

def calcul_nbcomb(nbObserver, groups):
    result = []
    nbO = np.math.factorial(nbObserver)
    for i in groups:
        nbG = np.math.factorial(i)
        nbdif = np.math.factorial(abs(i-nbObserver))
        f = int(nbO / (nbG * nbdif))
        if f < 100:
            result.append(f)
        else:
            result.append(100)
    return result


#读取数据
def CI(data):

    #data = pd.read_csv(origiPath) #行标不算一行
    print(data)
    nbObserver = data.shape[1] - 2
    print(nbObserver)
    #决定分组数
    groups = determine_groups(nbObserver)
    print(groups)

    #计算组合数
    comb = calcul_nbcomb(nbObserver,groups)
    print(comb)

    #按照分组数计算置信区间向量
    CIS = []
    for i in range(len(groups)):
        #返回的是最大排列数下， 分好组的数据
        datamatrix = select_number_of_score(data, groups[i], comb[i])
        #按分组数据计算CI
     #   CI = calcul_CI(datamatrix)
        CIS.append(calcul_CI(datamatrix))

    fig = plt.figure(figsize=(8, 8), dpi=80)
    ax = fig.add_subplot(111)
    ax.set_title('CONFIDENCE INTERVAL', fontsize=20)  # 标题
    ax.set_xticklabels(groups)  # 每个箱子的名字
    ax.set_xlabel('group size')  # 设置x轴名称
    ax.set_ylabel('CI width')  # 设置y轴名称
    ax.boxplot(CIS, patch_artist=True, boxprops={'color': 'lightslategray', 'facecolor': 'c'})
    #plt.show()

    """
    fig, ax = plt.subplots()
    plt.title('CONFIDENCE INTERVAL',fontsize=20) #标题
    ax.set_xticklabels(groups) #每个箱子的名字
    ax.set_xlabel('group size') #设置x轴名称
    ax.set_ylabel('CI width') #设置y轴名称
    plt.boxplot(CIS, patch_artist = True, boxprops = {'color':'lightslategray','facecolor':'c'})
    plt.show()
    #print(CIS)
    """

    return fig

