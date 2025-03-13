import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from singen import singen
from scipy.signal import periodogram

# A
amplA = 230
timeA = 0.1
freqA = 50
phase = 0
sin10k, time10k = singen(amplA, timeA, freqA, pow(10, 3), phase)
sin500, time500 = singen(amplA, timeA, freqA, 500, phase)
sin200, time200 = singen(amplA, timeA, freqA, 200, phase)

plt.plot(time10k, sin10k, 'b-', label="10kHz")
plt.plot(time500, sin500, 'r-o', label="500Hz")
plt.plot(time200, sin200, 'k-x', label="200Hz")
plt.legend()
plt.title("A")
plt.grid()
plt.show()

# B

amplB = 1
timeB = 1
freqB = 50
phase = 0

sin10k, time10k = singen(amplB, timeB, freqB, pow(10, 3), phase)
sin51, time51 = singen(amplB, timeB, freqB, 51, phase)
sin50, time50 = singen(amplB, timeB, freqB, 50, phase)
sin49, time49 = singen(amplB, timeB, freqB, 49, phase)
plt.plot(time10k, sin10k, 'b-', label="10khz")
plt.plot(time51, sin51, 'g-o', label="51Hz")
plt.plot(time50, sin50, 'r-o', label="50Hz")
plt.plot(time49, sin49, 'k-o', label="49Hz")
plt.legend()
plt.title("B.1")
plt.grid()
plt.show()

# sin10k, time10k = singen(amplB, timeB, freqB, pow(10, 3), phase)
sin26, time26 = singen(amplB, timeB, freqB, 26, phase)
sin25, time25 = singen(amplB, timeB, freqB, 25, phase)
sin24, time24 = singen(amplB, timeB, freqB, 24, phase)
# plt.plot(time10k, sin10k, 'b-', label="10khz")
plt.plot(time26, sin26, 'g-o', label="26Hz")
plt.plot(time25, sin25, 'r-o', label="25Hz")
plt.plot(time24, sin24, 'k-o', label="24Hz")
plt.legend()
plt.title("B.2")
plt.grid()
plt.show()

# C sinus

fs = 100
timeC = 1
freqC = 300
amplC = 1
phase = 0
sinuses = []

for i, freq in enumerate(range(0, freqC+5, 5)):
    sin, time = singen(amplC, timeC, freq, fs, phase)
    sinuses.append((time, sin))
    # plt.plot(time, sin, 'g-o', label=f'{freq}Hz')
    # plt.legend()
    # plt.title(f'Sinus Iteration: {i} Frequency: {freq}Hz  ')
    # plt.grid()
    # plt.show()

plt.figure()
plt.subplot(3,1,1)
plt.plot(sinuses[1][0], sinuses[1][1], 'g-', label="5Hz")
plt.plot(sinuses[21][0], sinuses[21][1], 'r-', label="105Hz")
plt.plot(sinuses[41][0], sinuses[41][1], 'k-', label="205Hz")
plt.legend()
plt.title("Porówanie sinus 5,105,205.")
plt.grid()


plt.subplot(3,1,2)
plt.plot(sinuses[19][0], sinuses[19][1], 'g-', label="95Hz")
plt.plot(sinuses[39][0], sinuses[39][1], 'r-', label="195Hz")
plt.plot(sinuses[59][0], sinuses[59][1], 'k-', label="295Hz")
plt.legend()
plt.title("Porówanie sinus 95,195,295.")
plt.grid()


plt.subplot(3,1,3)
plt.plot(sinuses[19][0], sinuses[19][1], 'g-', label="95Hz")
plt.plot(sinuses[21][0], sinuses[21][1], 'r-', label="105Hz")
plt.legend()
plt.title("Porówanie sinus 95,105.")
plt.grid()
plt.show()

# C cosinus

fs = 100
timeC = 1
freqC = 300
amplC = 1
phase = np.pi/2
cosinuses = []

for i, freq in enumerate(range(0, freqC+5, 5)):
    sin, time = singen(amplC, timeC, freq, fs, phase)
    cosinuses.append((time, sin))
    #plt.plot(time, sin, 'g-o', label=f'{freq}Hz')
    #plt.legend()
    #plt.title(f'Cosinus Iteration: {i} Frequency: {freq}Hz  ')
    #plt.grid()
    #plt.show()

plt.figure()
plt.subplot(3,1,1)
plt.plot(cosinuses[1][0], cosinuses[1][1], 'g-', label="5Hz")
plt.plot(cosinuses[21][0], cosinuses[21][1], 'r-', label="105Hz")
plt.plot(cosinuses[41][0], cosinuses[41][1], 'k-', label="205Hz")
plt.legend()
plt.title("Porówanie cosinus 5,105,205.")
plt.grid()


plt.subplot(3,1,2)
plt.plot(cosinuses[19][0], cosinuses[19][1], 'g-', label="95Hz")
plt.plot(cosinuses[39][0], cosinuses[39][1], 'r-', label="195Hz")
plt.plot(cosinuses[59][0], cosinuses[59][1], 'k-', label="295Hz")
plt.legend()
plt.title("Porówanie cosinus 95,195,295.")
plt.grid()


plt.subplot(3, 1, 3)
plt.plot(cosinuses[19][0], cosinuses[19][1], 'g-', label="95Hz")
plt.plot(cosinuses[21][0], cosinuses[21][1], 'r-', label="105Hz")
plt.legend()
plt.title("Porówanie cosinus 95,105.")
plt.grid()
plt.show()

# D 1
matplotlib.use('TkAgg')
fs1 = pow(10, 3)
fb = 50
fm = 1
df = 5
b = df/(fm*2*np.pi)
time = 1
t_size = int(time*fs1)
t = np.linspace(0, time, t_size, endpoint=True)
sin = b*np.sin(2*np.pi*fm*t)
SFM = np.sin(2*np.pi*fb*t - b*np.cos(2*np.pi*fm*t))
sin_dm = np.sin(2*np.pi*fb*t)
plt.plot(t, sin, label="Modulujący")
plt.plot(t, SFM, label="Po modulacji")
#plt.plot(t, sin_dm, label="Przed modulacji")
plt.legend()
plt.grid()
plt.show()

# D 2

fs2 = 25
t_size = int(time*fs2)
t2 = np.linspace(0, time, t_size, endpoint=True)
SFM2 = np.sin(2*np.pi*fb*t2 - b*np.cos(2*np.pi*fm*t2))
error = SFM - np.interp(t, t2, SFM2)
plt.plot(t2, SFM2, label="Mniejsze próbkowanie 25Hz")
plt.plot(t, SFM, label="Próbkowanie 10kHz")
plt.legend()
plt.grid()
plt.show()
plt.plot(t, error, label="Błędy modulacji")
plt.legend()
plt.grid()
plt.show()

# D 3

freq1, power1 = periodogram(SFM, fs1)
freq2, power2 = periodogram(SFM2, fs2)

plt.plot(freq1, power1, label="Widmowa gęstość przed zmianą próbkowania")
plt.xlim(0, 100)
plt.legend()
plt.grid()
plt.show()
plt.plot(freq2, power2, label="Widmowa gęstść mocy po zmianie próbkowania")
plt.legend()
plt.grid()
plt.show()

