# gerar secao sismica com tres interfaces
suplane | suxwigb title="suplane test pattern" label1="time (s)" label2="trace number" &

# gerar espectro de amostras em tempo de uma secao com tres interfaces
suplane | suspecfx | suxwigb label1="freq. hz" label2="trace number" &

# gerar espectro de uma vibracao de 30Hz simulada com vibroseis
suvibro f1=30 f2=30 t1=0 t2=0 > 30hz.su

# gerar espectro de uma vibracao de 30Hz
suvibro f1=30 f2=30 t1=0 t2=0 tv=100 > 30hz.su

# incrementar a frequencia em 0.1Hz
suvibro f1=30.1 f2=30.1 t1=0 t2=0 tv=100 > 30.1hz.su

# somar amplitudes
susum 30hz.su 30.1hz.su > sum.su

# espectro continuo: Fourier Transform (FT)
suspecfx <sum.su | suxwigb &

# espectro continuo: FT com Fast Fourier Transform
sufft < sum.su | suamp mode=amp | suxgraph label1="Frequency Hz" label2="Spectral Amplitude" &

# espectro discreto: DFT com FFT
suslowft < sum.su | suamp mode=amp | suxgraph label1="Frequency Hz" label2="Spectral Amplitude" &