% Odbiornik FM
clear all; close all;

% Parametry systemu
fs = 3.2e6;         % Częstotliwość próbkowania
N = 32e6;           % Liczba próbek (IQ)
f_center = 100e6;   % Częstotliwość strojenia (100 MHz)
bwSERV = 80e3;      % Szerokość pasma usługi FM
bwAUDIO = 16e3;     % Szerokość pasma audio mono

% Wczytanie sygnału
f = fopen('samples_100MHz_fs3200kHz.raw', 'r');
if f == -1
    error('Nie można otworzyć pliku samples_100MHz_fs3200kHz.raw');
end
s = fread(f, 2*N, 'uint8');
fclose(f);

s = s - 127;

% IQ --> complex
wideband_signal = s(1:2:end) + 1j * s(2:2:end); clear s;

% Analiza PSD i spektrogram oryginalnego sygnału
[psd_iq, freqs] = pwelch(wideband_signal, hamming(1024), 512, 1024, fs, 'power');
freqs_absolute = freqs + f_center;
figure;
subplot(2,1,1);
semilogy(freqs_absolute/1e6, psd_iq);
title('PSD oryginalnego sygnału IQ');
xlabel('Częstotliwość [MHz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(wideband_signal, hamming(1024), 512, 1024, fs, 'yaxis');
title('Spektrogram oryginalnego sygnału IQ');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Znajdowanie stacji radiowych
[peaks, locs] = findpeaks(psd_iq, 'MinPeakHeight', max(psd_iq)*0.1);
peak_freqs = freqs_absolute(locs)/1e6;
disp('Znalezione stacje radiowe (MHz) i ich siła sygnału (dB):');
for i = 1:length(peaks)
    fprintf('Stacja %d: %.4f MHz, Siła: %.2f dB\n', i, peak_freqs(i), 10*log10(peaks(i)));
end
figure;
semilogy(freqs_absolute/1e6, psd_iq);
hold on;
plot(peak_freqs, 10*log10(peaks), 'ro', 'MarkerSize', 8, 'LineWidth', 2);
title('PSD oryginalnego sygnału IQ z zaznaczonymi stacjami');
xlabel('Częstotliwość [MHz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;

% Wybór stacji
disp('Wybierz numer stacji z listy powyżej (np. 1 dla pierwszej stacji):');
station_idx = input('Numer stacji: ');
if station_idx < 1 || station_idx > length(peak_freqs)
    error('Nieprawidłowy numer stacji');
end
station_freq = peak_freqs(station_idx) * 1e6; % Częstotliwość w Hz
fc = station_freq - f_center; % Przesunięcie częstotliwości
fprintf('Wybrano stację: %.4f MHz, fc = %.4f MHz\n', station_freq/1e6, fc/1e6);

% Przesunięcie częstotliwości
wideband_signal_shifted = wideband_signal .* exp(-1j*2*pi*fc/fs*(0:N-1)');

% PSD i spektrogram po przesunięciu
[psd_shifted, freqs] = pwelch(wideband_signal_shifted, hamming(1024), 512, 1024, fs, 'power');
freqs_shifted = freqs + fc;
figure;
subplot(2,1,1);
semilogy(freqs_shifted/1e6, psd_shifted);
title(['PSD po przesunięciu (oczekiwana stacja: ', num2str(station_freq/1e6), ' MHz)']);
xlabel('Częstotliwość [MHz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(wideband_signal_shifted, hamming(1024), 512, 1024, fs, 'yaxis');
title('Spektrogram po przesunięciu częstotliwości');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Filtracja pasma usługi (Butterworth 4. rzędu, 80 kHz)
nyq = fs/2;
Wn = 80e3/nyq;
[b, a] = butter(4, Wn, 'low');
wideband_signal_filtered = filter(b, a, wideband_signal_shifted);

% PSD i spektrogram po filtracji
[psd_filtered, freqs] = pwelch(wideband_signal_filtered, hamming(1024), 512, 1024, fs, 'power');
figure;
subplot(2,1,1);
semilogy(freqs, psd_filtered);
title('PSD sygnału po filtracji pasma usługi');
xlabel('Częstotliwość [Hz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(wideband_signal_filtered, hamming(1024), 512, 1024, fs, 'yaxis');
title('Spektrogram sygnału po filtracji pasma usługi');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Decymacja do 160 kHz
decim1 = round(fs/(bwSERV*2)); % decim1 = 20
x = wideband_signal_filtered(1:decim1:end);
fs1 = fs/decim1; % fs1 = 160 kHz

% Demodulacja FM
dx = x(2:end) .* conj(x(1:end-1));
y = atan2(imag(dx), real(dx));

% PSD i spektrogram po demodulacji
[psd_demod, freqs] = pwelch(y, hamming(1024), 512, 1024, fs1, 'power');
figure;
subplot(2,1,1);
semilogy(freqs, psd_demod);
title('PSD sygnału po demodulacji FM');
xlabel('Częstotliwość [Hz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(y, hamming(1024), 512, 1024, fs1, 'yaxis');
title('Spektrogram sygnału po demodulacji FM');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Filtracja mono (0-16 kHz)
Wn_mono = bwAUDIO/(fs1/2);
[b_mono, a_mono] = butter(5, Wn_mono, 'low');
y_mono = filter(b_mono, a_mono, y);

% PSD i spektrogram po filtracji mono
[psd_mono, freqs] = pwelch(y_mono, hamming(1024), 512, 1024, fs1, 'power');
figure;
subplot(2,1,1);
semilogy(freqs, psd_mono);
title('PSD sygnału mono po filtracji');
xlabel('Częstotliwość [Hz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(y_mono, hamming(1024), 512, 1024, fs1, 'yaxis');
title('Spektrogram sygnału mono po filtracji');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Filtr antyaliasingowy (16 kHz) i decymacja do 32 kHz
Wn_aa = 16e3/(fs1/2);
[b_aa, a_aa] = butter(6, Wn_aa, 'low');
y_mono_aa = filter(b_aa, a_aa, y_mono);
decim2 = round(fs1/(bwAUDIO*2)); % decim2 = 5
ym = y_mono_aa(1:decim2:end);
fs2 = fs1/decim2; % fs2 = 32 kHz

% Sygnał bez filtru antyaliasingowego
ym_no_aa = y_mono(1:decim2:end);

% Porównanie PSD z/bez filtru antyaliasingowego
[psd_aa, freqs_aa] = pwelch(ym, hamming(1024), 512, 1024, fs2, 'power');
[psd_no_aa, freqs_no_aa] = pwelch(ym_no_aa, hamming(1024), 512, 1024, fs2, 'power');
figure;
semilogy(freqs_aa, psd_aa, 'b', 'DisplayName', 'Z filtrem antyaliasingowym');
hold on;
semilogy(freqs_no_aa, psd_no_aa, 'r', 'DisplayName', 'Bez filtru antyaliasingowego');
title('Porównanie PSD sygnału po decymacji');
xlabel('Częstotliwość [Hz]');
ylabel('Gęstość mocy [dB/Hz]');
legend;
grid on;

% De-emfaza
tau = 50e-6;
alpha = 1/(1 + fs2*tau);
b_deemph = [1-alpha, 0];
a_deemph = [1, -alpha];
ym = filter(b_deemph, a_deemph, ym);
ym_no_aa = filter(b_deemph, a_deemph, ym_no_aa);

% Redukcja szumu (filtr medianowy i wzmocnienie)
ym = medfilt1(ym, 3);
ym_no_aa = medfilt1(ym_no_aa, 3);
ym = ym * 5.0;
ym = ym / (1.001 * max(abs(ym)));
ym_no_aa = ym_no_aa * 5.0;
ym_no_aa = ym_no_aa / (1.001 * max(abs(ym_no_aa)));

% PSD i spektrogram końcowego sygnału
[psd_final, freqs] = pwelch(ym, hamming(1024), 512, 1024, fs2, 'power');
figure;
subplot(2,1,1);
semilogy(freqs, psd_final);
title('PSD końcowego sygnału po de-emfazie');
xlabel('Częstotliwość [Hz]');
ylabel('Gęstość mocy [dB/Hz]');
grid on;
subplot(2,1,2);
spectrogram(ym, hamming(1024), 512, 1024, fs2, 'yaxis');
title('Spektrogram końcowego sygnału po de-emfazie');
xlabel('Czas [s]');
ylabel('Częstotliwość [Hz]');
colormap jet;
colorbar;

% Normalizacja i odtwarzanie
ym = ym - mean(ym);
ym = ym / (1.001 * max(abs(ym)));
ym_no_aa = ym_no_aa - mean(ym_no_aa);
ym_no_aa = ym_no_aa / (1.001 * max(abs(ym_no_aa)));

disp('Odtwarzanie sygnału z filtrem antyaliasingowym...');
soundsc(ym, fs2);
pause(length(ym)/fs2 + 1);
disp('Odtwarzanie sygnału bez filtru antyaliasingowego...');
soundsc(ym_no_aa, fs2);