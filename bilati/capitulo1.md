# capitulo 1

**1.** A saída do comando abaixo detalha a função do atributo `scalco`

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

**2.** `suplane` é um gerador de dados sintéticos utilizado para criar uma seção de afastamento comum contendo até 3 eventos (reflectores ou "planos") inclinados.

O comando abaixo gera uma seção de afastamento comum com 3 eventos inclinados e a exibe usando `suximage`. O parâmetro `npl` só pode ser definido como 1, 2 ou 3.

```bash
suplane npl=3 | suximage
```
![Exemplo de saída do comando suplane](./16suplane1.png)

Na figura, o eixo horizontal representa o número do traço (trace number, parâmetro `ntr`) e o eixo vertical representa a amostra temporal (time sample, parâmetro `nt`). O plot mostra as amostras coletadas de 32 traços.

**3.** *work in progress*