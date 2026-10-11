# Exercicio 11 - Bloco convolucional
# ----------------------------------
# Crie um modulo chamado ConvBlock contendo:

# - Conv2d;
# - ReLU ou SiLU;
# - outra Conv2d;
# - outra ativacao.

# O bloco deve receber um tensor e devolver outro tensor com a mesma altura e
# largura.

# Teste o bloco com uma entrada de shape (2, 1, 32, 32).

import torch

class ConvBlock(torch.nn.Module):

    def __init__(self, n_canais):
        super(ConvBlock, self).__init__()
        self.conv1 = torch.nn.Conv2d(
            in_channels=n_canais,
            out_channels=n_canais,
            # M - N + 2P + 1 = M
            # P = (1 + N)/2 para manter a dimensao da imagem
            kernel_size=3, # N=3
            padding=1 # P=1
        )
        self.relu1 = torch.nn.ReLU()
        self.conv2 = torch.nn.Conv2d(
            in_channels=n_canais,
            out_channels=n_canais,
            # (mesmo raciocinio anterior)
            kernel_size=3,
            padding=1
        )
        self.relu2 = torch.nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.relu2(x)
        return x


imagem = torch.rand((2,1,32,32), dtype=torch.float32)

conv_block = ConvBlock(n_canais=1)

saida = conv_block(imagem)

print("shape (entrada):", imagem.shape)
print("shape (saida):", saida.shape)