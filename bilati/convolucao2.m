% CONVOLUCAO2
% Exercicio 10: interpretacao de filtros de derivada por convolucao.

clear;
clc;
close all;

delta_t = 0.004;  % 4 ms, valor comum de dt em dados sismicos
fpeak = 20;        % Hz

% Equivalente a np.arange(-0.128, 0.128, delta_t).
t = -0.128:delta_t:(0.128 - delta_t);
f = ricker(t, fpeak);

figure('Name', 'Wavelet Ricker', 'Color', 'w');
plot(t, f, 'LineWidth', 1.2);
title('f: wavelet Ricker (sinal de entrada)');
xlabel('tempo (s)');
grid on;

% Filtros de diferencas finitas centradas.
p = (1 / (2 * delta_t)) * [1, 0, -1];
q = (1 / delta_t^2) * [1, -2, 1];

% O argumento ''same'' mantem o tamanho do sinal de entrada f.
g = conv(f, p, 'same');
h = conv(f, q, 'same');

figure('Name', 'Filtros de derivada', 'Color', 'w');

subplot(3, 1, 1);
plot(t, f, 'b', 'LineWidth', 1.2);
title('f (sinal original - wavelet de Ricker)');
grid on;

subplot(3, 1, 2);
plot(t, g, 'r', 'LineWidth', 1.2);
title('g = f * p  (aproximacao da 1a derivada de f)');
grid on;

subplot(3, 1, 3);
plot(t, h, 'k', 'LineWidth', 1.2);
title('h = f * q  (aproximacao da 2a derivada de f)');
xlabel('tempo (s)');
grid on;

function y = ricker(t, fpeak)
    a = (pi * fpeak .* t).^2;
    y = (1 - 2 * a) .* exp(-a);
end
