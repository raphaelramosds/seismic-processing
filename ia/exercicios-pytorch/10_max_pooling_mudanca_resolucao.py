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

# Camada de convolucao
c1 = torch.nn.Conv2d(n_canais_entrada, n_canais_saida, kernel_size=3, padding=1)

# Camada de max pooling (downsampling)
c2 = torch.nn.MaxPool2d(
    kernel_size=2
)

# aumentar resolucao por convolucao transposta
c3 = torch.nn.ConvTranspose2d(
    in_channels=n_canais_saida,
    out_channels=n_canais_saida,
    # Para recuperar a dimensao N x N precisamos encontrar o valor de kernel_size tal que:
    #   (n - 1) + (kernel_size - 1) + 1 = N
    # Numericamente:
    #   se c2 produz dois kernels 4 x 4, entao n = 4
    #   se N = 8, entao kernel_size = 5
    # Referencia: https://docs.pytorch.org/docs/2.14/generated/torch.nn.ConvTranspose2d.html
    kernel_size=5
)

# alternativa: aumentar a resolucao por upsampling
c3_upsample = torch.nn.Upsample(
    scale_factor=2,
    mode="nearest"
    # Abaixo como funciona o upsampling por nearest:
    #
    #            a a b b
    # a b   ->   a a b b
    # c d        c c d d
    #            c c d d
)

# Aplicar camada de convolucao na imagem
imagem_conv = c1(imagem)
print(f"shape antes do pooling = {imagem_conv.shape}")

# Aplicar max pooling
imagem_conv_maxpool = c2(imagem_conv)
print(f"shape depois do pooling = {imagem_conv_maxpool.shape}")

# Aplicar convolucao transposta (deconvolucao)
imagem_conv_maxpool_deconv = c3(imagem_conv_maxpool)
print(f"(C3 deconv) shape depois da deconvolucao = {imagem_conv_maxpool_deconv.shape}")

# alternativa: aplicar upsampling
imagem_conv_maxpool_upsample = c3_upsample(imagem_conv_maxpool)
print(f"(C3 upsampling) shape depois do upsampling = {imagem_conv_maxpool_deconv.shape}")

# Comparar a saida antes do pooling com a saida apos a expansao
diferenca_deconv = imagem_conv - imagem_conv_maxpool_deconv
diferenca_upsamling = imagem_conv - imagem_conv_maxpool_upsample

# aumentar a resolucao vai recuperar parcialmente a informacao perdida
print(f"deconv - erro absoluto medio (MAE) = {(diferenca_deconv.abs().mean()).item():.6f}")
print(f"upsampling - erro absoluto medio (MAE) = {(diferenca_upsamling.abs().mean()).item():.6f}")

# OBS: O kernel ConvTranspose2d tem pesos treinaveis
# Entao, se ele nao for treinado corretamente, a recuperacao por upsampling
# consegue recuperar melhor a informacao perdida (menor MAE)