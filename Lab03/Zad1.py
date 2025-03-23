import numpy as np
from plot import rysowanie

# Zadanie 1
N = 100

A = np.zeros((N, N), dtype=np.complex128)
W = np.exp(-1j*2*np.pi/N)

# Żeby nie było błędów obliczeniowych spowodowanych dokładnością Python
np.set_printoptions(suppress=True, precision=8, threshold=8)

# Macierz A transformacji DFT

for kolumny in range(N):
    for wiersze in range(N):
        A[wiersze][kolumny] = np.sqrt(1 / N) * (W**(kolumny*wiersze))

# Sygnał x

A1 = 100
A2 = 200

phi1 = np.pi/7
phi2 = np.pi/11

fs = 1000

f1 = 100
# f1 = 125
f2 = 200

t = np.linspace(0, N / fs, N, endpoint=False)

x = A1 * np.cos(2*np.pi*f1*t + phi1) + A2 * np.cos(2*np.pi*f2*t + phi2)

rysowanie(t, x, 'Sygnał x', 'Czas [s]', 'Amplituda')

# oblicznie DFT

X = A @ x

f = fs*np.arange(N)/N

rysowanie(f, X, 'Widmo sygnału x', 'Częstotliwość [Hz]', 'Amplituda')

# część rzeczywista oraz urojona
X_real = np.real(X)
X_imag = np.imag(X)
phase = np.angle(X)

rysowanie(f, X_real, 'Część rzeczywista', 'Częstotliwość [Hz]', 'Amplituda')
rysowanie(f, X_imag, 'Część urojona', 'Częstotliwość [Hz]', 'Amplituda')
rysowanie(f, abs(X), 'Moduł X', 'Częstotliwość [Hz]', 'Amplituda')
rysowanie(f, phase, 'Faza sygnału', 'Częstotliwość [Hz]', 'Faza [rad]')


# wyznaczanie macierzy B

B = np.transpose(np.conj(A))

xr = B @ X

print(f'Czy xr == x? {np.allclose(x, xr)} \n {xr-x}') # np.allclose zwraca true gdy macieże są identyczne

# używanie gotowych funkcji

X = np.fft.fft(x)

xr = np.fft.ifft(X)

print(f'Gotowa funkcja FFT \nCzy xr == x? {np.allclose(x, xr)} \n {xr-x}')

