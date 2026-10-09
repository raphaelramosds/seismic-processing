# Exercicio 10 - Max pooling e mudanca de resolucao
# -------------------------------------------------
# Use MaxPool2d(kernel_size=2) na imagem do exercicio anterior.

# Compare os shapes antes e depois do pooling. Depois use ConvTranspose2d ou
# Upsample para aumentar novamente a resolucao.

# Pergunta: aumentar a resolucao recupera exatamente a informacao perdida?

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

# Camadas
c1 = torch.nn.Conv2d(n_canais_entrada, n_canais_saida, kernel_size=3, padding=1)
c2 = torch.nn.MaxPool2d(
    kernel_size=2
)
c3 = torch.nn.ConvTranspose2d(
    in_channels=n_canais_saida,
    out_channels=n_canais_saida,
    # Para recuperar a dimensao N x N precisamos encontrar o valor de kernel_size tal que:
    #   (Hin - 1) + (kernel_size - 1) + 1 = N
    # Numericamente:
    #   se c2 produz dois kernels 4 x 4, entao Hin = 4
    #   se N = 8, entao kernel_size = 5
    # Referencia: https://docs.pytorch.org/docs/2.14/generated/torch.nn.ConvTranspose2d.html
    kernel_size=5
)

# Aplicar camada de convolucao na imagem
imagem_conv = c1(imagem)
print(f"shape antes do pooling = {imagem_conv.shape}")

# Aplicar max pooling
imagem_conv_maxpool = c2(imagem_conv)
print(f"shape depois do pooling = {imagem_conv_maxpool.shape}")

# Aplicar convolucao transposta (deconvolucao)
imagem_conv_maxpool_deconv = c3(imagem_conv_maxpool)
print(f"shape depois da deconvolucao = {imagem_conv_maxpool_deconv.shape}")