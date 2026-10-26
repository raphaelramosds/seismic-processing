# Convolução 2D - Conceitos

Explicação dos conceitos de canais de entrada, canais de saída, kernels, padding e stride

Veja: https://hannibunny.github.io/mlbook/neuralnetworks/convolutionDemos.html

## Canais de entrada

É a profundidade espacial do tensor que entra na camada. 

- Para a primeira camada recebendo uma imagem colorida (RGB), o valor é 3. 
- Para uma imagem em tons de cinza, é 1. 

Se a convolução estiver no meio da rede, este número é igual aos mapas de características (feature maps) produzidos pela camada anterior.

## Kernel Size (Tamanho do Filtro)

São as dimensões espaciais da matriz de pesos (ex: 3x3, 5x5). Ele define o campo receptivo local, ou seja, o tamanho da "janela" de pixels que a rede observa simultaneamente para calcular um único valor de saída.

## Canais de saída

É o número de filtros (ou kernels) independentes que a camada vai aplicar sobre a entrada. Cada filtro aprende a extrair um padrão diferente (como bordas verticais, texturas ou formas). O número escolhido aqui define qual será a nova "profundidade" do tensor de saída.

Por exemplo, uma entrada de (1, 1, 8, 8) com 2 filtros de tamanho 3x3 produzirá uma saída de (1, 2, 6, 6), onde 2 é o número de canais de saída.

## *Padding* (Preenchimento)

É a técnica de adicionar valores artificiais (quase sempre zeros, chamado de zero-padding) ao redor das bordas do tensor de entrada. Isso serve para duas coisas: evitar que as dimensões espaciais da imagem encolham a cada camada e garantir que as informações nas bordas da imagem original sejam processadas adequadamente pelo kernel.

## *Stride* (Passo)

É a quantidade de pixels que o kernel se desloca de uma só vez ao deslizar sobre a entrada. Um stride de 1 move a janela pixel a pixel. Um stride maior (ex: 2) faz o kernel dar saltos, o que reduz propositalmente a largura e a altura do mapa de saída (downsampling).

## Relação entre kernel size, padding e stride

Para um kernel de tamanho $M$ aplicada a uma imagem de dimensão $M$, com padding $P$ e stride $S$, a dimensão da saída pode ser calculada como:

$$
O = \text{floor} \left( \frac{M - N + 2P}{S} + 1 \right)
$$

Para uma matriz de entrada que não foi aplicada padding ($P=0$), e stride unitário ($S=1$), a dimensão da saída será 

$$
O = M - N + 1
$$