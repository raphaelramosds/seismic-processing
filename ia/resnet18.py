import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np


# classes para aplicar variacoes nas imagens do dataset de treino
transform_train = transforms.Compose([
    # transformacoes
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    # normalizacao
    transforms.Normalize((0.4914, 0.4822, 0.4465), 
                         (0.2023, 0.1994, 0.2010))
])

transform_test = transforms.Compose([
    transforms.ToTensor(),
    # normalizacao
    transforms.Normalize((0.4914, 0.4822, 0.4465), 
                         (0.2023, 0.1994, 0.2010))
])

# datasets e loaders de treino e de teste
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

# definir o bloco de residuo conforme a RestNet18
# NOTE: o bloco de residuo previne o desaparecimento do gradiente
# NOTE: ele contem duas camadas convolucionais (Conv), cada uma seguida por
# uma camada de normlizacao em batch (BatchNorm) e ReLU
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()

        # caso haja um desecontro de dimensoes (in_channels diferente de out_channels)
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                # skip connection
                # NOTE: usa uma convolucao 1x1 (kernel_size = 1) para ajustar as dimensoes, seguida da normalizacao em batch
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out += self.shortcut(x) # skip connection de x com a saida do ultimo BatchNorm2d
        out = self.relu(out)
        return out

# definicao da rede RestNet18
# - quatro camadas residuais com canais crescentes (64 -> 128 -> 256 -> 512)
# - cada camada eh criada com funcoes "make layer" para gerar copias de um bloco residual
# - "global average pooling" converte mapas de caracteristica em um vetor
# - contem uma FCNN (fully connected neural network) com 10 classes de saida
class ResNet18(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet18, self).__init__()

        # variavel auxiliar para ser utilizada durante a construcao da rede
        # ela guarda quantos canais sairam do ultimo bloco criado
        self.in_channels = 64

        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        
        self.layer1 = self._make_layer(ResidualBlock, 64, 2, stride=1)
        self.layer2 = self._make_layer(ResidualBlock, 128, 2, stride=2)
        self.layer3 = self._make_layer(ResidualBlock, 256, 2, stride=2)
        self.layer4 = self._make_layer(ResidualBlock, 512, 2, stride=2)
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # fully connected
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, block, out_channels, num_blocks, stride):
        """
        empilha num_blocks blocos residuais em um unico nn.Sequential
        """
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_channels, out_channels, stride))
            # o proximo bloco recebe (in_channels) o que este produziu (out_channels)
            self.in_channels = out_channels
        return nn.Sequential(*layers)

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        
        out = self.avgpool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out

model = ResNet18().to(device)
print(model)

# definir a funcao de perda como entropia cruzada, SGD como otimizador e
# um cronograma (scheduler) para reduzir a taxa de aprendizado durante o treinamento
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

# REFERENCIA: https://www.geeksforgeeks.org/deep-learning/resnet18-from-scratch-using-pytorch/