import matplotlib.pyplot as plt
import numpy as np

def plot_signal(signal):
    #calls plt.plot() but does not show it
    n = len(signal)

    # f = (np.array(range(0,n-1)) * fs) / n;
    x = np.array(range(0, n))
    plt.plot(x[1:], signal[1:])
    # plt.legend("noisy", "filtered")
