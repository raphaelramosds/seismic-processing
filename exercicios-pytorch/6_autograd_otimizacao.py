# PARTE 2 - AUTOGRAD E OTIMIZACAO

# Exercicio 6 - Ajustar uma reta
# -----------------------------
# Crie dados sinteticos seguindo aproximadamente:

#     y = 3 * x + 2

# Crie dois parametros treinaveis, w e b, e defina:

#     y_pred = w * x + b

# Use MSELoss e o otimizador SGD ou Adam para aprender w e b.

# Requisitos:
# - execute pelo menos 100 iteracoes;
# - imprima a loss a cada 10 iteracoes;
# - mostre os valores finais de w e b.

# Resultado esperado: w proximo de 3 e b proximo de 2.

import torch

# inclinacao e bias da funcao linear y = m * x + bias
m=3.0
bias=2.0

# numero de amostras
epochs=100
ns=10

# dataset
ruido = torch.randn(ns, 1) * 0.1
x = torch.randn(ns, 1)
y_real = (m * x + bias) + ruido

# modelo: inferir w e b
w = torch.rand(1, requires_grad=True)
b = torch.rand(1, requires_grad=True)

otimizador = torch.optim.SGD([w, b], lr=0.01, momentum=0.9)
loss_fn = torch.nn.MSELoss()

for t in range(1,epochs):
    # forward
    y_pred = w * x + b

    # calculo da perda
    loss = loss_fn(y_pred, y_real)

    # zerar gradientes acumulados
    otimizador.zero_grad()

    # calcula gradientes de w e b com backpropagation
    loss.backward()

    # atualiza w e b
    otimizador.step()

    if t % 10 == 0:
        print(f"epoca {t}: MSE = {loss.item():.4f}")
        # (opcional) exibir gradientes
        # print(f"gradW = {w.grad.item():.4f}, gradB = {b.grad.item():.4f}")

# testar com um ponto qualquer
x_teste = -1.0
y_teste = m*x_teste + bias
y_teste_pred = w.item() * x_teste + b.item()
print(f"Real: {y_teste} | Pred: {y_teste_pred:.3f}")