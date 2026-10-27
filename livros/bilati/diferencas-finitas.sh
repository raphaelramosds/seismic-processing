# gere modelo_velocidades_2d.bin com o matlab

# resolver modelo de velocidade com diferencas finitas
sufdmod2 < modelo_velocidades_2d.bin > ondas.su \
  nx=16000 nz=6000 dx=1.0 dz=1.0 \
  xs=8000 zs=10 tmax=6.0