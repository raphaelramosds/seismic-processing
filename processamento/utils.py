import os
import numpy as np
from obspy import Stream, Trace, read
from obspy.core import AttribDict

def pulso_ricker(fp: float, dt: float, ns: int):
    """Gera pulso ricker com frequencia de pico fp amostrado em dt segundos com ns amostras"""
    a = (ns * dt) / 2
    t = np.arange(-a, a, dt)
    ft = (np.pi * fp * t) ** 2
    return t, (1.0 - 2.0 * ft) * np.exp(-ft)

def convolve_secao(refl: np.ndarray, ricker: np.ndarray):
    """Convolve cada traco do modelo de refletividade da secao com a mesma ricker"""
    return np.apply_along_axis(lambda tr: np.convolve(tr, ricker, mode="same"), 0, refl)

def adiciona_ruido_snr(sinal: np.ndarray, snr_db: float, rng: np.random.Generator | None = None):
    """Adiciona ruido gaussiano para um SNR especifico (em dB)"""
    if rng is None:
        rng = np.random.default_rng()
    p_sinal = np.mean(sinal ** 2)
    p_ruido = p_sinal / 10 ** (snr_db / 10)
    return sinal + rng.normal(0, np.sqrt(p_ruido), sinal.shape)

def salva_su(secao: np.ndarray, dt: float, arquivo: str):
    """Salva a secao (ns, ntr) em formato SU little-endian"""
    st = Stream()
    for k in range(secao.shape[1]):
        tr = Trace(data=np.ascontiguousarray(secao[:, k], dtype=np.float32))
        tr.stats.delta = dt
        tr.stats.su = AttribDict()
        tr.stats.su.trace_header = AttribDict()
        # tracl, tracr e cdp
        tr.stats.su.trace_header.trace_sequence_number_within_line = k + 1
        tr.stats.su.trace_header.trace_sequence_number_within_segy_file = k + 1
        tr.stats.su.trace_header.ensemble_number = k + 1
        st.append(tr)
    os.makedirs(os.path.dirname(arquivo) or ".", exist_ok=True)
    st.write(arquivo, format="SU", byteorder="<")

def le_su(arquivo: str):
    """Le um arquivo SU little-endian e retorna a secao (ns, ntr) e o dt"""
    st = read(arquivo, format="SU", byteorder="<")
    secao = np.stack([tr.data for tr in st], axis=1)
    return secao, st[0].stats.delta
