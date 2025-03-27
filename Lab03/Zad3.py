import numpy as np
from matplotlib import pyplot as plt

from plot import rysowanie
from scipy.signal.windows import chebwin

import matplotlib

matplotlib.use('TkAgg')

# Sygnał x

N = 100
# N = 1000

A1 = 1
A2 = 0.0001

phi1 = np.pi / 7
phi2 = np.pi / 11

fs = 1000

f1 = 100
f2 = 125

t = np.linspace(0, N / fs, N, endpoint=False)

x = A1 * np.cos(2 * np.pi * f1 * t + phi1) + A2 * np.cos(2 * np.pi * f2 * t + phi2)

widnow = np.zeros(N, dtype=np.complex128)
widnow[:int(N/2)] = 1

x_p = x * widnow
x_H = x * np.hamming(N)
x_B = x * np.blackman(N)
x_C_100 = x * chebwin(N, 100)
x_C_125 = x * chebwin(N, 125)

# DTFT
f = np.arange(0, 500.1, 0.1)

n = np.arange(N, dtype=np.complex128)

exp_term = np.exp(-1j * 2 * np.pi * f[:, None] / fs * n)
DTFT = (1 / N) * np.sum(x * exp_term, axis=1, dtype=np.complex128)
DTFT_p = (1 / N) * np.sum(x_p * exp_term, axis=1, dtype=np.complex128)
DTFT_H = (1 / N) * np.sum(x_H * exp_term, axis=1, dtype=np.complex128)
DTFT_B = (1 / N) * np.sum(x_B * exp_term, axis=1, dtype=np.complex128)
DTFT_C_100 = (1 / N) * np.sum(x_C_100 * exp_term, axis=1, dtype=np.complex128)
DTFT_C_125 = (1 / N) * np.sum(x_C_125 * exp_term, axis=1, dtype=np.complex128)

rysowanie(f, DTFT, 'Widmo DTFT', 'Częstotliwość [Hz]', 'Amplituda')

fig, axs = plt.subplots(5, 1, figsize=(8, 6), constrained_layout=True)

axs[0].plot(f, 20 * np.log10(abs(DTFT_p)), 'b-')
axs[0].set_title(f'Okno prostokątne')
axs[0].set_xlabel('Częstotliwość [Hz]')
axs[0].set_ylabel('Amplituda')

axs[1].plot(f, 20 * np.log10(abs(DTFT_H)), 'b-')
axs[1].set_title(f'Okno Hamminga')
axs[1].set_xlabel('Częstotliwość [Hz]')
axs[1].set_ylabel('Amplituda')

axs[2].plot(f, 20 * np.log10(abs(DTFT_B)), 'b-')
axs[2].set_title(f'Okno Blackmana')
axs[2].set_xlabel('Częstotliwość [Hz]')
axs[2].set_ylabel('Amplituda')

axs[3].plot(f, 20 * np.log10(abs(DTFT_C_100)), 'b-')
axs[3].set_title(f'Okno Chybyszewa 100dB')
axs[3].set_xlabel('Częstotliwość [Hz]')
axs[3].set_ylabel('Amplituda')

axs[4].plot(f, 20 * np.log10(abs(DTFT_C_125)), 'b-')
axs[4].set_title(f'Okno Chybyszewa 125dB')
axs[4].set_xlabel('Częstotliwość [Hz]')
axs[4].set_ylabel('Amplituda')

plt.show()
