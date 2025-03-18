import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.fftpack import dct, idct

x = read('nagranie.wav')

signal = x[1]
fs = x[0]

plt.title(f'Original Signal with : {fs}Hz sampling frequency and {len(signal)} samples.')
plt.plot(signal)
plt.grid()
plt.show()

# sd.play(signal, fs)
# sd.wait()

transformata = dct(signal, type=2, norm="ortho")

plt.title(f'Transformed Signal with DCT2')
plt.stem(transformata)
plt.grid()
plt.show()

# transformataCzesci = dct(signal[0:int(len(signal)/2)], norm="ortho")
#
# plt.title(f'Transformed half of Signal with DCT2')
# plt.stem(transformataCzesci)
# plt.grid()
# plt.show()
#
# # 25% współczyniików
# print('Pierwsze nagranie')
# y25 = idct(transformata[:int(len(transformata)/4)], norm='ortho')
# sd.play(y25, fs)
# sd.wait()
# plt.title('IDCT 25% pierwszych współczynników')
# plt.stem(y25)
# plt.grid()
# plt.show()
#
# # 75% współczynników
# print('Drugie nagranie')
# y75 = idct(transformata[int(len(transformata)/4):int(len(transformata))], norm='ortho')
# plt.title('IDCT 75% ostatnich współczynników')
# plt.stem(y25)
# plt.grid()
# plt.show()
# sd.play(y75, fs)
# sd.wait()
#
print('W teori 1:1')
y = idct(transformata, norm='ortho')
plt.title('IDCT sygnału C')
plt.stem(y)
plt.grid()
plt.show()
# sd.play(y, fs)
# sd.wait()
#
# # wyzerowanie mniejszych niż 50
#
# print('IDCT < 50')
# mniejsze = transformata
# mniejsze[mniejsze < 50] = 0
#
# y = idct(mniejsze, norm='ortho')
# plt.title('Wyzerowanie <50')
# plt.stem(y)
# plt.grid()
# plt.show()
# sd.play(y, fs)
# sd.wait()
#
# # wyzerowanie 100 do 200
# print('IDCT 100-200')
# wieksze = transformata
# wieksze[100:200] = 0
#
# y = idct(wieksze, norm='ortho')
# plt.title('Wyzerowanie 100:200')
# plt.stem(y)
# plt.grid()
# plt.show()
# sd.play(y, fs)
# sd.wait()

# zakłucanie sygnału
signal = signal + 0.5*np.sin(2*np.pi*250/fs*np.transpose(np.arange(len(signal))))
recon = dct(signal, norm='ortho')
recon[250] = 0
y = idct(recon, norm='ortho')

print('Syngał zakłucony')
plt.title('Sygnał zakłucony')
plt.stem(y)
plt.grid()
plt.show()
# sd.play(y, fs)
# sd.wait()
