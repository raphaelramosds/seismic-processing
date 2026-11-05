import numpy as np


def _eixos(x):
    """
    Eixos sobre os quais as estatisticas do mini-batch sao calculadas

    Note.
        1. Camada totalmente conectada (N, D): normaliza cada ativacao sobre o batch, eixo 0
        2. Camada convolucional (N, C, H, W): normaliza cada canal sobre o batch e as posicoes espaciais,
           eixos (0, 2, 3). O mini-batch efetivo tem tamanho m' = N * H * W
    """
    return (0,) if x.ndim == 2 else (0, 2, 3)


def batch_norm(x, gamma, beta, eps=1e-5):
    """
    Batch Normalizing Transform durante o treino

    Args.
        x (np.ndarray): entrada com shape (N, D) ou (N, C, H, W)
        gamma (np.ndarray): escala aprendida, shape (1, D) ou (1, C, 1, 1)
        beta (np.ndarray): deslocamento aprendido, shape (1, D) ou (1, C, 1, 1)
        eps (float): constante somada a variancia para estabilidade numerica

    Returns.
        y (np.ndarray): saida normalizada, mesmo shape de x
        cache (tuple): valores intermediarios usados no backpropagation

    Note.
        1. A media e a variancia sao do mini-batch, entao a saida de uma amostra depende das outras amostras do batch
        2. gamma e beta permitem que a camada represente a identidade: com gamma = sqrt(Var[x]) e beta = E[x]
           recuperamos as ativacoes originais
    """
    eixos = _eixos(x)
    
    mu = x.mean(axis=eixos, keepdims=True)  # media do mini-batch
    var = ((x - mu) ** 2).mean(axis=eixos, keepdims=True)  # variancia do mini-batch
    x_hat = (x - mu) / np.sqrt(var + eps)  # normalizar
    y = gamma * x_hat + beta  # escalar e deslocar

    cache = (x, x_hat, mu, var, gamma, eps)
    return y, cache


def batch_norm_backward(dy, cache):
    """
    Gradientes do Batch Normalizing Transform pela regra da cadeia (secao 3 do artigo)

    Args.
        dy (np.ndarray): gradiente da perda em relacao a saida y
        cache (tuple): retornado por batch_norm

    Returns.
        dx, dgamma, dbeta (np.ndarray): gradientes em relacao a x, gamma e beta
    """
    x, x_hat, mu, var, gamma, eps = cache
    eixos = _eixos(x)
    m = x.size // gamma.size  # tamanho do mini-batch (efetivo, no caso convolucional)

    dx_hat = dy * gamma
    dvar = (
        np.sum(dx_hat * (x - mu), axis=eixos, keepdims=True)
        * -0.5
        * (var + eps) ** -1.5
    )
    dmu = (
        np.sum(dx_hat * -1 / np.sqrt(var + eps), axis=eixos, keepdims=True)
        + dvar * np.sum(-2 * (x - mu), axis=eixos, keepdims=True) / m
    )
    dx = dx_hat / np.sqrt(var + eps) + dvar * 2 * (x - mu) / m + dmu / m
    dgamma = np.sum(dy * x_hat, axis=eixos, keepdims=True)
    dbeta = np.sum(dy, axis=eixos, keepdims=True)

    return dx, dgamma, dbeta


def estatisticas_populacao(batches):
    """
    Media e variancia da populacao a partir de varios mini-batches de treino (Algoritmo 2, passo 10)

    Args.
        batches (list[np.ndarray]): mini-batches de mesmo tamanho m

    Returns.
        media (np.ndarray): E[x] = E_B[mu_B]
        var (np.ndarray): Var[x] = m / (m - 1) * E_B[sigma_B^2], estimativa nao enviesada
    """
    eixos = _eixos(batches[0])
    mus = [b.mean(axis=eixos, keepdims=True) for b in batches]
    m = (
        batches[0].size // mus[0].size
    )  # tamanho do mini-batch (efetivo, no caso convolucional)

    vars_ = [b.var(axis=eixos, keepdims=True) for b in batches]

    media = np.mean(mus, axis=0)
    var = m / (m - 1) * np.mean(vars_, axis=0)
    return media, var


