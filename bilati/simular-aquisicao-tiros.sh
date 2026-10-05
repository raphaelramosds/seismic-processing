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

# ximage n1=600 n2=1600 <hseis.pml.out

# Arquivo final acumulado com todos os tiros
ARQ_SAIDA_SU="todos_os_tiros.su"
rm -f "$ARQ_SAIDA_SU"

echo "iniciando loop de disparos e concatenacao em $ARQ_SAIDA_SU..."

# Loop para realizar 10 tiros
for i in $(seq 0 9); do

    # Posicao da fonte (avançando 200 metros a cada tiro)
    xs=$((8000 + i * 200))
    zs=$((100 * $d1))
    hsz=$((100 * $d1))
    vsx=$xs

    vsfile="vseis.pml.out" ssfile="sseis.pml.out" hsfile="hseis.pml.out"

    # Parametros de simulacao
    tmax=5 # para secoes quilometricas, mantenha esse valor alto
    mt=10 pml=1 pml_thick=20

    echo "iniciando a simulacao por diferenças finitas para o tiro $((i+1))/100 (xs=${xs}m)..."

    sufdmod2_pml <$1 nz=$n1 dz=$d1 nx=$n2 dx=$d2 \
        xs=$xs zs=$zs hsz=$hsz vsx=$vsx hsfile=$hsfile \
        vsfile=$vsfile ssfile=$ssfile verbose=1 \
        tmax=$tmax abs=1,1,1,1 mt=$mt pml=$pml pml_thick=$pml_thick 2>&1 > /dev/null

    echo "simulacao concluida!"

    # calcular gx a partir dos offsets
    suchw < "$hsfile" key1=gx key2=sx key3=offset b=1 c=1 >> "$ARQ_SAIDA_SU"

    # Limpa arquivos intermediários
    rm -f "$hsfile" "$vsfile" "$ssfile"

done

echo "processamento concluido! Todos os tiros foram salvos em '$ARQ_SAIDA_SU'."

exit 0