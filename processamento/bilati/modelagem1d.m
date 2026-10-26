% experimento modelagem sismica 1D
clear; clc; close all;

% parametros do meio geologico 
z = [0.5; 0.8; 1.1; 1.6; 2.4; 2.6; 2.9; 3.0; 3.5]; % Profundidades (km)
v = 2*[1.5; 2.7; 2.2; 2.8; 4.5; 3.0; 2.4; 2.6; 3.6]; % Velocidades (km/s)

% prametros da aquisicao e do pulso
dt_amostra = 0.002;  % Intervalo de amostragem (s)
t0 = 0.025;         % Tempo do 1º zero da Ricker (s) [f_p = 1 / (sqrt(2)*pi*t0)]

% Modelo geologico -> Refletividade e Amplitudes
[samples, r_serie, a_serie, dt_acumulado] = gerar_modelo_refletividade(z, v, dt_amostra);

% Geracao do Pulso de Ricker
[ricker, t_ricker] = gerar_pulso_ricker(t0, dt_amostra);

% Convolucao e Modelagem do trraco sismico
a_ricker = conv(a_serie, ricker, 'same');

% visualizacao dos resultados
figure('Name', 'Modelagem Sismica Modularizada', 'Color', 'w');

subplot(3,1,1);
stem(samples, r_serie, 'filled', 'MarkerSize', 3);
title('(a) Perfil de Refletividade (R)');
ylabel('Refletividade'); grid on;

subplot(3,1,2);
stem(samples, a_serie, 'r', 'filled', 'MarkerSize', 3);
title('(b) Perfil de Amplitude (a) com Perda por Transmissao');
ylabel('Amplitude'); grid on;

subplot(3,1,3);
plot(samples, a_ricker, 'b', 'LineWidth', 1.2);
title(sprintf('(c) Traco Sismico Final (Ricker t_0 = %.3f s)', t0));
xlabel('Tempo de Ida e Volta (s)');
ylabel('Amplitude'); grid on;