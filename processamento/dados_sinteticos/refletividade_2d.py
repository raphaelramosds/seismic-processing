import numpy as np

from utils import pulso_ricker, convolve_secao, adiciona_ruido_snr, salva_su

ns=256      # amostras
ntr=256     # tracos
nrefl=10    # numero de refletores
dt=0.006    # taxa amostragem

# limites relativos (%) do topo e base para posicao dos refletores
# t1 e t2: quanto menores, mais perto do topo do gri
# b1 e b2: quanto maiores, mais perto da base do  grid
t1, t2 = 0.3, 0.4
b1, b2 = 0.9, 0.99

# gerador de numeros aleatorios
rng = np.random.default_rng()

def tendencia_senoidal(ntr: int, t_medio: float, amp_max: float):
    """Curva t(x) = t_medio + A sin(2 pi x / comp + fase), em amostras"""
    x = np.arange(ntr)
    # amplitude da ondulacao 
    amp = rng.uniform(0, amp_max)
    # comprimento de onda
    comp = rng.uniform(0.5 * ntr, 3 * ntr)
    fase = rng.uniform(0, 2 * np.pi)
    return t_medio + amp * np.sin(2 * np.pi * x / comp + fase)

def modelo_refletividade(ns, ntr, nrefl):
    """Preenche a secao com refletores que seguem duas tendencias senoidais"""
    # coordenadas relativas ao grid do topo e base dos pontos nas tendencias senoidais
    topo = tendencia_senoidal(ntr, rng.uniform(t1, t2) * ns, 0.1 * ns)
    base = tendencia_senoidal(ntr, rng.uniform(b1, b2) * ns, 0.1 * ns)

    # tempo relativo u dos refletores (nrefl, ) 
    # u = 0 (refletor exatamente no topo)
    # u = 1 (exatamente na base)
    # u < 0 (acima do topo) e u > 1 (acima da base)
    u = np.sort(rng.uniform(-0.1, 1.1, nrefl))

    # amplitude dos refletores (nrefl, )
    amps = rng.uniform(-1, 1, nrefl)

    refl = np.zeros((ns, ntr))
    tracos = np.arange(ntr)

    # distribui refletor posicionado em uk com amplitude ak
    for uk, ak in zip(u, amps):
        # tempo (em amostras) do refletor k em cada traco
        tk = topo + uk * (base - topo)

        # o refletor tk pode n ser exato, entao truncamos ele para obter um indice inteiro
        # Visualizacao: (i0 = 9) ---- (tk = 9.3) ---- (i0+1 = 10)
        i0 = np.floor(tk).astype(int)

        # calculamos a distancia ate o refletor
        w = tk - i0

        # propagamos em i0 (com peso de amplitude maior: 1-w) e no vizinho i0+1 (amplitude menor: w)
        # NOTE: a amostra mais proxima do refletor tk recebe mais amplitude.
        for i, peso in ((i0, 1 - w), (i0 + 1, w)):
            # extrai quais indices estao dentro dos limites da imagem
            ok = (i >= 0) & (i < ns)
            # splice para preencher o grid nos indices validas
            refl[i[ok], tracos[ok]] += ak * peso[ok]

    return refl, topo, base

if __name__ == "__main__":
    refl, topo, base = modelo_refletividade(ns, ntr, nrefl=nrefl)

    # convolucao de cada traco com a mesma ricker
    _, ricker = pulso_ricker(rng.uniform(10, 40), dt, ns)
    # ricker *= rng.uniform(0.5, 1.5) # ganho de energia
    secao = convolve_secao(refl, ricker)

    # aplica ruido gaussiano
    secao_ruidosa = adiciona_ruido_snr(secao, snr_db=rng.uniform(5, 20), rng=rng)

    # exporta secoes em SU (little-endian)
    salva_su(secao, dt, "su/secao_2d.su")
    salva_su(secao_ruidosa, dt, "su/secao_2d_ruidosa.su")
