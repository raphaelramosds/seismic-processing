# Exercicio 12 - U-Net minima
# ---------------------------
# Implemente uma U-Net pequena com:

# - uma etapa de descida;
# - um bottleneck;
# - uma etapa de subida;
# - uma skip connection;
# - uma camada final Conv2d.

# Use entrada com shape:

#     (batch, canais, altura, largura)
#     (4, 1, 64, 64)

# O modelo deve devolver shape:

#     (4, 1, 64, 64)

# Imprima o shape depois de cada bloco durante o primeiro teste.

import torch

class NaiveUNet(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = torch.nn.Conv2d(
            in_channels=1,
            out_channels=1,
            kernel_size=3,
            padding=1 # mantem 64x64
        )
        self.relu1 = torch.nn.ReLU()

        # descida (contracao)
        self.pool1 = torch.nn.MaxPool2d(
            kernel_size=2 # 64x64 -> 32x32
        )

        # bootleneck
        self.conv2 = torch.nn.Conv2d(
            in_channels=1,
            out_channels=1,
            kernel_size=3,
            padding=1
        )
        self.relu2 = torch.nn.ReLU()

        # subida (expansao)
        self.deconv1 = torch.nn.ConvTranspose2d(
            in_channels=1,
            out_channels=1,
            # (n - 1) * stride + 1 * (kernel_size - 1) + 1
            # n = 32
            # entao, para 32x32 expandi para 64x64, precisamos que kernel_size=2 e stride=2
            # Referencia: https://docs.pytorch.org/docs/2.14/generated/torch.nn.ConvTranspose2d.html
            kernel_size=2,
            stride=2 # 32x32 -> 64x64
        )

        # skip connection: concatenar 1 canal de descida com 1 canal de subida (ambos 64x64)
        # entao, a saida final vai receber 2 canais
        self.conv3 = torch.nn.Conv2d(
            in_channels=2,
            out_channels=1,
            kernel_size=3,
            padding=1
        )

    def forward(self, x):
        x1 = self.conv1(self.relu1(x))
        print(f"shape apos conv1 (entrada): {x1.shape}")

        x_pool = self.pool1(x1)
        print(f"shape apos pool1 (descida): {x_pool.shape}")

        x_bottleneck = self.relu2(self.conv2(x_pool))
        print(f"shape apos conv2 (bootleneck): {x_bottleneck.shape}")

        x_up = self.deconv1(x_bottleneck)
        print(f"shape apos deconv1 (subida): {x_up.shape}")

        # NOTE: o objetivo da skip connection eh juntar as informacoes espaciais de alta resolucao (64x64)
        # da etapa de descida com as informacoes contextuais da etapa de subida. 
        # NOTE: isso eh feito mantendo a resolucao de ambas e concatentando seus canais em um so tensor. 
        # Ex: dois tensores (4,1,64,64) concatenados pela dimensao do canal, se tornam um so (4,2,64,64)
        x_skip = torch.cat(
            # NOTE: para concatenar, as dimensoes de TODOS os tensores devem ser as MESMAS
            [x_up, x1], 
            # NOTE: shape = (batch, canais, altura, largura) entao dim = 0 (batch), dim = 1 (canais), dim = 2 (altura) e dim = 3 (largura)
            dim=1 # concatenar na dimensao dos canais (dim = 1)
        )
        print(f"shape apos skip connection: {x_skip.shape}")

        saida = self.conv3(x_skip)
        print(f"shape (saida): {saida.shape}")

        return saida

modelo = NaiveUNet()

entrada = torch.randn(4, 1, 64, 64)

saida = modelo.forward(entrada)