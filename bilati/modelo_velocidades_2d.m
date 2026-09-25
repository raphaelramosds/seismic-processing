nz = 600;  % n1 em profundidade
nx = 1600; % n2 no eixo horizontal

z = linspace(0, 600, nz);
x = linspace(0, 1600, nx);
[X, Z] = meshgrid(x, z);

% Construção das camadas de velocidade (em m/s)
vel = 1500 * ones(size(Z));
vel(Z > 150) = 2000; % 2 km/s
vel(Z > 300) = 3000;
vel(Z > 450) = 4000;

% Salvar a transposta 'vel'' para respeitar o formato V[nx][nz]
fid = fopen('vel.out', 'w', 'ieee-le');
fwrite(fid, single(vel'), 'float32');
fclose(fid);