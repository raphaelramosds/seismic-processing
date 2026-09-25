#!/bin/bash

if [ -z "$1" ]
    then
    echo "no velocity model (vel.out) supplied"
    exit 0
fi

# dimensoes da janela do visualizador X-11
WIDTH=800
HEIGHT=600

# dimensoes da malha
n1=600   d1=1.0
n2=1600  d2=1.0

# Posicao da fonte
xs=800 zs=10 hsz=10 vsx=800

vsfile="vseis.pml.out" ssfile="sseis.pml.out" hsfile="hseis.pml.out"

# Parametros de simulacao
tmax=0.5 
mt=10 pml=1 pml_thick=20

echo "iniciando a simulacao por diferenças finitas..."

sufdmod2_pml <$1 nz=$n1 dz=$d1 nx=$n2 dx=$d2 \
    xs=$xs zs=$zs hsz=$hsz vsx=$vsx hsfile=$hsfile \
    vsfile=$vsfile ssfile=$ssfile verbose=1 \
    tmax=$tmax abs=1,1,1,1 mt=$mt pml=$pml pml_thick=$pml_thick 2&> /dev/null

# nao consigo visualizar no WSL (talves no Mint?)
echo "simulacao concluida!"

# xmovie < filme_ondas.bin \
#     n1=$n1 n2=$n2 d1=$d1 d2=$d2 \
#     title="Propagacao da Onda Acustica" \
#     cmap=gray loop=2 interp=0 \
#     -geometry ${WIDTH}x${HEIGHT}+50+50 &

exit 0