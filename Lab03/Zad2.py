import numpy as np
from matplotlib import pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
from plot import rysowanie

# Zadanie 1
N = 100

A = np.zeros((N, N), dtype=np.complex128)
W = np.exp(-1j * 2 * np.pi / N)

# Żeby nie było błędów obliczeniowych spowodowanych dokładnością Python
np.set_printoptions(suppress=True, precision=8, threshold=8)

# Macierz A transformacji DFT

for kolumny in range(N):
    for wiersze in range(N):
        A[wiersze][kolumny] = np.sqrt(1 / N) * (W ** (kolumny * wiersze))

# Sygnał x

A1 = 100
A2 = 200

phi1 = np.pi / 7
phi2 = np.pi / 11

fs = 1000

f1 = 125
f2 = 200

t = np.linspace(0, N / fs, N, endpoint=False)

x = A1 * np.cos(2 * np.pi * f1 * t + phi1) + A2 * np.cos(2 * np.pi * f2 * t + phi2)

rysowanie(t, x, 'Sygnał x', 'Czas [s]', 'Amplituda')

# oblicznie DFT

X = A @ x

fx1 = fs * np.arange(N) / N

M = np.zeros(100)

x2 = np.pad(x, (0, 100), mode='constant', constant_values=0)

X2 = np.fft.fft(x2) / (N + len(M))

fx3 = np.arange(0, 1000.25, 0.25)

fx2 = fs * np.arange(N + len(M)) / N / 2

n = np.arange(N)

exp_term = np.exp(-1j * 2 * np.pi * fx3[:, None] / fs * n)
X3 = (1 / N) * np.sum(x * exp_term, axis=1)

fig, axs = plt.subplots(3, 1, figsize=(0, 6))

axs[0].plot(fx1, X, 'o-')
axs[0].set_title(f'X1')
axs[0].set_xlabel('Częstotliwość [Hz}')
axs[0].set_ylabel('Amplituda')

axs[1].plot(fx2, X2, 'rx-')
axs[1].set_title(f'X2')
axs[1].set_xlabel('Częstotliwość [Hz}')
axs[1].set_ylabel('Amplituda')

axs[2].plot(fx3, X3, 'k-')
axs[2].set_title(f'X3')
axs[2].set_xlabel('Częstotliwość [Hz}')
axs[2].set_ylabel('Amplituda')

plt.show()

# wiekszy zakres dtft
fx3 = np.arange(-2000, 2000.25, 0.25)

n = np.arange(N)

exp_term = np.exp(-1j * 2 * np.pi * fx3[:, None] / fs * n)
X3 = (1 / N) * np.sum(x * exp_term, axis=1)

fig, axs = plt.subplots(3, 1, figsize=(0, 6))

axs[0].plot(fx1, X, 'o-')
axs[0].set_title(f'X1')
axs[0].set_xlabel('Częstotliwość [Hz}')
axs[0].set_ylabel('Amplituda')

axs[1].plot(fx2, X2, 'rx-')
axs[1].set_title(f'X2')
axs[1].set_xlabel('Częstotliwość [Hz}')
axs[1].set_ylabel('Amplituda')

axs[2].plot(fx3, X3, 'k-')
axs[2].set_title(f'X3')
axs[2].set_xlabel('Częstotliwość [Hz}')
axs[2].set_ylabel('Amplituda')

plt.show()
