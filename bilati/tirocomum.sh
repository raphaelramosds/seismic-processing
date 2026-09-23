#!/bin/bash

# Parâmetros da grade do modelo
NZ=6000       # n1 em profundidade
NX=16000      # n2 na horizontal
DZ=1.0        # Espaçamento em Z (m)
DX=1.0        # Espaçamento em X (m)

# Parâmetros do disparo e arranjo
XS=8000       # Posição X da fonte (meio da linha = 8 km)
ZS=10         # Profundidade da fonte (m)

# Execução da modelagem por diferenças finitas
sufdmod2d < modelo_velocidades_2d.bin \
  nx=$NX nz=$NZ dx=$DX dz=$DZ \
  xs=$XS zs=$ZS \
  tmax=6.0 dt=0.001 \
  fmax=25.0 \
  abs=1,1,1,1 \
  > tiro_fd.su

echo "Simulação concluída com sucesso!"