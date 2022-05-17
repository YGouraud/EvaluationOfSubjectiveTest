from ratings_to_bew import *
from bew_to_curve import *
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def precision_ACR5(f, filename):

    B, C = ratings_to_bew('inf', f)
    D, E = bew_to_curve(B, C)
    plt.plot(E, D)
    plt.title(filename)
    plt.xlabel('DeltaS')
    plt.ylabel('PI')
    plt.grid(True, linestyle='-')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.show()