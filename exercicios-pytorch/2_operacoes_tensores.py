# Exercicio 2 - Operacoes e broadcasting
# --------------------------------------
# Crie dois tensores de formato (2, 3). Calcule:

# - soma;
# - subtracao;
# - multiplicacao elemento a elemento;
# - divisao;
# - media;
# - valor minimo e maximo.

# Depois some um tensor de formato (2, 3) com um tensor de formato (3,) (vetor de 3 elementos).
# Explique por que essa operacao funciona.

import torch

torch.manual_seed(10)

t1 = torch.rand(2, 3, dtype=torch.float32)
t2 = torch.rand(2, 3, dtype=torch.float32)
t3 = torch.rand(3, dtype=torch.float32) # (3,)
tones = torch.ones(2, 3, dtype=torch.float32)
dtones = 2*tones

print(t1)
print(t2)
print(t3)
print(tones)
print(dtones)

# soma e subtracao
print(t1 + t2)

# multiplicacao elemento a elemento
print(tones * t2)

# divisao elemento a elemento
print(t2 / dtones)

# media dos elementos
print(t1.mean())

# valor minimo e maximo
print(f"max={t1.max()} e min = {t1.min()}")

# somar um tensor (2,3) com tensor de formato (3,)
# resultado: soma o tensor (3,) a cada linha do tensor (2,3)
# entao, o resultado vai ser um tensor (2,3)
print(t1 + t3)