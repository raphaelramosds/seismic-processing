# Exercicio 7 - Dataset e DataLoader
# ----------------------------------
# Crie uma classe Dataset que gere pares (x, y) para a reta do exercicio
# anterior. Depois:

# - crie um DataLoader;
# - use batch_size=8;
# - embaralhe os dados;
# - imprima o shape de um batch;
# - treine novamente o modelo usando batches.

# Observe a diferenca entre um tensor com shape (8,) e um tensor com shape
# (8, 1).

# Dataset vs DataLoader:
# - Dataset armazena as amostras e seus labels
# - DataLoader eh um iterador para acessar as amostras do Dataset

import torch
from torch.utils.data import Dataset, DataLoader

# Toda classe que herda Dataset tem que implementar tres funcoes: __init__, __len__ e __getitem__
class DatasetRegressao(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data

    def __len__(self):
        # numero de amostras no dataset
        return len(self.x_data)

    def __getitem__(self, index):
        # retorna uma amostra na posicao index com seu rotulo
        return self.x_data[index], self.y_data[index]

m=3.0
bias=2.0

epochs=100
ns=10

x_data = torch.rand(ns, 1)
y_data = m*x_data+bias

dados = DatasetRegressao(x_data, y_data)
dados_dl = DataLoader(dados, batch_size=8, shuffle=True)
n_dados = len(dados_dl)

# modelo: inferir w e b
w = torch.rand(1, requires_grad=True)
b = torch.rand(1, requires_grad=True)

# otimizador e funcao de perda
otimizador = torch.optim.SGD([w, b], lr=0.01, momentum=0.9)
loss_fn = torch.nn.MSELoss()

treino_features, treino_labels = next(iter(dados_dl))
print(f"shape primeiro batch: {treino_features.shape}")

for epoch in range(epochs):
    soma_loss = 0.0
    for feat, label in dados_dl:
        # forward
        y_pred = w*feat + b

        # calculo da perda
        loss = loss_fn(y_pred, label)

        # zerar gradientes acumulados
        otimizador.zero_grad()

        # calcula gradientes de w e b com backpropagation
        loss.backward()

        # atualiza w e b
        otimizador.step()

        soma_loss += loss.item()
    
    mse_medio = soma_loss/n_dados

    if epoch % 10 == 0:
            print(f"epoca {epoch}: MSE (medio) = {mse_medio:.4f}")

# testar com um ponto qualquer
x_teste = -1.0
y_teste = m*x_teste + bias
y_teste_pred = w.item() * x_teste + b.item()
print(f"real = {y_teste}")
print(f"pred = {y_teste_pred:.3f}")