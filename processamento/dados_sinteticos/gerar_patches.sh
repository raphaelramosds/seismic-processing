#!/usr/bin/env bash
# Uso: ./gerar_patches.sh [N]
set -euo pipefail

N=${1:-4}           # numero de patches (par)
SAIDA=su/patches    # diretorio de saida dos patches

# resolver arquivos neste diretorio
cd "$(dirname "$0")"

# Gera uma secao sintetica com difracoes e 
python refletividade_2d_difracoes.py

# Divide cada secao em N patches
for secao in total_ruidosa; do
    python patches_2d.py "su/difracoes/secao_2d_${secao}.su" "$N" --saida "$SAIDA"
done