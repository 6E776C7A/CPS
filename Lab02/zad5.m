[x, fs] = audioread('mowa.wav');

c=dct(x);

% 25% pierwszych współczynników
disp('25% pierwszych współczynników')
y=idct(c(1:length(c)/4));
soundsc(y,fs)
pause()

% 75% ostatnich współczynników
disp('75% ostatnich współczynników')
y=idct(c(length(c)/4:length(c)));
soundsc(y,fs)
pause()

% usunięcie <50
disp('usunięcie <50')
mniejsze = c;
mniejsze(mniejsze < 50) = 0;
y=idct(mniejsze);
soundsc(y,fs)
pause()

% usunięcie 100-200
disp('usunięcie 100-200')
wieksze = c;
wieksze([100:200]) = 0;
y=idct(wieksze);
soundsc(y,fs)
pause()

%zakłócenie sygnału
disp('odszumianie zakłóconego sygnału')
x=x+0.5*sin(2*pi*250/fs*(0:length(x)-1)');

c = dct(x);

c(250)=0;

y = idct(c);
soundsc(y,fs)
pause()