def batch_norm_inferencia(x, gamma, beta, media, var, eps=1e-5):
    """
    Batch Normalization na inferencia (Algoritmo 2, passo 11)

    Note.
        1. Usa as estatisticas da populacao, nao do mini-batch, entao a saida depende apenas da entrada
        2. Com media e variancia fixas, a normalizacao vira uma unica transformacao linear:
           y = gamma / sqrt(Var[x] + eps) * x + (beta - gamma * E[x] / sqrt(Var[x] + eps))
    """
    escala = gamma / np.sqrt(var + eps)
    return escala * x + (beta - escala * media)


if __name__ == "__main__":
    np.random.seed(42)

    N, C, H, W = 8, 4, 5, 5
    x = np.random.randn(N, C, H, W) * 3 + 5
    gamma = np.ones((1, C, 1, 1))
    beta = np.zeros((1, C, 1, 1))

    y, cache = batch_norm(x, gamma, beta)

    print("output:", y.shape)
    # cada canal deve ter media ~0 e variancia ~1 sobre (N, H, W)
    # NOTE: o shape (N,C,H,W) tem eixos 0, 1, 2 e 3, entao em (0,2,3) observe que
    # estamos omitindo a dimensao do canal (eixo = 1). Portanto, a media aqui eh
    # calculada por canal.
    print("media por canal ~ 0:", np.allclose(y.mean(axis=(0, 2, 3)), 0))
    print("variancia por canal ~ 1:", np.allclose(y.var(axis=(0, 2, 3)), 1, atol=1e-3))

    # a saida de uma amostra depende do resto do batch
    y_sozinha, _ = batch_norm(x[:2], gamma, beta)
    print("depende do batch:", not np.allclose(y[:2], y_sozinha))

    # identidade: com gamma = sqrt(var + eps) e beta = media, recuperamos x
    _, _, mu, var, _, eps = cache
    y_id, _ = batch_norm(x, np.sqrt(var + eps), mu)
    print("representa a identidade:", np.allclose(y_id, x))

    # conferir o backward com gradiente numerico, usando a perda L = sum(y * dy)
    gamma = np.random.randn(1, C, 1, 1)
    beta = np.random.randn(1, C, 1, 1)
    dy = np.random.randn(N, C, H, W)
    _, cache = batch_norm(x, gamma, beta)
    dx, dgamma, dbeta = batch_norm_backward(dy, cache)

    def gradiente_numerico(f, p, h=1e-5):
        grad = np.zeros_like(p)
        for idx in np.ndindex(p.shape):
            original = p[idx]
            p[idx] = original + h
            mais = f()
            p[idx] = original - h
            menos = f()
            p[idx] = original
            grad[idx] = (mais - menos) / (2 * h)
        return grad

    perda = lambda: np.sum(batch_norm(x, gamma, beta)[0] * dy)
    print("dx correto:", np.allclose(dx, gradiente_numerico(perda, x), atol=1e-5))
    print(
        "dgamma correto:",
        np.allclose(dgamma, gradiente_numerico(perda, gamma), atol=1e-5),
    )
    print(
        "dbeta correto:", np.allclose(dbeta, gradiente_numerico(perda, beta), atol=1e-5)
    )

    # inferencia: estatisticas da populacao estimadas a partir de varios mini-batches
    batches = [np.random.randn(N, C, H, W) * 3 + 5 for _ in range(200)]
    media, var = estatisticas_populacao(batches)
    print("media da populacao ~ 5:", np.allclose(media, 5, atol=0.1))
    print("variancia da populacao ~ 9:", np.allclose(var, 9, atol=0.3))

    # na inferencia, a saida de uma amostra nao depende do batch
    y_inf = batch_norm_inferencia(x, gamma, beta, media, var)
    y_inf_sozinha = batch_norm_inferencia(x[:2], gamma, beta, media, var)
    print("inferencia independente do batch:", np.allclose(y_inf[:2], y_inf_sozinha))

    # camada totalmente conectada (N, D)
    x_fc = np.random.randn(16, 10) * 2 - 1
    y_fc, _ = batch_norm(x_fc, np.ones((1, 10)), np.zeros((1, 10)))
    print(
        "FC media ~ 0 e variancia ~ 1:",
        np.allclose(y_fc.mean(axis=0), 0)
        and np.allclose(y_fc.var(axis=0), 1, atol=1e-3),
    )
