import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def MyCorrelation(x, y):
    lenX = len(x)
    lenY = len(y)
    correlation = np.zeros(lenX + lenY - 1)  # Długość pełnej korelacji

    # Obliczamy korelację poprzez sumowanie przesuniętych wartości
    for k in range(lenX + lenY - 1):
        sum_val = 0
        for l in range(max(0, k + 1 - lenY), min(k, lenX - 1) + 1):
            sum_val += x[l] * y[k - l]

        correlation[k] = sum_val

    return correlation


adsl = sio.loadmat('adsl_x.mat')
x = adsl['x'].flatten()

M = 32
N = 512
K = 4
# Dla gotowej funkcji
for i in range(K):
    # iterowanie od 0
    prefix = x[(i+1)*N - M-1:(i+1)*N-1]
    correlation = np.correlate(x, prefix, 'full')
    treshold = max(correlation) * 0.99
    poczatki_prefixow = find_peaks(correlation, treshold)
    poczatki_prefixow_x = poczatki_prefixow[0] - M + 1
    print(poczatki_prefixow_x)

# Dla własnej funkcji
for i in range(K):
    prefix = x[(i+1)*N - M-1:(i+1)*N-1]
    correlation = MyCorrelation(x, prefix)
    treshold = max(correlation) * 0.99
    poczatki_prefixow = find_peaks(correlation, treshold)
    poczatki_prefixow_x = poczatki_prefixow[0] - M + 1
    print(poczatki_prefixow_x)
