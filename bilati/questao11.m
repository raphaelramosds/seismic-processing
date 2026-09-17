% =========================================================================
% SCRIPT PRINCIPAL: EXPERIMENTOS DE MODELAGEM SÍSMICA 1D
% =========================================================================
clear; clc; close all;

% 1. PARÂMETROS DO MEIO GEOLÓGICO (Modifique aqui para os experimentos d/e)
z = 2 .* [0.5; 0.8; 1.1; 1.6; 2.4; 2.6; 2.9; 3.0; 3.5]; % Profundidades (km)
v = 2 .* [1.5; 2.7; 2.2; 2.8; 4.5; 3.0; 2.4; 2.6; 3.6]; % Velocidades (km/s)

% 2. PARÂMETROS DA AQUISIÇÃO E DO PULSO (Modifique aqui para os experimentos e/f)
dt_amostra = 0.002;  % Intervalo de amostragem (s)
t0 = 0.025;         % Tempo do 1º zero da Ricker (s) [f_p = 1 / (sqrt(2)*pi*t0)]

% =========================================================================
% EXECUÇÃO DO FLUXO MODULARIZADO
% =========================================================================

% Etapa A: Modelo geológico -> Refletividade e Amplitudes
[samples, r_serie, a_serie, dt_acumulado] = gerar_modelo_refletividade(z, v, dt_amostra);

% Etapa B: Geração do Pulso de Ricker
[ricker, t_ricker] = gerar_pulso_ricker(t0, dt_amostra);

% Etapa C: Convolução e Modelagem do Traço Sísmico
a_ricker = conv(a_serie, ricker, 'same');

% =========================================================================
% VISUALIZAÇÃO DOS RESULTADOS
% =========================================================================
figure('Name', 'Modelagem Sísmica Modularizada', 'Color', 'w');

subplot(3,1,1);
stem(samples, r_serie, 'filled', 'MarkerSize', 3);
title('(a) Perfil de Refletividade (R)');
ylabel('Refletividade'); grid on;

subplot(3,1,2);
stem(samples, a_serie, 'r', 'filled', 'MarkerSize', 3);
title('(b) Perfil de Amplitude (a) com Perda por Transmissão');
ylabel('Amplitude'); grid on;

subplot(3,1,3);
plot(samples, a_ricker, 'b', 'LineWidth', 1.2);
title(sprintf('(c) Traço Sísmico Final (Ricker t_0 = %.3f s)', t0));
xlabel('Tempo de Ida e Volta (s)');
ylabel('Amplitude'); grid on;