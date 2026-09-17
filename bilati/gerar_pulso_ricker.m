function [ricker, t_ricker] = gerar_pulso_ricker(t0, dt_amostra)
    % Frequência de pico derivada do parâmetro t0 (primeiro zero)
    fp = 1 / (sqrt(2) * pi * t0);
    
    % Janela temporal simétrica do pulso (-100 ms a +100 ms)
    t_ricker = -0.1 : dt_amostra : 0.1;
    
    % Equação analítica da Ricker
    term = (pi * fp * t_ricker).^2;
    ricker = (1 - 2 * term) .* exp(-term);
end