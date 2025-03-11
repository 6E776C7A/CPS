import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)


def generate_signal(bits, fpr=16000, fc=500, T=0.1):
    samples_per_bit = int(fpr * T)
    t = np.linspace(0, T, samples_per_bit, endpoint=False)
    signal = np.concatenate([np.sin(2 * np.pi * fc * t) if bit == '0' else -np.sin(2 * np.pi * fc * t) for bit in bits])
    return signal


def play_signal(signal, fpr):
    sd.play(signal, fpr)
    sd.wait()


def main():
    name = "Janek"
    bits = text_to_bits(name)
    print(f"Bity dla '{name}': {bits}")

    signal = generate_signal(bits)

    # Rysowanie sygnału
    plt.figure(figsize=(10, 4))
    plt.plot(signal[:5000])  # Pokazujemy tylko fragment sygnału
    plt.title("Sygnał transmitujący bity ASCII")
    plt.xlabel("Próbki")
    plt.ylabel("Amplituda")
    plt.show()

    # Odtwarzanie sygnału dla różnych częstotliwości próbkowania
    for fpr in [8000, 16000, 24000, 32000, 48000]:
        print(f"Odtwarzanie dla fpr = {fpr} Hz")
        play_signal(signal, fpr)


if __name__ == "__main__":
    main()

# Szybsza transmisja bitów
# Aby przyspieszyć transmisję, można:
#
# Skrócić czas trwania pojedynczego bitu (T).
# Zastosować transmisję wielopoziomową, np.:
# Modulację amplitudy (ASK): różne amplitudy dla różnych kombinacji bitów.
# Modulację fazy (PSK): przesunięcie fazowe dla różnych bitów.
# Modulację częstotliwości (FSK): inne częstotliwości sinusoidy dla różnych bitów.
# Jeśli mamy 2 bity na raz, możemy użyć 4 poziomów amplitudy lub fazy (np. 0°, 90°, 180°, 270°), co podwoiłoby prędkość transmisji. Przy 3 bitach można użyć 8 poziomów itd.