import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter, freqz, spectrogram, tf2zpk
from numpy.fft import fft, fftfreq

# === Funkcje pomocnicze ===

def plot_fft(signal, fs, title="FFT"):
    N = len(signal)
    freqs = fftfreq(N, 1/fs)
    fft_vals = np.abs(fft(signal))
    plt.figure(figsize=(10, 4))
    plt.plot(freqs[:N // 2], 20 * np.log10(fft_vals[:N // 2] + 1e-10))
    plt.title(title)
    plt.xlabel("Częstotliwość [Hz]")
    plt.ylabel("Amplituda [dB]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_spectrogram(signal, fs, title="Spektrogram"):
    f, t, Sxx = spectrogram(signal, fs=fs, nperseg=1024, noverlap=768)
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t, f, 20 * np.log10(Sxx + 1e-10), shading='gouraud')
    plt.title(title)
    plt.xlabel("Czas [s]")
    plt.ylabel("Częstotliwość [Hz]")
    plt.colorbar(label="Amplituda [dB]")
    plt.tight_layout()
    plt.show()

def design_lowpass_filter(cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return b, a

def plot_filter_response(b, a, fs):
    w, h = freqz(b, a, worN=8000)
    plt.figure(figsize=(10, 4))
    plt.plot(fs * 0.5 * w / np.pi, 20 * np.log10(np.abs(h) + 1e-10))
    plt.title('Charakterystyka amplitudowa filtru [dB]')
    plt.xlabel('Częstotliwość [Hz]')
    plt.ylabel('Wzmocnienie [dB]')
    plt.grid()
    plt.tight_layout()
    plt.show()

    z, p, _ = tf2zpk(b, a)
    plt.figure(figsize=(5, 5))
    plt.scatter(np.real(z), np.imag(z), marker='o', label='Zera')
    plt.scatter(np.real(p), np.imag(p), marker='x', label='Bieguny')
    plt.axhline(0, color='gray')
    plt.axvline(0, color='gray')
    plt.title('Zera i bieguny na płaszczyźnie zespolonej')
    plt.xlabel('Re')
    plt.ylabel('Im')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# === Wczytywanie plików ===

fs1, voice = wavfile.read("porche.wav")
fs2, bird = wavfile.read("bird.wav")

print(fs1)
print(fs2)

assert fs1 == fs2, "Częstotliwości próbkowania muszą być identyczne!"
fs = fs1

# Mono i wyrównanie długości
voice = voice if voice.ndim == 1 else voice[:, 0]
bird = bird if bird.ndim == 1 else bird[:, 0]
min_len = min(len(voice), len(bird))
voice = voice[:min_len]
bird = bird[:min_len]

# Normalizacja
voice = voice / np.max(np.abs(voice))
bird = bird / np.max(np.abs(bird))

# Sumowanie
combined = voice + bird
combined = combined / np.max(np.abs(combined))

# === Widma oryginalnych i sumy ===
plot_fft(voice, fs, "FFT - Mowa")
plot_spectrogram(voice, fs, "Spektrogram - Mowa")

plot_fft(bird, fs, "FFT - Ptak")
plot_spectrogram(bird, fs, "Spektrogram - Ptak")

plot_fft(combined, fs, "FFT - Sygnał zsumowany")
plot_spectrogram(combined, fs, "Spektrogram - Sygnał zsumowany")

# === Projektowanie filtru IIR ===
cutoff = 400  # Odcinamy ptoka
b, a = design_lowpass_filter(cutoff, fs, order=4)
plot_filter_response(b, a, fs)

# === Filtracja sygnału ===
filtered = lfilter(b, a, combined)

# === Analiza przefiltrowanego ===
plot_fft(filtered, fs, "FFT - Po filtrze (mowa)")
plot_spectrogram(filtered, fs, "Spektrogram - Po filtrze (mowa)")

# === Zapis do WAV ===
from scipy.io.wavfile import write
write("filtered_output.wav", fs, (filtered * 32767).astype(np.int16))
print("Zapisano plik: filtered_output.wav")
