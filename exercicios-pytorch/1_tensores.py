# Exercicio 1 - Criar e inspecionar tensores
# ------------------------------------------
# Crie tensores PyTorch com:

# 1. Uma lista com os valores 1, 2, 3 e 4.
# 2. Uma matriz de zeros com formato (3, 5).
# 3. Uma matriz de uns com formato (2, 4).
# 4. Uma matriz com valores aleatorios e formato (3, 3).

# Para cada tensor, imprima:
# - o proprio tensor;
# - shape;
# - dtype;
# - device.

# Pergunta: qual e a diferenca entre shape, dtype e device?

import torch

def info(tensor: torch.Tensor):
    print(f"""
    shape: {tensor.shape}
    dtype: {tensor.dtype}
    device: {tensor.device}
    """)

print(f"torch v{torch.__version__}")

tlista = torch.tensor([1,2,3,4])
print(tlista)
info(tlista)

tmatriz35 = torch.zeros(3,5, dtype=torch.float32)
print(tmatriz35)
info(tmatriz35)

tmatriz24 = torch.ones(2, 4, dtype=torch.float32)
print(tmatriz24)
info(tmatriz24)

tmatriz33 = torch.rand(3,3, dtype=torch.float32)
print(tmatriz33)
info(tmatriz33)

# shape retorna uma instancia do objeto torch.Size
# dtype retorna objetos de tipos do PyTorch: torch.float32, torch.float64, torch.int
# device retorna qual device (cpu ou gpu) esta sendo usado