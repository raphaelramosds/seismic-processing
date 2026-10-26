import numpy as np
import matplotlib.pyplot as plt

from refletividade_2d import modelo_refletividade
from helper import pulso_ricker, convolve_secao, adiciona_ruido_snr, salva_su

ns=256          # amostras
ntr=256         # tracos
nrefl=70        # numero de refletores
dt=0.006        # taxa amostragem
dx=12.5         # espacamento entre tracos (m)
ndif=(5, 20)    # intervalo do numero de difracoes
vel=(1500, 5000) # intervalo de velocidades (m/s): controla a abertura da hiperbole

# gerador de numeros aleatorios
rng = np.random.default_rng()

def modelo_difracoes(refl, ndif, vel):
    """Gera refletividade de difracoes com apices posicionados sobre os refletores"""
    ns, ntr = refl.shape
    dif = np.zeros((ns, ntr))
    tracos = np.arange(ntr)

    # numero de hiperboles
    n = rng.integers(ndif[0], ndif[1] + 1)

    apices = []
    for _ in range(n):
        # sorteia qual traco vai receber o apice (apex) da hiperbole
        x0 = rng.integers(ntr)

        # sorteia o tempo do apice (em amostras) entre as amostras do traco x0 que contem refletor
        cand = np.flatnonzero(np.abs(refl[1:, x0]) > 0.05) + 1
        if cand.size == 0:
            # NOTE: ignora a amostra 0 para evitar t0 = 0 (hiperbole degenerada)
            continue
        t0 = rng.choice(cand)

        # abertura da hiperbole: quanto maior a velocidade, mais aberta
        v = rng.uniform(*vel)

        # amplitude da difracao: bem menor que a das reflexoes
        amp = rng.choice([-1, 1]) * rng.uniform(0.05, 0.3)

        # tempo de transito da difracao (em amostras)
        # t(x) = sqrt(t0^2 + (2 (x - x0) dx / v)^2)
        t0_s = t0 * dt
        tk = np.sqrt(t0_s ** 2 + (2 * (tracos - x0) * dx / v) ** 2) / dt

        # energia decresce com a distancia ao apice:
        # espalhamento geometrico (t0 / t) e atenuacao lateral gaussiana
        largura = rng.uniform(0.05, 0.3) * ntr
        decai = (t0 / tk) * np.exp(-0.5 * ((tracos - x0) / largura) ** 2)

        # distribui a amplitude entre as amostras vizinhas (mesmo esquema da refletividade)
        i0 = np.floor(tk).astype(int)
        w = tk - i0
        for i, peso in ((i0, 1 - w), (i0 + 1, w)):
            ok = (i >= 0) & (i < ns)
            dif[i[ok], tracos[ok]] += amp * decai[ok] * peso[ok]

        apices.append((x0, t0))

    return dif, apices

if __name__ == "__main__":
    refl, topo, base = modelo_refletividade(ns, ntr, nrefl=nrefl)
    dif, apices = modelo_difracoes(refl, ndif, vel)

    # reflexoes: ricker com frequencias mais baixas
    _, ricker_refl = pulso_ricker(rng.uniform(10, 40), dt, ns)
    ricker_refl *= rng.uniform(0.5, 1.5)
    secao_refl = convolve_secao(refl, ricker_refl)

    # difracoes: ricker com frequencias mais altas que as das reflexoes
    _, ricker_dif = pulso_ricker(rng.uniform(40, 70), dt, ns)
    ricker_dif *= rng.uniform(0.5, 1.5)
    secao_dif = convolve_secao(dif, ricker_dif)

    # campo de onda completo (reflexoes + difracoes) com ruido gaussiano
    secao_total = secao_refl + secao_dif
    secao_total_ruidosa = adiciona_ruido_snr(secao_total, snr_db=rng.uniform(5, 20), rng=rng)

    # visualizacao modelos de refletividade
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].imshow(refl, aspect="auto", cmap="seismic", vmin=-1, vmax=1)
    axs[0].set_title("Refletividade das reflexoes")
    vmax = np.abs(dif).max()
    axs[1].imshow(dif, aspect="auto", cmap="seismic", vmin=-vmax, vmax=vmax)
    axs[1].plot(*zip(*apices), "k.", ms=4)
    axs[1].set_title("Refletins, ntr, nrefl, dt, rng,vidade das difracoes (apices em preto)")
    for ax in axs:
        ax.set_xlabel("Traco")
        ax.set_ylabel("Amostra")

    plt.tight_layout()
    plt.savefig("imagens/refletividade_2d_difracoes.jpg", dpi=150, bbox_inches="tight")
    # plt.show()

    # visualizacao secoes convoluidas
    secoes = (
        (secao_refl, "Reflexoes"),
        (secao_dif, "Difracoes"),
        (secao_total, "Reflexoes + difracoes"),
        (secao_total_ruidosa, "Reflexoes + difracoes (ruidosa)"),
    )
    fig, axs = plt.subplots(1, 4, figsize=(20, 5))
    for ax, (s, titulo) in zip(axs, secoes):
        vmax = np.abs(s).max()
        ax.imshow(s, aspect="auto", cmap="seismic", vmin=-vmax, vmax=vmax)
        ax.set_title(titulo)
        ax.set_xlabel("Traco")
        ax.set_ylabel("Amostra")

    plt.tight_layout()
    plt.savefig("imagens/secao_2d_difracoes.jpg", dpi=150, bbox_inches="tight")
    # plt.show()

    # exporta secoes em SU (little-endian)
    salva_su(secao_refl, dt, "su/secao_2d_reflexoes.su")
    salva_su(secao_dif, dt, "su/secao_2d_difracoes.su")
    salva_su(secao_total, dt, "su/secao_2d_total.su")
    salva_su(secao_total_ruidosa, dt, "su/secao_2d_total_ruidosa.su")
