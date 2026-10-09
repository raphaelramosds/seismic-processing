# Exercicio 9 - Convolucao 2D manual
# ----------------------------------
# Crie uma imagem simples com shape (1, 1, 8, 8), contendo um quadrado
# branco sobre fundo preto.

# Crie uma camada:

#     torch.nn.Conv2d(1, 2, kernel_size=3, padding=1)

# Passe a imagem pela camada e imprima:
# - shape da entrada;
# - shape da saida;
# - valores minimo e maximo da saida.

# Explique o significado de:
# - canais de entrada;
# - canais de saida;
# - kernel_size;
# - padding;
# - stride.

# Ilustracao de padding
# veja: https://hannibunny.github.io/mlbook/neuralnetworks/convolutionDemos.html

import torch

n_canais_entrada = 1
n_canais_saida = 2
n = 8
raio = n/4

# coordenada do centro
x0 = y0 = n/2 - 1

eixo = torch.arange(0, n)
y, x = torch.meshgrid(eixo, eixo, indexing="ij")
z = torch.max(torch.abs(y - y0), torch.abs(x - x0))

quadrado = (z <= raio).float()

imagem = torch.reshape(quadrado, (1, 1, n, n))
print(imagem.shape)
print(imagem)

# Camada convolucional
c1 = torch.nn.Conv2d(n_canais_entrada, n_canais_saida, kernel_size=3, padding=1)

# # Aplicar camada de convolucao na imagem
imagem_conv = c1(imagem)
print(imagem_conv.shape)
print(imagem_conv.min())
print(imagem_conv.max())