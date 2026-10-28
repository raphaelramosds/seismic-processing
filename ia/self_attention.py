import numpy as np

def self_attention(X):
    """Aplica self-attention em uma entrada X"""

    batch_size, seq_len, d_model = X.shape

    d_k = d_model
    W_q = np.random.randn(d_model, d_k)
    W_k = np.random.randn(d_model, d_k)
    W_v = np.random.randn(d_model, d_k)

    Q = X @ W_q
    K = X @ W_k
    V = X @ W_k

    # Se K.shape = (1,3,4), entao K.transpose(0,2,1) vai trocar a terceira dimensao (4) com a segunda (3)
    # Entao, o K transposto vai ter shape (1,4,3)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)

    attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)

    output = attention_weights @ V

    return output, attention_weights

np.random.seed(42)

X = np.random.rand(1, 128, 128)

output, weights = self_attention(X)

print("output: ", output.shape)

print("\nattention weights: ", weights.shape)