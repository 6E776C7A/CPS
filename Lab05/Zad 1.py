import matplotlib.pyplot as plt
import matplotlib
from scipy.signal import zpk2tf

matplotlib.use('TkAgg')
import numpy as np

# Dane do projektowania filtru pasywnego układu LTI

# bieguny
P = np.array(
    [-0.5 + 1j * 9.5, -0.5 - 1j * 9.5, -1 + 1j * 10, -1 - 1j * 10, -0.5 + 1j * 10.5, -0.5 - 1j * 10.5],
    dtype=np.complex64)

# miejsca zerowe

Z = np.array(
    [1j * 5, -1j * 5, 1j * 15, -1j * 15],
    dtype=np.complex64)

# Wyświetlanie zer i biegunów na płaszczyznie
plt.figure(figsize=(6, 6))
plt.plot(np.real(Z), np.imag(Z), 'bo', label='Zera')
plt.plot(np.real(P), np.imag(P), 'r*', label='Bieguny')
plt.grid()
plt.axhline(0, color='black', linestyle='--', lw=1)
plt.axvline(0, color='black', linestyle='--', lw=1)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.title('Miejsca zerowe i biegunowe')
plt.legend()
plt.show()

w = np.linspace(0, 20, 1000)

S = 1j * w

# Wyzanczanie współczynników licznika i mianownika
a = np.poly(P)
b = np.poly(Z)

# Wyznaczanie transmitancji
H = np.polyval(b, S) / np.polyval(a, S)

# Ch-Cz
plt.figure(figsize=(6, 6))
plt.plot(w, np.abs(H), label='|H(s)|')
plt.grid()
plt.axhline(0, color='black', linestyle='--', lw=1)
plt.axvline(0, color='black', linestyle='--', lw=1)
plt.xlabel('Częstotliość')
plt.ylabel('Apmplituda')
plt.title('Ch-Cz')
plt.legend()
plt.show()

# Ch-Cz dB
plt.figure(figsize=(6, 6))
plt.plot(w, 20 * np.log10(np.abs(H)), label='20*log10(|H(s)|)')
plt.grid()
plt.axhline(0, color='black', linestyle='--', lw=1)
plt.axvline(0, color='black', linestyle='--', lw=1)
plt.xlabel('Częstotliość')
plt.ylabel('Apmplituda')
plt.title('Ch-Cz')
plt.legend()
plt.show()

# Sprawdzenie wzmocnienia w paśmie przepustowym i tłumienia w zaporowym
max_gain = np.max(np.abs(H))
min_gain = np.min(np.abs(H))
max_atten_db = np.max(20 * np.log10(np.abs(H)))
min_atten_db = np.min(20 * np.log10(np.abs(H)))

print('Max gain: ' + str(max_gain))
print('Max gain: ' + str(min_gain))
print('Max Attenuation dB: ' + str(max_atten_db))
print('Min Attenuation dB: ' + str(min_atten_db))

# Normalizacja transmitancji

w0 = 1j * 10

H_w0 = np.polyval(b, w0) / np.polyval(a, w0)

current_gain = np.abs(H_w0)
# k = current_gain ** (1 / (len(Z) - len(P)))
# P_new = P * k
# Z_new = Z * k

# Wyznaczanie transmitancji
H_normalized = H / current_gain

# Ch-Cz
plt.figure(figsize=(6, 6))
plt.plot(w, np.abs(H_normalized), label='|H(s)| normalized')
plt.grid()
plt.axhline(0, color='black', linestyle='--', lw=1)
plt.axvline(0, color='black', linestyle='--', lw=1)
plt.xlabel('Częstotliość')
plt.ylabel('Apmplituda')
plt.title('Ch-Cz')
plt.legend()
plt.show()

# Ch-FC

H_phase = np.angle(H_normalized, deg=True)

plt.figure(figsize=(6, 6))
plt.plot(w, H_phase, label='|H(s)| normalized')
plt.grid()
plt.axhline(0, color='black', linestyle='--', lw=1)
plt.axvline(0, color='black', linestyle='--', lw=1)
plt.xlabel('Częstotliość')
plt.ylabel('Faza')
plt.title('Ch-FC')
plt.legend()
plt.show()
