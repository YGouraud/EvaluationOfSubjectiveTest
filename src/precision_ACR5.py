from ratings_to_bew import *
from bew_to_curve import *
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

def precision_ACR5(f, filename):

    B, C = ratings_to_bew('inf', f)
    D, E = bew_to_curve(B, C)


    #a.gca().yaxis.set_major_formatter(PercentFormatter(1))
    return [D,E]