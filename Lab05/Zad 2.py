import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import lti, impulse, step

matplotlib.use('TkAgg')

# częstotliwość pulsacji 3dB
w_3db = 2 * np.pi * 100

# Rząd filtru
N = [2, 4, 6, 8]

# Położenie biegunów dla każdego N
P = [[] for _ in range(len(N))]
mianownik = [[] for _ in range(len(N))]

# Częstotliwości dla analizy
f = np.linspace(1, 1000, 1000)
omega = 2 * np.pi * f

# Inicjalizacja wykresów
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

for i in range(len(N)):
    # Obliczanie biegunów
    P[i] = [w_3db * np.exp(1j * np.pi * (0.5 + 1/(2*N[i]) + (k-1)/N[i])) for k in range(1, N[i]+1)]

    # Obliczanie współczynników mianownika filtru (wielomian z biegunami)
    mianownik[i] = np.poly(P[i])

    # Obliczanie H(jω) na wszystkich częstotliwościach
    H = 1 / np.polyval(mianownik[i], 1j * omega)

    # Charakterystyka amplitudowa (w dB)
    axs[0].semilogx(f, 20 * np.log10(np.abs(H)), label=f'N={N[i]}')

    # Charakterystyka fazowa (w stopniach)
    axs[1].plot(f, np.angle(H, deg=True), label=f'N={N[i]}')

# Opis wykresu amplitudowego
axs[0].set_title('Charakterystyka amplitudowa |H(jω)| (skala logarytmiczna)')
axs[0].set_xlabel('Częstotliwość [Hz]')
axs[0].set_ylabel('Amplituda [dB]')
axs[0].legend()
axs[0].grid(True, which='both')

# Opis wykresu fazowego
axs[1].set_title('Charakterystyka fazowa ∠H(jω)')
axs[1].set_xlabel('Częstotliwość [Hz]')
axs[1].set_ylabel('Faza [stopnie]')
axs[1].legend()
axs[1].grid(True)

# Zastosowanie układu wykresów
plt.tight_layout()
plt.show()

# Tworzymy funkcję transferową
system = lti(1, mianownik[1])

# Obliczanie odpowiedzi impulsowej
time, y_impulse = impulse(system)

# Obliczanie odpowiedzi na skok jednostkowy
time, y_step = step(system)

# Rysowanie wyników
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Odpowiedź impulsowa
axs[0].plot(time, y_impulse)
axs[0].set_title('Odpowiedź impulsowa filtru Butterwortha (N=4)')
axs[0].set_xlabel('Czas [s]')
axs[0].set_ylabel('Amplituda')
axs[0].grid(True)

# Odpowiedź na skok jednostkowy
axs[1].plot(time, y_step)
axs[1].set_title('Odpowiedź na skok jednostkowy filtru Butterwortha (N=4)')
axs[1].set_xlabel('Czas [s]')
axs[1].set_ylabel('Amplituda')
axs[1].grid(True)

plt.tight_layout()
plt.show()