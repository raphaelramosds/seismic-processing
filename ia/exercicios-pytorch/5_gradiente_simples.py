# Exercicio 5 - Gradientes simples
# -------------------------------
# Crie um tensor x com requires_grad=True e calcule:

#     y = (x ** 2).mean()

# Chame backward() e imprima x.grad.

# Repita usando:

#     y = (3 * x + 2).sum()

# Compare o gradiente obtido com o resultado esperado matematicamente.

# Referencia: https://www.geeksforgeeks.org/deep-learning/understanding-pytorchs-autogradgrad-and-autogradbackward/

import torch

# 1) estimar o gradiente de y = x^2 no ponto x = 5
x = torch.tensor(5., dtype=torch.float32, requires_grad=True)
y = (x ** 2).mean()
# executa o backward para calcular os gradientes dy/dx
y.backward()

# compare com o resultado real da derivada de x^2 que eh 2*x
print(x.grad)

# 1 - EXTRA) estimar o gradiente de y = x^2 em varios pontos x
pontos_x = torch.tensor([-2., -1., 1., 4.], dtype=torch.float32, requires_grad=True)
y = (pontos_x ** 2)
z = y.sum()
z.backward()

# compare com o resultado da derivada de x^2 que 2*x
print(pontos_x.grad)

# 2) estimar o gradiente de y = (3 * x + 2) no ponto x = 5
x.grad.zero_()
# x = torch.tensor(5., dtype=torch.float32, requires_grad=True)
y = (3 * x + 2).sum()
y.backward()

# compare como resultado real da derivada de 3*x+2 que eh 3
print(x.grad)