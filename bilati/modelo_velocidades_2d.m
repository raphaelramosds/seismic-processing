nz = 6000;  % número de amostras no eixo Z
nx = 16000; % número de amostras no eixo X

z_max = 6000;  % profundidade máxima em metros (6 km)
x_max = 16000; % extensão máxima em metros (16 km)

z = linspace(0, z_max, nz); % cria z_max pontos entre 0 e nz
x = linspace(0, x_max, nx); % cria x_max pontos entre 0 e nx

[X, Z] = meshgrid(x,z);

vel = 1500 * ones(size(Z)); % inicializa todas com 1500 m/s
vel(Z > 500) = 2000; % camada 2 tem 2 km/s
vel(Z > 1500) = 3000; % camada 3 tem 3 km/s
vel(Z > 2000) = 4000; % camada 4 tem 4 km/s

% precisao simples
vel_single = single(vel);

% salvar arquivo em little-endian (float32)
fid = fopen('modelo_velocidades_2d.bin', 'w', 'ieee-le');
fwrite(fid, single(vel), 'float32');
fclose(fid)

info = dir('modelo_velocidades_2d.bin');
fprintf('Tamanho do arquivo gerado: %d bytes\n', info.bytes);