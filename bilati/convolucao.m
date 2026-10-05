% CONVOLUCAO
% Exercicio 9: convolucao de dois sinais discretos e finitos.
    
clear;
clc;
close all;

% Exemplo com sinais nulos: confirma que o resultado tem m + n - 1
% amostras.
n = 10;
m = 15;

xn = zeros(1, n);
xm = zeros(1, m);

resultado = conv(xn, xm);

fprintf('xn tem %d elementos\n', numel(xn));
fprintf('xm tem %d elementos\n', numel(xm));
fprintf('Tamanho xn * xm: %d\n', numel(resultado));

% Sinais nao triviais para visualizar o formato da convolucao.
xn_ex = zeros(1, n);
xn_ex(3:5) = [1, 2, 1];

xm_ex = zeros(1, m);
xm_ex(1:3) = [1, -1, 0.5];

resultado_ex = conv(xn_ex, xm_ex);

figure('Name', 'Convolucao de sinais discretos', 'Color', 'w');

subplot(3, 1, 1);
stem(0:numel(xn_ex)-1, xn_ex, 'filled');
title(sprintf('xn (m=%d amostras)', numel(xn_ex)));
xlabel('indice da amostra');
grid on;

subplot(3, 1, 2);
stem(0:numel(xm_ex)-1, xm_ex, 'filled');
title(sprintf('xm (n=%d amostras)', numel(xm_ex)));
xlabel('indice da amostra');
grid on;

subplot(3, 1, 3);
stem(0:numel(resultado_ex)-1, resultado_ex, 'filled');
title(sprintf('xn * xm (m+n-1=%d amostras)', numel(resultado_ex)));
xlabel('indice da amostra');
grid on;

fprintf('Tamanho esperado (m+n-1): %d\n', numel(xn_ex) + numel(xm_ex) - 1);
fprintf('Tamanho obtido: %d\n', numel(resultado_ex));
