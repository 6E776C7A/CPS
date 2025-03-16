import numpy as np
def singen(ampl, time, freq, sampling, phase):
    t_size = int(time * sampling)
    t = np.round(np.linspace(0, time, t_size, endpoint=True),8)
    sin = np.round(ampl * np.sin(2 * np.pi * freq * t + phase), 8)
    return sin, t
