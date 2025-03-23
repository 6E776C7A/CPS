import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
import numpy as np

# Żeby nie było błędów obliczeniowych spowodowanych dokładnością Python
np.set_printoptions(precision=8, suppress=True)

# Sygnał x

N = 100
fs = 1000
f = [50, 100, 150]

# na 107 jest rozmycie z jakiegos powodu na 105 jest nie zauważalne
# f = [50, 107, 150]

# zwiększenie wszystkiego o 2.5Hz
# f = [52.5, 102.5, 152.5]
Amp = [50, 100, 150]

t = np.linspace(0, N / fs, N, endpoint=False)

x = Amp[0] * np.cos(2 * np.pi * f[0] * t) + Amp[1] * np.cos(2 * np.pi * f[1] * t) + Amp[2] * np.cos(
    2 * np.pi * f[2] * t)
plt.title('Sygnału x')
plt.grid()
plt.plot(x)
plt.show()

# Tworzenie DCT
A = np.zeros((N, N))
s = np.sqrt(2 / N)

for kolumny in range(N):
    for wiersze in range(N):
        if kolumny == 0:
            A[wiersze][kolumny] = np.sqrt(1/N)
        else:
            A[wiersze][kolumny] = s * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)

# Tworzenie IDCT
S = np.conj(A.transpose())

# Wykresy w pętli



# for i in range(N):
#     fig, axs = plt.subplots(2, 1, figsize=(6, 6))
#
#     axs[0].plot(A[i, :], label=f'Wiersz {i}')
#     axs[0].set_title('Wiersze macierzy A (DCT)')
#     axs[0].legend()
#     axs[0].grid()
#
#     axs[1].plot(S[:, i], label=f'Kolumna {i}')
#     axs[1].set_title('Kolumny macierzy S (IDCT)')
#     axs[1].legend()
#     axs[1].grid()
#
#     plt.tight_layout()
#     plt.show()

y = A @ x

plt.title("n=1:N")
plt.grid()
plt.plot(y)
plt.show()

freq = np.arange(N) * fs / N / 2

plt.title("f=(0:N-1)*fs/N/2 (normalizacja częstotliwości na osi f)")
plt.grid()
plt.plot(freq, y)
plt.show()

xs = S @ y

print(f'Czy x == xs? :\n {xs - x}')
