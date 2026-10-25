import numpy as np 

ns=256      # amostras
trl=256     # tracos
dt=0.006    # taxa amostragem

# gerador de numeros aleatorios
rng = np.random.default_rng()

def pulso_ricker(fp: float, dt: float, ns: int):
    """Gera pulso ricker com frequencia de pico fp amostrado em dt segundos com ns amostras"""
    a = (ns * dt) / 2
    t = np.arange(-a, a, dt)
    ft = (np.pi * fp * t) ** 2
    return t, (1.0 - 2.0 * ft) * np.exp(-ft)

def tendencia_senoidal(ntr, t_medio, amp_max):
    """Curva t(x) = t_medio + A sin(2 pi x / comp + fase), em amostras"""
    x = np.arange(ntr)
    amp = rng.uniform(0, amp_max)               # amplitude da ondulacao
    comp = rng.uniform(0.5 * ntr, 3 * ntr)      # comprimento de onda (em tracos)
    fase = rng.uniform(0, 2 * np.pi)
    return t_medio + amp * np.sin(2 * np.pi * x / comp + fase)