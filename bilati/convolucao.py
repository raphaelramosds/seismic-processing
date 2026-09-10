import numpy as np

n = 10
m = 15

xn = [0]*n
xm = [0]*m

resultado = np.convolve(xn, xm)

print("xn tem {} elementos".format(len(xn)))
print("xm tem {} elementos".format(len(xm)))
print("Tamanho xn * xm: {} ".format(len(resultado)))