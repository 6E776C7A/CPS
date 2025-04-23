import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy.signal import bilinear, zpk2tf, freqs, freqz, lfilter

## 1. Wczytanie danych filtru analogowego
data = loadmat('butter.mat')
zeros = data['z'].flatten()
poles = data['p'].flatten()
k = data['k'].item()

## Parametry
fs = 16000  # Częstotliwość próbkowania [Hz]
fp_dol = 1189  # Dolna częstotliwość graniczna [Hz]
fp_gor = 1229  # Górna częstotliwość graniczna [Hz]

## 2. Konwersja do postaci cyfrowej przy użyciu transformacji biliniowej
b, a = bilinear(*zpk2tf(zeros, poles, k), fs=fs)

## 3. Charakterystyka amplitudowo-częstotliwościowa
# Obliczenie charakterystyki filtru analogowego
num, den = zpk2tf(zeros, poles, k)
w_analog, h_analog = freqs(num, den, worN=2048)
f_analog = w_analog / (2 * np.pi)

# Obliczenie charakterystyki filtru cyfrowego
w_digital, h_digital = freqz(b, a, worN=2048, fs=fs)
f_digital = w_digital

# Normalizacja charakterystyk
h_analog_norm = np.abs(h_analog) / np.max(np.abs(h_analog))
h_digital_norm = np.abs(h_digital) / np.max(np.abs(h_digital))

# Wykres charakterystyk
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.semilogx(f_analog, 20 * np.log10(h_analog_norm), 'b', linewidth=1.5, label='Analogowy')
plt.semilogx(f_digital, 20 * np.log10(h_digital_norm), 'r', linewidth=1.5, label='Cyfrowy')
plt.axvline(fp_dol, color='k', linestyle='--', label='Dolna częstotliwość graniczna')
plt.axvline(fp_gor, color='k', linestyle='--', label='Górna częstotliwość graniczna')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [dB]')
plt.title('Charakterystyka amplitudowo-częstotliwościowa')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(f_analog, h_analog_norm, 'b', linewidth=1.5, label='Analogowy')
plt.plot(f_digital, h_digital_norm, 'r', linewidth=1.5, label='Cyfrowy')
plt.axvline(fp_dol, color='k', linestyle='--')
plt.axvline(fp_gor, color='k', linestyle='--')
plt.xlim(1000, 1400)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda [znormalizowana]')
plt.title('Zbliżenie w skali liniowej')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

## 4. Generacja i filtracja sygnału testowego
# Generacja sygnału testowego
t = np.arange(0, 1, 1 / fs)
f1 = 1209  # Pierwsza składowa [Hz]
f2 = 1272  # Druga składowa [Hz]
x = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)


# Implementacja własna filtracji (realizacja równania różnicowego)
def my_filter(b, a, x):
    y = np.zeros_like(x)
    N = len(b)
    M = len(a)
    buffer_x = np.zeros(N)
    buffer_y = np.zeros(M - 1)

    for n in range(len(x)):
        # Przesuwanie bufora wejściowego
        buffer_x = np.roll(buffer_x, 1)
        buffer_x[0] = x[n]

        # Obliczenie wyjścia
        y[n] = np.sum(b * buffer_x) - np.sum(a[1:] * buffer_y)

        # Przesuwanie bufora wyjściowego
        buffer_y = np.roll(buffer_y, 1)
        buffer_y[0] = y[n]

    return y


y_own = my_filter(b, a, x)

# Filtracja za pomocą funkcji lfilter()
y_lfilter = lfilter(b, a, x)

# Porównanie wyników
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, y_own, 'b', label='Własna implementacja')
plt.plot(t, y_lfilter, 'r--', label='Funkcja lfilter()')
plt.xlabel('Czas [s]')
plt.ylabel('Amplituda')
plt.title('Porównanie sygnałów wyjściowych')
plt.legend()
plt.xlim(0, 0.02)
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, np.abs(y_own - y_lfilter))
plt.xlabel('Czas [s]')
plt.ylabel('Różnica amplitud')
plt.title('Różnica między implementacjami')
plt.xlim(0, 0.02)
plt.grid(True)

plt.tight_layout()
plt.show()


# Analiza w dziedzinie częstotliwości
def compute_fft(signal, fs):
    N = len(signal)
    fft_result = np.fft.fft(signal) / N
    freq = np.fft.fftfreq(N, 1 / fs)[:N // 2]
    return freq, 2 * np.abs(fft_result[:N // 2])


freq, X = compute_fft(x, fs)
_, Y_own = compute_fft(y_own, fs)
_, Y_lfilter = compute_fft(y_lfilter, fs)

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(freq, X, 'b', label='Wejście')
plt.plot(freq, Y_own, 'r', label='Wyjście (własna implementacja)')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.title('Widmo sygnału wejściowego i wyjściowego')
plt.legend()
plt.xlim(1100, 1300)
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(freq, Y_own, 'b', label='Własna implementacja')
plt.plot(freq, Y_lfilter, 'r--', label='Funkcja lfilter()')
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Amplituda')
plt.title('Porównanie widm wyjściowych')
plt.legend()
plt.xlim(1100, 1300)
plt.grid(True)

plt.tight_layout()
plt.show()