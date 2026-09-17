function [samples, r_serie, a_serie, esp_acumulado] = gerar_modelo_refletividade(z, v, dt_amostra)
    % Espessuras e tempos de viagem de ida e volta por camada
    dz = diff([0; z(:)]);
    esp = (2 * dz) ./ v(:);
    esp_acumulado = cumsum(esp);
    
    % Cálculo dos coeficientes de reflexão nas interfaces
    nr = length(v) - 1;
    r = (v(2:end) - v(1:end-1)) ./ (v(2:end) + v(1:end-1));
    
    % Cálculo das perdas por transmissão acumuladas
    transmissao_fatores = 1 - r.^2;
    perda_acumulada = cumprod(transmissao_fatores);
    
    a = zeros(size(r));
    a(1) = r(1);
    a(2:end) = r(2:end) .* perda_acumulada(1:end-1);
    
    % Mapeamento nos eixos de amostragem no tempo
    t_max = ceil(esp_acumulado(end));
    samples = 0 : dt_amostra : t_max;
    
    r_serie = zeros(size(samples));
    a_serie = zeros(size(samples));
    
    for k = 1:nr
        [~, idx] = min(abs(samples - esp_acumulado(k)));
        r_serie(idx) = r(k);
        a_serie(idx) = a(k);
    end
end