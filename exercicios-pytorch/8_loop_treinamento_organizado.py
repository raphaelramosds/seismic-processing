# Exercicio 8 - Loop de treinamento organizado
# --------------------------------------------
# Separe o treinamento em funcoes:

# - train_step;
# - train_epoch;
# - evaluate;

# A funcao evaluate deve usar torch.no_grad().

# Adicione:
# - zero_grad;
# - backward;
# - optimizer.step;
# - registro da loss media por epoca.

import torch
from torch.utils.data import Dataset, DataLoader

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

def train_step(otimizador, feat, label, loss_fn, w, b):
    """Calcula a previsao, a loss e os gradientes"""
    y_pred = w * feat + b

    loss = loss_fn(y_pred, label)

    otimizador.zero_grad()

    loss.backward()

    otimizador.step()

    return loss.item()

def train_epoch(otimizador, dados_dl, loss_fn, w, b):
    """Execute o train step em todos os batches """
    loss_total = 0.0

    # o data loader aponta para todos os batches
    for feat, label in dados_dl:
        loss_total += train_step(
            otimizador, feat, label, loss_fn, w, b
        )

    return loss_total / len(dados_dl)

def train(epochs: int, dados_dl: DataLoader):
    """Configuracoes e loop do treinamento"""
    w = torch.rand(1, requires_grad=True)
    b = torch.rand(1, requires_grad=True)

    otimizador = torch.optim.SGD([w, b], lr=0.01, momentum=0.9)
    loss_fn = torch.nn.MSELoss()

    historico_loss = []

    for epoch in range(epochs):
        loss_media = train_epoch(
            otimizador, dados_dl, loss_fn, w, b
        )
        if epoch % 10 == 0:
            print(f"epoch #{epoch}: MSE = {loss_media}")
        historico_loss.append(loss_media)

    return w, b, historico_loss


def evaluate(w: torch.Tensor, b: torch.Tensor, x_teste: torch.Tensor):
    # torch.no_grad desativa o calculo e armazenamento de gradientes
    # por que desativar? reduz o uso de memoria e acelera as previsoes
    with torch.no_grad():
        return w.item() * x_teste + b.item()

# Dados sintéticos seguindo y = 3x + 2
ns=32           # precisa ser divisivel por batch_size
batch_size=8
m=3
b=2
x_data = torch.linspace(-1, 1, ns).reshape(-1, 1)
y_data = m * x_data + b
print(f"{len(x_data)} amostras")

# Dataset e DataLoader
dataset = DatasetRegressao(x_data, y_data)
dados_dl = DataLoader(
    dataset,
    batch_size=batch_size,
    shuffle=True
)

# Treinamento
w, b, historico_loss = train(
    epochs=100,
    dados_dl=dados_dl
)

print(f"\nw aprendido: {w.item()}")
print(f"b aprendido: {b.item()}")
print(f"MSE medio inicial: {historico_loss[0]}")
print(f"MSE medio final: {historico_loss[-1]}")

# Avaliacao em novos valores
x_teste = torch.tensor([[-1.0], [0.0], [0.5], [1.0]])
y_real = m * x_teste + b
y_pred = evaluate(w, b, x_teste)

print("\nPrevisoes:")
for x, pred, real in zip(x_teste, y_pred, y_real):
    print(f"x = {x.item()} -> y previsto = {pred.item()}, y real = {real.item()}")