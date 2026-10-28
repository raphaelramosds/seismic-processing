import numpy as np

def self_attention(X, W_q, W_k, W_v):
    """Aplica self-attention em uma entrada X"""
    batch_size, seq_len, d_model = X.shape
    d_k = d_model

    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v

    # se K.shape = (1,3,4), entao K.transpose(0,2,1) vai trocar a terceira dimensao (4) com a segunda (3)
    # entao, o K transposto vai ter shape (1,4,3)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)

    # softmax estavel: subtrair o maximo de cada linha garante expoentes <= 0, evitando overflow do np.exp
    scores = scores - scores.max(axis=-1, keepdims=True)

    # pesos da camada de atencao: scores normalizados
    attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)

    output = attention_weights @ V

    return output, attention_weights

def positional_encoding(seq_len, d_model):
    """
    Matriz de Positional Encoding (PE) para ser somado ao array de entrada X

    Args.
        seq_len (int): tamanho da sequencia da entrada
        d_model (int): dimensao do vetor de cada token
        
        E.g, para uma entrada (1,128,128) sao 128 (seq_len) tokens cada um com 128 features (d_model)

    Note. 
        1. A self-attention nao sabe a ordem dos tokens. Se embaralharmos as linhas de X, a saida sai embaralhada mesmo jeito
        2. Em muitos problemas, a ordem importa, por exemplo:
            - Na semantica: "o cao mordeu o homem" e "o homem mordeu o cao" sao diferentes
            - Nos dados sismicos: a amostra no tempo 100ms nao eh a mesma coisa que a amostra em 2s, e a ordem dos tracos tambem carrega informacao
        3. O PE deve ser somado a X antes de coloca-lo na camada de atencao (self_attention)
    """
    pos = np.arange(seq_len)[:, None]   # (seq_len, 1)
    i = np.arange(0, d_model, 2)        # indices pares: 0, 2, 4, ...
    div = 10000 ** (i / d_model)        # (d_model/2,)

    pe = np.zeros((seq_len, d_model))
    pe[:, 0::2] = np.sin(pos / div)                     # colunas pares
    pe[:, 1::2] = np.cos(pos / div)[:, :d_model // 2]   # colunas ímpares
    return pe

if __name__ == "__main__":
    np.random.seed(42)

    X = np.random.rand(1, 128, 128)
    batch_size, seq_len, d_model = X.shape

    # inicializar os pesos de query, key e value
    # NOTE: colocar Q, K e V na mesma escala de X normalizando por sqrt(d_model)
    W_q = np.random.randn(d_model, d_model) / np.sqrt(d_model)
    W_k = np.random.randn(d_model, d_model) / np.sqrt(d_model)
    W_v = np.random.randn(d_model, d_model) / np.sqrt(d_model)

    # aplicar encoding posicional
    X_encoded = positional_encoding(seq_len=seq_len, d_model=d_model)

    # colocar no bloco de self attention os tokens somados ao positional encoding
    output, weights = self_attention(X + X_encoded, W_q, W_k, W_v)

    print("x encoded:", X_encoded.shape)
    print("\noutput: ", output.shape)
    print("\nattention weights: ", weights.shape)

    perm = np.random.permutation(seq_len)

    # teste sem PE: as saidas sao as mesmas, independente se esta embaralhado
    # entao, sem PE, a rede nao respeita a ordem das features
    out, _ = self_attention(X, W_q, W_k, W_v)
    out_perm, _ = self_attention(X[:, perm], W_q, W_k, W_v)
    print("sem PE, ordem ignorada:", np.allclose(out[:, perm], out_perm))

    # com PE: o PE fica fixo nas posicoes, entao embaralhar os tokens muda a saida
    out, _ = self_attention(X + X_encoded, W_q, W_k, W_v)
    out_perm, _ = self_attention(X[:, perm] + X_encoded, W_q, W_k, W_v)
    print("com PE, ordem ignorada:", np.allclose(out[:, perm], out_perm))