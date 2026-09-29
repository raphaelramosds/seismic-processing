function residual = operador_pwd(dado, dt, dx, dip_map)
    % DADO: Matriz de amostragem temporal x espacial (nt x nx)
    % DT: Intervalo de amostragem no tempo (s)
    % DX: Distancia entre tracos (m)
    % DIP_MAP: Matriz de mergulhos locais estipulados/estimados (nt x nx) [s/m]
    
    [nt, nx] = size(dado);
    residual = zeros(nt, nx);
    
    % Frequ�ncias
    df = 1 / (nt * dt);
    f = (0:nt-1)' * df;
    w = 2 * pi * f;
    
    for ix = 1:nx-1
        t1 = dado(:, ix);     % Traco atual P(x)
        t2 = dado(:, ix+1);   % Proximo traco real P(x + dx)
        
        T1_fft = fft(t1);
        
        % Aplica o deslocamento de fase baseado no dip ponto a ponto
        % Para simplificar por bloco/coluna:
        sigma_col = dip_map(:, ix); 
        
        % Predicao do traco P_predito(x + dx)
        % Para cada frequencia, desloca a fase correspondente ao dip medio ou amostrado
        t2_pred = zeros(nt, 1);
        for it = 1:nt
            shift_operator = exp(-1i * w * sigma_col(it) * dx);
            t2_pred_all = real(ifft(T1_fft .* shift_operator));
            t2_pred(it) = t2_pred_all(it); % P_predito(x+dx, t)
        end
        
        % Aplicacao da subtracao diferencial / residuo: R = P(x+dx) - C(sigma)*P(x)
        residual(:, ix) = t2 - t2_pred;
    end
    
    % ultimo traco
    residual(:, end) = residual(:, end-1);
end