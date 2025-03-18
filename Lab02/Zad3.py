import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use('TkAgg')
import numpy as np

#Żeby nie było błędów obliczeniowych spowodowanych dokładnością Python
np.set_printoptions(precision=8, suppress=True)

# Sygnał x

N = 100
fs = 1000
# f = [50, 100, 150]

# na 107 jest rozmycie z jakiegos powodu na 105 jest nie zauważalne
f = [50, 107, 150]

# zwiększenie wszystkiego o 2.5Hz
# f = [52.5, 102.5, 152.5]
Amp = [50, 100, 150]

t = np.linspace(0, N/fs, N, endpoint=False)

x = Amp[0] * np.sin(2 * np.pi * f[0]*t) + Amp[1] * np.sin(2 * np.pi * f[1]*t) + Amp[2] * np.sin(2 * np.pi * f[2]*t)
plt.plot(x)
plt.show()

# Tworzenie DCT
A = np.zeros((N, N))
s = np.sqrt(2 / N)

for kolumny in range(N):
    for wiersze in range(N):
        if kolumny == 0:
            A[wiersze][kolumny] = (s * 1 / np.sqrt(2)) * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)
        else:
            A[wiersze][kolumny] = s * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)

# Tworzenie IDCT
S = np.conj(A.transpose())

# # Wykresy w pętli
# plt.ion()
# fig, ax = plt.subplots()
# for i in range(N):
#     ax.clear()
#     ax.plot(A[i, :], label=f'Wiersz {i} macierzy A (DCT)')
#     ax.plot(S[:, i], label=f'Kolumna {i} macierzy S (IDCT)')
#     ax.legend()
#     plt.draw()
#     plt.pause(1)
#
# plt.ioff()
# plt.show()

y = A @ x

plt.title("n=1:N")
plt.grid()
plt.plot(y)
plt.show()

freq = np.arange(N) * fs/N/2

plt.title("f=(0:N-1)*fs/N/2 (normalizacja częstotliwości na osi f)")
plt.grid()
plt.plot(freq, y)
plt.show()

xs = S @ y

print(f'Czy x == xs? :\n {xs - x}')

