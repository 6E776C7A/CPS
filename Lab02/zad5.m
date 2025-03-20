clear all; close all;

[x, fs] = audioread('mowa.wav');

figure();
plot(x);
pause

% c=dct(x);
% 
% % 25% pierwszych współczynników
% disp('25% pierwszych współczynników')
% y=idct(c(1:length(c)/4));
% soundsc(y,fs)
% pause()
% 
% % 75% ostatnich współczynników
% disp('75% ostatnich współczynników')
% y=idct(c(length(c)/4:length(c)));
% soundsc(y,fs)
% pause()
% 
% % usunięcie <50
% disp('usunięcie <50')
% mniejsze = c;
% mniejsze(mniejsze < 50) = 0;
% y=idct(mniejsze);
% soundsc(y,fs)
% pause()
% 
% % usunięcie 100-200
% disp('usunięcie 100-200')
% wieksze = c;
% wieksze([100:200]) = 0;
% y=idct(wieksze);
% soundsc(y,fs)
% pause()

%zakłócenie sygnału
disp('odszumianie zakłóconego sygnału')
szum = 0.5*sin(2*pi*250/fs*(0:length(x)-1)');
sygnalszum = x + szum;
%soundsc(x,fs)
%pause(

c = dct(sygnalszum);

%odszumianie sygnału

a = round(250*2*length(c)/fs);

c(a-10:a+10)=0;

y = idct(c);

figure;
subplot(3,1,1);plot(x); title("Sygnał zakłócony przed DCT")
subplot(3,1,2);plot(c); title("Sygnał po DCT")
subplot(3,1,3);plot(y); title("Sygnał po IDCT z odszumianiem")
%soundsc(y,fs)
%pause()
