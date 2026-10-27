nz = 600;  % n1 em profundidade
nx = 1600; % n2 no eixo horizontal

vel = ones(nz, nx)*1500;
vel(150:300,:) = 2000;
vel(301:450,:) = 3000;
vel(451:end,:) = 4000;

fid = fopen('vel.out', 'w', 'ieee-le');
fwrite(fid, vel, 'float32');
fclose(fid);