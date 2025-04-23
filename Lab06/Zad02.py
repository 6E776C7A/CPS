import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile, loadmat
from scipy.signal import spectrogram, bilinear, zpk2tf

# === Wczytanie pliku WAV ===
fs, sx = wavfile.read("s6.wav")

## 1. Wczytanie danych filtru analogowego
data = loadmat('butter.mat')
zeros = data['z'].flatten()
poles = data['p'].flatten()
k = data['k'].item()

## 2. Konwersja do postaci cyfrowej przy użyciu transformacji biliniowej
b, a = bilinear(*zpk2tf(zeros, poles, k), fs=fs)

# === Własna funkcja filtrująca ===
def my_filter(b, a, x):
    y = np.zeros_like(x, dtype=np.float64)
    buffer_x = np.zeros(len(b))
    buffer_y = np.zeros(len(a) - 1)

    for n in range(len(x)):
        buffer_x[1:] = buffer_x[:-1]
        buffer_x[0] = x[n]

        y_n = np.dot(b, buffer_x) - np.dot(a[1:], buffer_y)
        y[n] = y_n

        buffer_y[1:] = buffer_y[:-1]
        buffer_y[0] = y_n

    return y

# === Filtracja sygnału ===
sy_filt = my_filter(b, a, sx)

# === Kompensacja opóźnienia filtra ===
delay = int((len(b) - 1) // 2)
sy_filt_comp = np.roll(sy_filt, -delay)

# === Spektrogramy ===
f1, t1, Sxx1 = spectrogram(sx, fs, nperseg=4096, noverlap=4096 - 512)
f2, t2, Sxx2 = spectrogram(sy_filt_comp, fs, nperseg=4096, noverlap=4096 - 512)

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.pcolormesh(t1, f1, 20 * np.log10(Sxx1), shading='gouraud')
plt.title("Spektrogram przed filtracją")
plt.xlabel("Czas [s]")
plt.ylabel("Częstotliwość [Hz]")
plt.ylim(600, 1700)
plt.colorbar(label='Amplituda [dB]')

plt.subplot(1, 2, 2)
plt.pcolormesh(t2, f2, 20 * np.log10(Sxx2), shading='gouraud')
plt.title("Spektrogram po filtracji (my_filter)")
plt.xlabel("Czas [s]")
plt.ylabel("Częstotliwość [Hz]")
plt.ylim(600, 1700)
plt.colorbar(label='Amplituda [dB]')

plt.tight_layout()
plt.show()

# === Wykres w dziedzinie czasu ===
plt.figure(figsize=(12, 4))
plt.plot(sx, label="Oryginalny")
plt.plot(sy_filt_comp, '--', label="Filtrowany (my_filter)")
plt.xlabel("Próbka")
plt.ylabel("Amplituda")
plt.title("Porównanie sygnału przed i po filtracji")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
