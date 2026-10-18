import numpy as np

linha = 100     # extensao da superficie onde a aquisicao foi feita (metros)
dxs = 20        # tiro por metro
dxg = dxs//2    # receptor por metro

xs = np.arange(dxs,linha + dxs, dxs)     # posicao dos tiros
xg = np.arange(dxg, linha + dxg, dxg)    # posicao dos tracos/gathers

XS, XG = np.meshgrid(xs, xg)

matriz_cmp = (XS + XG)/2
matriz_offset = (XS - XG)/2

def extract_cmp(n, cmp: np.array, offset: np.array):
    mask = (cmp == n)
    return n, offset[mask]

# visualizacao da qtde de gathers em cada CMP
for n in xs:
    cmp_no, offsets = extract_cmp(n, matriz_cmp, matriz_offset)
    print(f"O CMP {cmp_no} contem os tracos/gathers com offset (metros): {offsets}")