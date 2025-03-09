import numpy as np


def singen(ampl, time, freq, sampling, phase):
    t_size = int(time * sampling)
    t = np.linspace(0, time, t_size, endpoint=True)
    sin = ampl * np.sin(2 * np.pi * freq * t + phase)
    return sin, t
