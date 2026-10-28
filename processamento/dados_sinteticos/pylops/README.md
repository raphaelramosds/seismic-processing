# Exemplos pylops

Referência: https://pylops.readthedocs.io/en/stable/gallery/plot_seismicevents.html


### Eixos (`par`)

Os eixos são criados por `makeaxis(par)`, que segue a convenção `o` (origem), `d` (amostragem) e `n` (número de amostras):

| Parâmetro | Valor | Significado |
|-----------|-------|-------------|
| `ox`, `dx`, `nx` | -200, 2, 201 | Eixo x (offset/inline) em metros: de -200 a 200 m, a cada 2 m |
| `oy`, `dy`, `ny` | -100, 2, 101 | Eixo y (crossline, usado só no 3D) em metros: de -100 a 100 m, a cada 2 m |
| `ot`, `dt`, `nt` | 0, 0.004, 501 | Eixo do tempo em segundos: de 0 a 2 s, amostragem de 4 ms |
| `f0` | 20 | Frequência de pico (Hz) da wavelet Ricker |
| `nfmax` | 210 | Índice máximo de frequência; herdado do exemplo original, não é usado por `makeaxis` nem pelas funções chamadas aqui |

### Parâmetros comuns aos eventos

Todos são listas com um valor por evento (aqui, 3 eventos):

| Parâmetro | Valor | Significado |
|-----------|-------|-------------|
| `t0` | [0.2, 0.7, 1.6] | Tempo de intercepto (s) de cada evento em `x = 0` (e `y = 0` no 3D) |
| `amp` | [1.0, 0.6, -2.0] | Amplitude de cada evento; o sinal negativo inverte a polaridade do terceiro |
| `wav` | Ricker acima | Wavelet convoluída com os spikes de cada evento |

Cada função retorna dois arrays: o dado com spikes (sem wavelet) e o dado convoluído com a wavelet (`...wav`).
No 2D, o formato é `(nx, nt)` (por isso o `.T` no `imshow`); no 3D, é `(ny, nx, nt)`.

### Eventos 2D

**Lineares** — `linear2d(x, t, v, t0, theta, amp, wav)`

$$t(x) = t_0 + \frac{\sin\theta}{v}\,x$$

- `v = 1500`: velocidade (m/s) usada para converter o ângulo em vagarosidade (slowness)
- `theta = [40, 0, -60]`: ângulo de mergulho (graus) de cada evento; 0 gera um evento horizontal, e valores positivos/negativos inclinam para lados opostos

**Parabólicos** — `parabolic2d(x, t, t0, px, pxx, amp, wav)`

$$t(x) = t_0 + p_x\,x + p_{xx}\,x^2$$

- `px = [0, 0, 0]`: termo linear (s/m); zero deixa as parábolas simétricas em torno de `x = 0`
- `pxx = [1e-5, 5e-6, 1e-6]`: curvatura (s/m²). Em `x = 200 m`, o moveout é de 0.4, 0.2 e 0.04 s, respectivamente

**Hiperbólicos** — `hyperbolic2d(x, t, t0, vrms, amp, wav)`

$$t(x) = \sqrt{t_0^2 + \frac{x^2}{v_{rms}^2}}$$

- `vrms = [500, 700, 1700]`: velocidade RMS (m/s) de cada evento; quanto menor, mais acentuada a hipérbole (simula o moveout normal — NMO — de um CMP)
