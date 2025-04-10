import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Specifications
fs = 256e3  # Sampling frequency in Hz
fp = 64e3  # Passband edge in Hz
fs_stop = 128e3  # Stopband edge (fs/2) in Hz
Ap = 3  # Max passband ripple in dB
As = 40  # Min stopband attenuation in dB

# Convert to angular frequencies (rad/s)
wp = 2 * np.pi * fp
ws = 2 * np.pi * fs_stop

# Frequency array for plotting (Hz)
f = np.logspace(3, 6, 1000)  # 1 kHz to 1 MHz
w = 2 * np.pi * f  # Angular frequency for response
omega = 2 * np.pi * f


# Filter design functions
def design_and_plot_filter(filter_type, N, wp, ws, Ap=None, As=None):
    if filter_type == 'butter':
        b, a = signal.butter(N, wp, btype='low', analog=True, output='ba')
        label = f'Butterworth (N={N})'
    elif filter_type == 'cheby1':
        b, a = signal.cheby1(N, Ap, wp, btype='low', analog=True, output='ba')
        label = f'Chebyshev 1 (N={N})'
    elif filter_type == 'cheby2':
        b, a = signal.cheby2(N, As, ws, btype='low', analog=True, output='ba')
        label = f'Chebyshev 2 (N={N})'
    elif filter_type == 'ellip':
        b, a = signal.ellip(N, Ap, As, wp, btype='low', analog=True, output='ba')
        label = f'Elliptic (N={N})'

    # Frequency response
    w, h = signal.freqs(b, a, worN=omega)
    mag_dB = 20 * np.log10(np.abs(h))

    # Poles and zeros
    z, p, k = signal.tf2zpk(b, a)

    return mag_dB, z, p, label


# Determine minimum order for each filter
N_butter = signal.buttord(wp, ws, Ap, As, analog=True)[0]
N_cheby1 = signal.cheb1ord(wp, ws, Ap, As, analog=True)[0]
N_cheby2 = signal.cheb2ord(wp, ws, Ap, As, analog=True)[0]
N_ellip = signal.ellipord(wp, ws, Ap, As, analog=True)[0]

# Design filters
mag_butter, z_butter, p_butter, label_butter = design_and_plot_filter('butter', N_butter, wp, ws)
mag_cheby1, z_cheby1, p_cheby1, label_cheby1 = design_and_plot_filter('cheby1', N_cheby1, wp, ws, Ap)
mag_cheby2, z_cheby2, p_cheby2, label_cheby2 = design_and_plot_filter('cheby2', N_cheby2, wp, ws, As=As)
mag_ellip, z_ellip, p_ellip, label_ellip = design_and_plot_filter('ellip', N_ellip, wp, ws, Ap, As)

# Plot frequency response
plt.figure(figsize=(12, 6))
plt.semilogx(f, mag_butter, label=label_butter)
plt.semilogx(f, mag_cheby1, label=label_cheby1)
plt.semilogx(f, mag_cheby2, label=label_cheby2)
plt.semilogx(f, mag_ellip, label=label_ellip)
plt.axvline(fp, color='g', linestyle='--', label='Passband edge (64 kHz)')
plt.axvline(fs_stop, color='r', linestyle='--', label='Stopband edge (128 kHz)')
plt.axhline(-Ap, color='k', linestyle=':', label='-3 dB')
plt.axhline(-As, color='k', linestyle='--', label='-40 dB')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude [dB]')
plt.title('Frequency Response of Analog Low-Pass Filters')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.ylim(-100, 5)

# Plot pole-zero diagrams
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
for ax, z, p, title in zip(axs.flat,
                           [z_butter, z_cheby1, z_cheby2, z_ellip],
                           [p_butter, p_cheby1, p_cheby2, p_ellip],
                           [label_butter, label_cheby1, label_cheby2, label_ellip]):
    ax.plot(np.real(z), np.imag(z), 'go', label='Zeros')
    ax.plot(np.real(p), np.imag(p), 'rx', label='Poles')
    ax.set_title(f'Pole-Zero Plot: {title}')
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.grid(True)
    ax.legend()
    ax.axis('equal')

plt.tight_layout()
plt.show()

# Print filter orders
print(f"Butterworth order: {N_butter}")
print(f"Chebyshev 1 order: {N_cheby1}")
print(f"Chebyshev 2 order: {N_cheby2}")
print(f"Elliptic order: {N_ellip}")