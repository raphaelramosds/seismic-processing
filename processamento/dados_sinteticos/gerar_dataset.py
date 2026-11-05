"""Gera um dataset de patches SU para separacao de difracoes

Para cada modelo de refletividade sorteado:
  - posiciona `ndif` difracoes sobre cada um dos `nrefl` refletores;
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

def difracoes_por_refletor(topo, base, u, ndif, ns, vel):
    """Posiciona ndif apices de difracao sobre cada refletor (tempos relativos u)"""
    ntr = topo.size
    dif = np.zeros((ns, ntr))
    apices = []
    for uk in u:
        # tempo (em amostras) do refletor k em cada traco
        tk = topo + uk * (base - topo)

        # tracos em que o refletor esta dentro do grid
        # NOTE: ignora t0 < 1 para evitar hiperbole degenerada
        validos = np.flatnonzero((tk >= 1) & (tk < ns - 1))
        if validos.size == 0:
            continue

        for x0 in rd.rng.choice(validos, size=ndif, replace=validos.size < ndif):
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
    for nome in ("nmodelos", "nrefl", "npatches", "ns", "ntr"):
        if not isinstance(cfg[nome], int) or cfg[nome] <= 0:
            raise ValueError(f"{nome} deve ser um inteiro positivo")
    if not isinstance(cfg["ndif"], int) or cfg["ndif"] < 0:
        raise ValueError("ndif deve ser um inteiro >= 0")
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
    total_dif = 0

    for m in tqdm(range(args.nmodelos), desc="gerando modelos", unit="modelo"):
        u = sorteia_u(args.nrefl)
        refl, topo, base = modelo_refletividade(args.ns, args.ntr, args.nrefl, u=u)
        dif, apices = difracoes_por_refletor(topo, base, u, args.ndif, args.ns, rd.vel)
        total_dif += len(apices)

        _, secao_dif, secao_total, secao_ruidosa = sintetiza_secoes(refl, dif, dt=args.dt)
        secao_data = secao_total if args.sem_ruido else secao_ruidosa

        patches_data = extrai_patches(secao_data, args.npatches)
        patches_label = extrai_patches(secao_dif, args.npatches)
        for p, (pd, pl) in enumerate(zip(patches_data, patches_label)):
            nome = f"modelo_{m:04d}_patch_{p:02d}.su"
            salva_su(pd, args.dt, os.path.join(dir_data, nome))
            salva_su(pl, args.dt, os.path.join(dir_label, nome))

    print(f"{args.nmodelos} modelos, {total_dif} difracoes, "
          f"{args.nmodelos * args.npatches} pares de patches salvos em {args.saida}/{{data,label}}")

if __name__ == "__main__":
    main()
