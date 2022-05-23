from ratings_to_bew import *
from bew_to_curve import *
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def precision_ACR5(f, filename):

    B, C = ratings_to_bew('inf', f)
    D, E = bew_to_curve(B, C)

    fig = plt.figure(figsize=(10,10), dpi=80)
    a = fig.add_subplot(111)
    a.plot(E, D*100)
    a.set_title(filename)
    a.set_xlabel('DeltaS')
    a.set_ylabel('PI')
    a.grid(True, linestyle='-')
    #a.gca().yaxis.set_major_formatter(PercentFormatter(1))
    return fig