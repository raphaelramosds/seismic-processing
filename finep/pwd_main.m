clear; clc;

%% 1. Parametros do Dado (Obtidos no SU via 'surange')
nt = 600;         % ns: n�mero de amostras no tempo
dt = 0.004;       % dt: intervalo de amostragem no tempo em segundos
dx = 20;          % dx: dist�ncia horizontal entre tra�os em metros

%% 2. Leitura das Amostras Binarias Extraidas do SU
filename_in = 'dadoBasico_amostras.bin'; % Gerado no terminal: sustrip < entrada.su head=cabecalho.bin > dado_amostras.bin[cite: 3]

fid = fopen(filename_in, 'r', 'ieee-le'); 
if fid == -1
    error('N�o foi poss�vel abrir o arquivo %s. Verifique se executou o sustrip.', filename_in);
end
dado = fread(fid, [nt, Inf], 'float32');
fclose(fid);

[nt, nx] = size(dado);
fprintf('-> Dado carregado: %d amostras x %d tra�os.\n', nt, nx);

%% 3. Etapa 1: Estimativa do Mapa de Mergulhos (Dip Map)
% Define a faixa de varredura de inclinacoes (p = dt/dx em s/m)
p_range = linspace(-0.0008, 0.0008, 201); 

fprintf('-> Estimando o mapa de mergulhos locais (dip_map)...\n');
dip_map = estimar_dip_map(dado, dt, dx, p_range);

%% 4. Etapa 2: Aplicacao do Operador PWD (Chamada da SUA Funcao)
fprintf('-> Aplicando a fun��o operador_pwd...\n');
residual = operador_pwd(dado, dt, dx, dip_map);

%% 5. Exportacao das Difracoes Isoladas (Residuo em Float32)
fid_res = fopen('residuos_difracao.bin', 'w', 'ieee-le');
fwrite(fid_res, single(residual), 'float32');
fclose(fid_res);

fid_dip = fopen('mapa_dip.bin', 'w', 'ieee-le');
fwrite(fid_dip, single(dip_map), 'float32');
fclose(fid_dip);

fprintf('-> Sucesso! Arquivos "residuos_difracao.bin" e "mapa_dip.bin" gerados.\n');

% Decompoe os eventos para o dominio Tau-P
% sutaup < dado_entrada.su > dado_taup.su dx=10 dt=0.004 pmin=-0.0005 pmax=0.0005 np=101

% Visualiza as energias concentradas nos valores de p dos refletores
% suximage < dado_taup.su title="Decomposicao Tau-P Inclinacoes" label2="Slowness p s/m" label1="Tau s" &

% Separa os dados binarios do cabecalho
% sustrip < dadoBasico_reflecoes_difracoes.su head=cabecalho.bin > amostras.bin

% Reconstroi dado SU a partir dos dados binarios e do header
% supaste < residuos_difracao.bin head=dadoBasico_cabecalho.bin ns=600 > difracoes_separadas.su

% Visualizar as difracoes resultantes da filtragem
% suximage < difracoes_separadas.su title="Difracoes Isoladas pelo PWD" label1="Tempo s" label2="Tracos" &