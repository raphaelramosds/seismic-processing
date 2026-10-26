# Exercicio 4 - Reshape, view e transpose
# ---------------------------------------
# Crie um tensor com shape (2, 3, 4). Gere versoes com:

# - shape (6, 4);
# - shape (2, 12);
# - dimensoes trocadas;
# - uma nova dimensao usando unsqueeze;
# - uma dimensao removida usando squeeze.

# Registre o shape antes e depois de cada operacao.

import torch 

# tensor 3D (plano, linha, coluna)
matriz234 = torch.rand(size=(2,3,4))

print(matriz234)
print(matriz234.shape)

# concatene as duas matrizes (3,4)
matriz64 = matriz234.reshape((6,4))
print(matriz64)
print(matriz64.shape)

# colapse em 2 linhas com 12 colunas
matriz212 = matriz234.reshape((2,12))
print(matriz212)

# unsqueeze adiciona uma nova dimensao
print("com nova dimensao:\n")
matriz_nova_dimensao = matriz234.unsqueeze(1)
print(matriz_nova_dimensao)
print(matriz_nova_dimensao.shape)

# squeeze remove uma dimensao
print("com dimensao removida:\n")
matriz_menos_dimensao = matriz_nova_dimensao.squeeze()
print(matriz_menos_dimensao)
print(matriz_menos_dimensao.shape)

# extra: colapsar uma matriz (2,3,4) em um vetor (2*3*4,)
vetor234 = matriz234.reshape((matriz234.shape.numel(),))
print(vetor234)