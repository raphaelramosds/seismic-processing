# capitulo 1

**1.5.** A saída do comando abaixo detalha a função do atributo `scalco`

```bash
sukeyword -o | grep -m 1 -A7 scalco
```

```c
short scalco;   /* Scalar to be applied to the next 4 entries
                    to give the real value. 
                    Scalar = 1, +10, +100, +1000, +10000.
                    If positive, scalar is used as a multiplier,
                    if negative, scalar is used as a divisor.
                    byte# 71-72
                    */
```

**1.6.**