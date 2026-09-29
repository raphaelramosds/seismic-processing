function dip_map = estimar_dip_map(dado, dt, dx, p_range)
    [nt, nx] = size(dado);
    np = length(p_range);
    dip_map = zeros(nt, nx);
    
    df = 1 / (nt * dt);
    f = (0:nt-1)' * df;
    w = 2 * pi * f;
    
    for ix = 1:nx-1
        t1_fft = fft(dado(:, ix));
        t2     = dado(:, ix+1);
        
        min_err = inf(nt, 1);
        best_p  = zeros(nt, 1);
        
        for ip = 1:np
            p = p_range(ip);
            shift_operator = exp(-1i * w * p * dx);
            t2_pred = real(ifft(t1_fft .* shift_operator));
            
            err = (t2 - t2_pred).^2;
            
            mask = err < min_err;
            min_err(mask) = err(mask);
            best_p(mask)  = p;
        end
        dip_map(:, ix) = best_p;
    end
    dip_map(:, end) = dip_map(:, end-1);
end