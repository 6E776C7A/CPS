import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
import matplotlib

matplotlib.use('TkAgg')

x = read('mowa.wav')

signal = x[1]
fs = x[0]

plt.title(f'Original Signal with : {fs}Hz sampling frequency.')
plt.plot(signal)
plt.show()

N = 256

# Tworzenie DCT
A = np.zeros((N, N))
s = np.sqrt(2 / N)

for kolumny in range(N):
    for wiersze in range(N):
        if kolumny == 0:
            A[wiersze][kolumny] = (s * 1 / np.sqrt(2)) * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)
        else:
            A[wiersze][kolumny] = s * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)

M = np.zeros((10, 256))
poczatkiM = list()

L = [2000, 4000, 12000, 13000, 17500, 18000, 20000, 25000, 33000, 35000]

for i in range(10):
    M[i] = signal[L[i]:L[i] + N]

y = np.zeros((10, 256))
f = np.arange(N) * fs / N / 2

for i in range(10):
    y[i] = A @ M[i]

    fig, axs = plt.subplots(2, 1, figsize=(0, 6))

    axs[0].plot(M[i])
    axs[0].set_title(f' {i + 1} k-ty element xk dla próbki w przedziale próbki {L[i]} do {L[i] + 256}')
    axs[0].set_xlabel('Próbki')
    axs[0].set_ylabel('Amplituda')

    axs[1].plot(f, y[i])
    axs[1].set_title(f' {i + 1} k-ty element yk(f) dla próbki w przedziale próbki {L[i]} do {L[i] + 256}')
    axs[1].set_xlabel('Częstotliwość [Hz]')
    axs[1].set_ylabel('Amplituda')

    plt.show()
