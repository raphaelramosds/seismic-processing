import numpy as np


def group_norm(x, gamma, beta, G, eps=1e-5):
    """
    Group Normalization

    Args.
        x (np.ndarray): entrada com shape (N, C, H, W)
        gamma (np.ndarray): escala aprendida por canal, shape (1, C, 1, 1)
        beta (np.ndarray): deslocamento aprendido por canal, shape (1, C, 1, 1)
        G (int): numero de grupos. C deve ser divisivel por G
        eps (float): constante para estabilidade numerica

    Note.
        1. A BatchNorm calcula media e variancia ao longo do batch (N), entao seu erro aumenta muito com batches pequenos
        2. A GroupNorm divide os C canais em G grupos e calcula media e variancia dentro de cada grupo,
           para cada amostra separadamente. Assim, o resultado nao depende do tamanho do batch
        3. Casos extremos: G = 1 equivale a LayerNorm e G = C equivale a InstanceNorm
    """
    N, C, H, W = x.shape
    assert C % G == 0, "C deve ser divisivel por G"

    # agrupar os canais: cada grupo tem C // G canais
    x = x.reshape(N, G, C // G, H, W)

    # media e variancia sobre os canais do grupo e as dimensoes espaciais (C//G, H, W)
    mean = x.mean(axis=(2, 3, 4), keepdims=True)
    var = x.var(axis=(2, 3, 4), keepdims=True)

    x = (x - mean) / np.sqrt(var + eps)

    # voltar ao shape original e aplicar a transformacao afim por canal
    x = x.reshape(N, C, H, W)
    return x * gamma + beta


if __name__ == "__main__":
    np.random.seed(42)

    N, C, H, W = 2, 32, 8, 8
    G = 8

    x = np.random.randn(N, C, H, W) * 3 + 5
    gamma = np.ones((1, C, 1, 1))
    beta = np.zeros((1, C, 1, 1))

    out = group_norm(x, gamma, beta, G)

    # cada grupo de cada amostra deve ter media ~0 e variancia ~1
    grupos = out.reshape(N, G, -1)
    print("output:", out.shape)
    print("media por grupo ~ 0:", np.allclose(grupos.mean(axis=-1), 0))
    print("variancia por grupo ~ 1:", np.allclose(grupos.var(axis=-1), 1, atol=1e-3))

    # a saida de uma amostra nao depende das outras amostras do batch
    out_sozinha = group_norm(x[:1], gamma, beta, G)
    print("independente do batch:", np.allclose(out[:1], out_sozinha))

    # comparar com a implementacao do PyTorch, se estiver instalado
    try:
        import torch
        import torch.nn as nn

        gn = nn.GroupNorm(num_groups=G, num_channels=C, eps=1e-5)
        out_torch = gn(torch.from_numpy(x).float()).detach().numpy()
        print("igual ao nn.GroupNorm:", np.allclose(out, out_torch, atol=1e-4))
    except ImportError:
        print("torch nao instalado, comparacao com nn.GroupNorm ignorada")
