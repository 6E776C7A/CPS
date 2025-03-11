import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def cross_correlation(x, y):
    lenX = len(x)
    lenY = len(y)
    correlation = [0] * (lenX + lenY - 1)

    y = y[::-1]

    # Obliczanie korelacji
    for k in range(lenX + lenY - 1):
        sum_val = 0
        for l in range(lenX):
            if 0 <= k - l < lenY:
                sum_val += x[l] * y[k - l]
        correlation[k] = sum_val

    return correlation[::-1]


adsl = sio.loadmat('adsl_x.mat')
x = adsl['x'].flatten()

M = 32
N = 512
K = 4
y = np.arange(0, 2080, 1)
# Dla gotowej funkcji
for i in range(K):
    # iterowanie od 0
    prefix = x[(i+1)*N - M-1:(i+1)*N-1]
    correlation = np.correlate(x, prefix, 'full')
    plt.plot(y, correlation)
    plt.show()
    poczatki_prefixow = np.argmax(correlation)
    poczatki_prefixow_x = poczatki_prefixow - M + 1
    print(poczatki_prefixow_x)

# Dla własnej funkcji
for i in range(K):
    prefix = x[(i+1)*N - M-1:(i+1)*N-1]
    correlation = cross_correlation(prefix, x)
    plt.plot(y, correlation)
    plt.show()
    poczatki_prefixow = np.argmax(correlation)
    poczatki_prefixow_x = poczatki_prefixow - M + 1
    print(poczatki_prefixow_x)
