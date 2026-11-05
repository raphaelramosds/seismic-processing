# processamento

## scripts basicos

- `refletividade_1d.ipynb` mostra como gerar uma seção sísmica a partir de um modelo de refletividade 1D, utilizando a convolução com uma onda sísmica.
- `calculo_cmp.py` mostra como calcular o CMP a partir de uma geometria de aquisição sísmica (número de tiros e posições de receptores e fontes).

## dados_sinteticos

- `refletividade_2d.py` mostra como gerar uma seção sísmica a partir de um modelo de refletividade 2D. As seções são salvas em `su/`.
- `refletividade_2d_difracoes.py` mostra como gerar uma seção sísmica a partir de um modelo de refletividade 2D, incluindo difrações. As seções são salvas em `su/difracoes/`.
- `patches_2d.py` divide uma seção SU em N patches (N par), salvando cada patch como um arquivo SU com o número de traços e amostras corrigidos.
- `gerar_patches.sh` gera uma seção com difrações e divide cada uma das seções resultantes em N patches, salvos em `su/patches/`.
- `gerar_dataset.py` gera um dataset para separação de difrações: lê de um arquivo JSON o número de modelos, de refletores, de difrações por refletor e de patches, e salva os patches em `su/dataset/data/` (dado completo, com ruído) e `su/dataset/label/` (apenas difrações). Os arquivos correspondentes têm o mesmo nome nos dois diretórios (`modelo_XXXX_patch_YY.su`). Copie `dataset-exemplo.json` para `dataset.json` (ignorado pelo git) e ajuste os parâmetros.
- `utils.py` reúne as funções auxiliares: pulso Ricker, convolução, adição de ruído e leitura/escrita de arquivos SU.

Os scripts devem ser executados a partir de `dados_sinteticos/`, pois usam caminhos relativos a esse diretório:

```bash
# OBRIGATORIO
cd dados_sinteticos

# exemplo: executar o script PY sem parametros
python refletividade_2d.py

# exemplo: executar o script PY com parametros
python patches_2d.py su/difracoes/secao_2d_total.su 4 --saida su/patches

# exemplo: executar o script SH com parametros
chmod +x gerar_patches.sh
./gerar_patches.sh 4   # N = 4 por padrao

# exemplo: dataset configurado em dataset.json (copia local, ignorada pelo git)
cp dataset-exemplo.json dataset.json
python gerar_dataset.py dataset.json
```
