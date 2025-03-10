import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from singen import singen

# Parametry sygnału
amplA = 230
freqA = 50
timeA = 1
phase = 0

# Sygnał próbkowany fs3 = 200 Hz
fs3 = 200
sin200, time200 = singen(amplA, timeA, freqA, fs3, phase)

# Nowe chwile czasowe dla fs = 10 kHz
fs = 10000
time_high_res = np.arange(0, timeA, 1/fs)

# Rekonstrukcja sygnału
t_size = len(time_high_res)  # Liczba próbek w nowej siatce czasowej
reconstructed_signal = np.zeros(t_size)  # Inicjalizacja tablicy wynikowej
Ts = 1/fs3  # Okres próbkowania

for idx in range(t_size):
    t_rec = time_high_res[idx]
    reconstructed_signal[idx] = np.sum(sin200 * np.sinc((t_rec - time200) / Ts))

# Oryginalny sygnał pseudo-analogowy
sin_analog, _ = singen(amplA, timeA, freqA, fs, phase)

# Obliczenie błędu rekonstrukcji
error = sin_analog - reconstructed_signal

# Wykresy
plt.figure(figsize=(10, 5))
plt.plot(time_high_res, sin_analog, 'b', label='Oryginalny sygnał (pseudo-analogowy)')
plt.plot(time_high_res, reconstructed_signal, 'r', linestyle='dashed', label='Zrekonstruowany sygnał')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.legend()
plt.title('Porównanie sygnałów')
plt.grid()
plt.show()

# Wykres błędu rekonstrukcji
plt.figure(figsize=(10, 3))
plt.plot(time_high_res, error, 'k', label='Błąd rekonstrukcji')
plt.xlabel('Czas [s]')
plt.ylabel('Błąd')
plt.legend()
plt.title('Błąd rekonstrukcji')
plt.grid()
plt.show()