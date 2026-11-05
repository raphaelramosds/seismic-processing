"""Gera um dataset de patches SU para separacao de difracoes

Para cada modelo de refletividade sorteado:
  - sorteia o numero de refletores em `nrefl`;
  - sorteia, para cada refletor, quantas difracoes (`ndif`) ficam sobre ele;
  - sintetiza a secao (reflexoes + difracoes + ruido);
  - divide as secoes em `npatches` patches.

Estrutura de saida:
  <saida>/data/modelo_XXXX_patch_YY.su   -> dado completo (reflexoes + difracoes [+ ruido])
  <saida>/label/modelo_XXXX_patch_YY.su  -> apenas difracoes (sem ruido)

Uso (a partir de dados_sinteticos/):
  cp dataset-exemplo.json dataset.json  # dataset.json e ignorado pelo git
  python gerar_dataset.py dataset.json

Parametros do JSON (ver dataset-exemplo.json):
  obrigatorios: nmodelos, nrefl, ndif (por refletor), npatches (1 ou par)
  opcionais:    saida, ns, ntr, dt, sem_ruido, seed

  nrefl e ndif aceitam um inteiro (valor fixo) ou [min, max] (sorteio
  uniforme inclusivo: nrefl por modelo, ndif por refletor). Ex.:
    "nrefl": [5, 50]   # faixa do Algoritmo 3 de Zhang et al. (2024)
    "ndif": [0, 4]     # alguns refletores ficam sem difracao
"""
import os
import json
import argparse
import numpy as np
from tqdm import tqdm

import refletividade_2d
import refletividade_2d_difracoes as rd
from refletividade_2d import modelo_refletividade, sorteia_u
from refletividade_2d_difracoes import adiciona_difracao, sintetiza_secoes
from patches_2d import extrai_patches
from utils import salva_su

def sorteia(intervalo):
    """Sorteia um inteiro em [min, max] (inclusivo)

    Com min == max nao consome o gerador, preservando a reprodutibilidade
    de datasets gerados com valores fixos.
    """
    vmin, vmax = intervalo
    if vmin == vmax:
        return vmin
    return int(rd.rng.integers(vmin, vmax + 1))

def difracoes_por_refletor(topo, base, u, ndif, ns, vel):
    """Posiciona apices de difracao sobre cada refletor (tempos relativos u)

    ndif: (min, max) de difracoes por refletor, sorteado para cada refletor
    """
    ntr = topo.size
    dif = np.zeros((ns, ntr))
    apices = []
    for uk in u:
        n = sorteia(ndif)
        if n == 0:
            continue

        # tempo (em amostras) do refletor k em cada traco
        tk = topo + uk * (base - topo)

        # tracos em que o refletor esta dentro do grid
        # NOTE: ignora t0 < 1 para evitar hiperbole degenerada
        validos = np.flatnonzero((tk >= 1) & (tk < ns - 1))
        if validos.size == 0:
            continue

        for x0 in rd.rng.choice(validos, size=n, replace=validos.size < n):
            adiciona_difracao(dif, x0, tk[x0], vel)
            apices.append((x0, tk[x0]))
    return dif, apices

# parametros opcionais do JSON e seus valores padrao
PADROES = {
    "saida": "su/dataset",  # diretorio de saida
    "ns": rd.ns,            # amostras por traco
    "ntr": rd.ntr,          # numero de tracos
    "dt": rd.dt,            # taxa de amostragem (s)
    "sem_ruido": False,     # data sem ruido gaussiano
    "seed": None,           # semente para reprodutibilidade
}
OBRIGATORIOS = ("nmodelos", "nrefl", "ndif", "npatches")

def le_intervalo(cfg, nome, minimo):
    """Converte cfg[nome] (inteiro ou [min, max]) na tupla (min, max)"""
    valor = cfg[nome]
    eh_int = lambda v: isinstance(v, int) and not isinstance(v, bool)
    if eh_int(valor):
        valor = [valor, valor]
    if (not isinstance(valor, list) or len(valor) != 2 or not all(map(eh_int, valor))
            or valor[0] < minimo or valor[0] > valor[1]):
        raise ValueError(f"{nome} deve ser um inteiro >= {minimo} ou [min, max] com {minimo} <= min <= max")
    return tuple(valor)

def le_config(arquivo):
    """Le e valida os parametros do JSON, completando os opcionais com PADROES"""
    with open(arquivo) as f:
        cfg = json.load(f)

    faltando = [k for k in OBRIGATORIOS if k not in cfg]
    if faltando:
        raise ValueError(f"parametros obrigatorios ausentes: {', '.join(faltando)}")
    desconhecidos = set(cfg) - set(OBRIGATORIOS) - set(PADROES)
    if desconhecidos:
        raise ValueError(f"parametros desconhecidos: {', '.join(sorted(desconhecidos))}")

    cfg = {**PADROES, **cfg}
    for nome in ("nmodelos", "npatches", "ns", "ntr"):
        if not isinstance(cfg[nome], int) or cfg[nome] <= 0:
            raise ValueError(f"{nome} deve ser um inteiro positivo")
    cfg["nrefl"] = le_intervalo(cfg, "nrefl", 1)
    cfg["ndif"] = le_intervalo(cfg, "ndif", 0)
    if cfg["npatches"] != 1 and cfg["npatches"] % 2 != 0:
        raise ValueError("npatches deve ser 1 ou um numero par")
    return argparse.Namespace(**cfg)

def main():
    parser = argparse.ArgumentParser(description="Gera dataset SU (data/label) de difracoes em patches")
    parser.add_argument("config", help="arquivo JSON com os parametros do dataset")
    try:
        args = le_config(parser.parse_args().config)
    except (OSError, ValueError) as e:
        parser.error(str(e))

    # mesmo gerador em todos os modulos (reprodutibilidade com --seed)
    rng = np.random.default_rng(args.seed)
    refletividade_2d.rng = rng
    rd.rng = rng

    dir_data = os.path.join(args.saida, "data")
    dir_label = os.path.join(args.saida, "label")
    total_refl = total_dif = sem_dif = 0

    for m in tqdm(range(args.nmodelos), desc="gerando modelos", unit="modelo"):
        nrefl = sorteia(args.nrefl)
        u = sorteia_u(nrefl)
        refl, topo, base = modelo_refletividade(args.ns, args.ntr, nrefl, u=u)
        dif, apices = difracoes_por_refletor(topo, base, u, args.ndif, args.ns, rd.vel)
        total_refl += nrefl
        total_dif += len(apices)
        sem_dif += len(apices) == 0

        _, secao_dif, secao_total, secao_ruidosa = sintetiza_secoes(refl, dif, dt=args.dt)
        secao_data = secao_total if args.sem_ruido else secao_ruidosa

        patches_data = extrai_patches(secao_data, args.npatches)
        patches_label = extrai_patches(secao_dif, args.npatches)
        for p, (pd, pl) in enumerate(zip(patches_data, patches_label)):
            nome = f"modelo_{m:04d}_patch_{p:02d}.su"
            salva_su(pd, args.dt, os.path.join(dir_data, nome))
            salva_su(pl, args.dt, os.path.join(dir_label, nome))

    print(f"{args.nmodelos} modelos, {total_refl} refletores, {total_dif} difracoes "
          f"({sem_dif} modelos sem difracao), "
          f"{args.nmodelos * args.npatches} pares de patches salvos em {args.saida}/{{data,label}}")

if __name__ == "__main__":
    main()
