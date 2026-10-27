#!/bin/bash

set -e

if [ -z "$1" ]
    then
    echo "no velocity model (vel.out) supplied"
    exit 0
fi

# dimensoes da janela do visualizador X-11
WIDTH=800
HEIGHT=600

# dimensoes da malha: n1 e n2 representam a qtde de amostras (matriz n1 x n2)
# d1 e d2 representam a distancia (em metros) entre cada amostra
n1=600   d1=10
n2=1600  d2=10

# Posicao da fonte
xs=$((800 * $d2))
zs=$((100 * $d1))
hsz=$((100 * $d1))
vsx=$((800 * $d2))

# NAO LEIA hseis.pml.out com ximage, pois ele contem um header em cada traco!!!
vsfile="vseis.pml.out" ssfile="sseis.pml.out" hsfile="hseis.pml.out"

# Parametros de simulacao
tmax=5 # para secoes quilometricas, mantenha esse valor alto
mt=10 pml=1 pml_thick=20

echo "iniciando a simulacao por diferenças finitas..."

sufdmod2_pml <$1 nz=$n1 dz=$d1 nx=$n2 dx=$d2 \
    xs=$xs zs=$zs hsz=$hsz vsx=$vsx hsfile=$hsfile \
    vsfile=$vsfile ssfile=$ssfile verbose=1 \
    tmax=$tmax abs=1,1,1,1 mt=$mt pml=$pml pml_thick=$pml_thick 2&> /dev/null

# calcular gx a partir dos offsets
suchw < "$hsfile" key1=gx key2=sx key3=offset b=1 c=1 > tiro.su

# nao consigo visualizar no WSL (talves no Mint?)
echo "simulacao concluida!"

exit 0