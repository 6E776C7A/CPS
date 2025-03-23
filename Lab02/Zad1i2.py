import numpy as np

# Zadanie1
print("Zadanie 1!")
N = 20

maciez_cos = np.zeros((N, N))
s = np.sqrt(2 / N)

# Żeby nie było błędów obliczeniowych spowodowanych dokładnością Python
np.set_printoptions(suppress=True, precision=8, threshold=8)

for kolumny in range(N):
    for wiersze in range(N):
        if kolumny == 0:
            maciez_cos[wiersze][kolumny] = np.sqrt(1 / N)
        else:
            maciez_cos[wiersze][kolumny] = s * np.cos((np.pi * kolumny * (wiersze + 0.5)) / N)

skalar = np.zeros(N - 1)
skalar4 = np.zeros(N - 1)

for i in range(N - 1):
    skalar[i] = np.dot(maciez_cos[i], maciez_cos[i + 1])
    skalar4[i] = np.dot(maciez_cos[i], maciez_cos[i])

print(f'Wartości mnożenia skalarnego:\n {skalar, skalar4}')

# Zadanie 2
print("Zadanie 2!")
maciez_cos_transp = maciez_cos.transpose()

maciez_ide = maciez_cos_transp @ maciez_cos

print(f'Macierz identycznościowa:\n {maciez_ide}')

x = np.random.randn(N)

x = np.transpose(x)

X = maciez_cos @ x

xs = maciez_cos_transp @ X

print(f'Czy x == xs? :\n {xs - x}')

# Zadanie 2 losowe
print("Zadanie 2 losowe wartości!")

A = np.random.randn(N, N)

skalar2 = np.zeros(N - 1)
skalar3 = np.zeros(N - 1)

for i in range(N - 1):
    skalar2[i] = np.dot(A[i], A[i + 1])
    skalar3[i] = np.dot(A[i], A[i])

print(f'Wartości mnożenia skalarnego:\n {skalar2, skalar3}')

S = np.transpose(A)

I = S @ A

print(f'Macież identycznościowa: \n {I}')

X = A @ x

xs = S @ X

print(f'Czy x == xs? :\n {xs - x}')

# Zepsute DCT
print("Zadanie zepsute DCT")

A = np.zeros((N, N))
for k in range(N):
    for n in range(N):
        corrupted_k = k + 0.25  # Introduce corruption in the index
        A[k, n] = np.cos(np.pi * corrupted_k * (2 * n + 1) / (2 * N))
A = A / np.sqrt(N / 2)

skalar5 = np.zeros(N - 1)
skalar6 = np.zeros(N - 1)

for i in range(N - 1):
    skalar5[i] = np.dot(A[i], A[i + 1])
    skalar6[i] = np.dot(A[i], A[i])

print(f'Wartości mnożenia skalarnego:\n {skalar5, skalar6}')

S = np.conj(A.transpose())

t = np.linspace(0, 1, N, endpoint=False)
signal = np.sin(2 * np.pi * 5 * t) # + 0.5 * np.random.randn(N)

X = A @ signal

xs = S @ X

print(f'Czy x == xs? :\n {signal - x}')
