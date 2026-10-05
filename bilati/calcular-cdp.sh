#!/bin/bash

set -e

fln="todos_os_tiros.su"

# calcular CDPs
suchw < "$fln" key1=cdp key2=gx key3=sx b=0.5 c=0.5 > todos_os_tiros_cdp.su

# ordenar por CDPs
susort cdp offset <todos_os_tiros_cdp.su > todos_os_tiros_ordenados.su 

# plote todos os CDPs
suximage <todos_os_tiros_ordenados.su perc=99 &

# plotar
cdp=4000
suwind key=cdp min=$cdp max=$cdp < dado_ordenado_cdp.su | \
suximage title="CDP Gather $cdp" label2="Offset m" label1="Tempo s" perc=99 &