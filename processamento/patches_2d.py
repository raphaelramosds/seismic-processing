import os
import argparse
import numpy as np
from utils import le_su, salva_su

def grade_patches(n: int, ns: int, ntr: int):
    """Fatora n em (n_t, n_x) o mais proximo de uma grade quadrada/retangular"""
    quadrado = int(np.sqrt(n)) + 1

    # ache o primeiro d que for divisivel para n janelas
    a = max(d for d in range(1, quadrado) if n % d == 0)
    b = n // a

    # maior dimensao primeiro (retangulo horizontal)
    return (b, a) if ns >= ntr else (a, b)

def extrai_patches(secao: np.ndarray, n: int):
    """Divide a secao (ns, ntr) em n patches, percorrendo a grade linha a linha"""
    ns, ntr = secao.shape
    n_t, n_x = grade_patches(n, ns, ntr)
    if n_t > ns or n_x > ntr:
        raise ValueError(f"Grade {n_t}x{n_x} maior que a secao ({ns} amostras, {ntr} tracos)")
    return [
        bloco
        for faixa in np.array_split(secao, n_t, axis=0)
        for bloco in np.array_split(faixa, n_x, axis=1)
    ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide uma secao SU em N patches")
    parser.add_argument("arquivo", help="arquivo SU de entrada")
    parser.add_argument("n", type=int, help="numero de patches (par)")
    parser.add_argument("--saida", default="su/patches", help="diretorio de saida")
    args = parser.parse_args()

    if args.n <= 0 or args.n % 2 != 0:
        parser.error("n deve ser um numero par positivo")

    secao, dt = le_su(args.arquivo)
    patches = extrai_patches(secao, args.n)

    base = os.path.splitext(os.path.basename(args.arquivo))[0]
    for i, patch in enumerate(patches):
        arquivo = os.path.join(args.saida, f"{base}_patch_{i:02d}.su")
        salva_su(patch, dt, arquivo)
        print(f"{arquivo}: ns={patch.shape[0]} ntr={patch.shape[1]}")
