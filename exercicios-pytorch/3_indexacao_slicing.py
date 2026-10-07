# Exercicio 3 - Indexacao e slicing
# ---------------------------------
# Crie um tensor com valores de 0 ate 23 e transforme-o em uma matriz (4, 6).

# Extraia:
# - a primeira linha;
# - a ultima coluna;
# - as duas primeiras linhas;
# - um bloco com linhas 2 e 3 e colunas 3, 4 e 5;
# - todos os valores maiores que 10.

import torch

matriz45 = torch.randint(0, 23, (4,6))
print(matriz45)

primeira_linha = matriz45[0,:]
print(primeira_linha)

ultima_coluna = matriz45[:,-1]
print(ultima_coluna)

duas_primeiras_linhas = matriz45[:2,]
print(duas_primeiras_linhas)

bloco_l23_c345 = matriz45[2:4,3:6]
print(bloco_l23_c345)

maior10 = matriz45[matriz45 > 10]
print(maior10)