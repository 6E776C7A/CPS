import numpy as np
import scipy.io
from matplotlib import pyplot as plt

mat = scipy.io.loadmat("lab_03.mat")
x = mat[f'x_{420646%6 + 1}'].flatten()

M = 32   # prefix
N = 512  # ramka
K = 8
fs = 2.2e6  # próbkowanie

for i in range(K):
    start = i * (M + N) + M  # Początek ramki po prefiksie
    ramka = x[start:start + N]  # Pobranie ramki

    # FFT
    X = np.fft.fft(ramka)
    freq = np.fft.fftfreq(N, d=1/fs)  # Skala częstotliwości

    # Wykres
    plt.plot(freq[:N//2], np.abs(X[:N//2]))  # Tylko dodatnie częstotliwości
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda")
    plt.title(f"FFT Ramki {i+1}")
    plt.grid()
    plt.show()

    # Wykrywanie harmonicznych (progiem 90% wartości maksymalnej)
    threshold = 0.9 * np.max(np.abs(X))
    harmonic = freq[np.abs(X) > threshold]

    print(f"Ramka {i+1}: Wykryte harmoniczne:", harmonic)
