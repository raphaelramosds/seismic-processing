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

from torch.utils.data import Dataset

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

def train_step():
    ...

def train_epoch():
    ...

def evaluate():
    ...