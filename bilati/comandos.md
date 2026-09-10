# Programas Relacionados (1.4)

## a2b

**Explicação**: Converte um arquivo texto com números de ponto flutuante em um binário de precisão simples. É necessário informar quantos números há em cada linha do arquivo texto.

**Exemplo**:
```sh
a2b <in.dat n1=1001 >out.bin
```
Encadeando com `suaddhead` para criar um arquivo SU:
```sh
a2b <in.dat n1=1001 | suaddhead n1=1001 > out.su
```

## b2a

**Explicação**: Converte um arquivo binário com número de ponto flutuante em precisão simples para um arquivo texto. É necessário informar quantos números devem ser escritos em cada linha do arquivo de saída.

**Exemplo**:
```sh
b2a <in.bin n1=1001 >out.dat
```

## segyclean

**Explicação**: Zera porções do cabeçalho de um dado SU não especificadas no padrão SEG-Y.

**Exemplo**:
```sh
segyread tape=in.segy | segyclean >out.su
```

## segyread

**Explicação**: Lê um arquivo SEG-Y e o converte para o formato SU.

**Exemplo**:
```sh
segyread tape=in.segy | segyclean >out.su
```

## suaddhead

**Explicação**: Recebe um arquivo binário contendo números de ponto flutuante em precisão simples e cria um dado no formato SU com espaço reservado para o cabeçalho de cada traço, sem preenchê-lo, entretanto.

**Exemplo**:
```sh
suaddhead <in.bin ns=501 >out.su
```

## suchw

**Explicação**: Altera os valores de um campo do cabeçalho dos traços, utilizando para isso valores de outros campos do cabeçalho.

**Exemplo**:
```sh
suchw <in.su key1=offset key2=gx key3=sx c=-1 >out.su
```

## sudoc

**Explicação**: Exibe a documentação de um programa do SU escolhido. A maior parte dos programas do SU, quando executados sem qualquer parâmetro, por padrão, apresentam sua documentação na tela. Em vários casos, a documentação exibida pelo `sudoc` é a mesma exibida diretamente pelo programa. Ocasionalmente, `sudoc` pode apresentar mais detalhes.

**Exemplo**:
```sh
sudoc sufnzero
```

## suedit

**Explicação**: Examina interativamente um ou mais campos do cabeçalho dos traços.

**Exemplo**:
```sh
suedit <in.su
```

## sugethw

**Explicação**: Consulta o valor de um ou mais campos do cabeçalho dos traços.

**Exemplo**:
```sh
sugethw <in.su key=sx,gx,offset
```

## suhelp

**Explicação**: Apresenta a lista dos programas do SU, organizados por categorias.

**Exemplo**:
```sh
suhelp
```

## sukeyword

**Explicação**: Exibe a definição de cada campo do cabeçalho de um dado no formato SU.

**Exemplo**:
```sh
sukeyword -o
```

## supaste

**Explicação**: Cola um arquivo binário de cabeçalho a um arquivo binário com amostras de precisão simples para criar um arquivo no formato SU. Em geral, é usado com os arquivos de cabeçalho exportados pelo comando `sustrip`.

**Exemplo**:
```sh
supaste <in.bin head=header.bin >out.su
```

## surange

**Explicação**: Exibe os valores mínimos e máximos para cada campo do cabeçalho, entre todos os traços de um dado sísmico.

**Exemplo**:
```sh
surange <in.su
```

## sushw

**Explicação**: Altera os valores de um ou mais campos do cabeçalho dos traços, a partir de uma fórmula simples.

**Exemplo**:
```sh
sushw <in.su >out.su key=dt a=4000
```

## sustrip

**Explicação**: Retira o cabeçalho de um arquivo, retornando apenas um binário, em precisão simples, contendo as amostras dos traços. Este comando é útil quando queremos obter apenas a matriz de traços, por exemplo para carregá-la em outro programa. Caso pretenda reconstruir o arquivo no formato SU, o cabeçalho pode ser preservado para ser novamente adicionado ao binário com o programa `supaste`.

**Exemplo**:
```sh
sustrip <in.su head=header.bin >out.bin
```

## suwaveform

**Explicação**: Gera um pulso sísmico, dentre algumas opções clássicas, como Ricker, por exemplo.

**Exemplo**:
```sh
suwaveform type=ricker1 fpeak=15 | suxgraph style=normal
```
