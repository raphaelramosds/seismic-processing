# Instalação Seismic To Unix

Instale dependências básicas

```bash
sudo apt install libtirpc-dev

export CPATH="/usr/include/tirpc:$CPATH"
```

Siga o tutorial de: https://wiki.seismic-unix.org/sudoc:su_installation

Antes de executar o `make install`, no Makefile.config que você escolheu, descomente a linha:

```Makefile
XDRFLAG =  -DSUXDR -DSUTIRPC
```

Depois, faça as seguintes modificações:

```Makefile
#-----------------------------------------------------------------------
# Gnu compilers by default just because they are the most common
#-----------------------------------------------------------------------

CPP = cpp

#CC = clang
CC = gcc
#OPTC = -g  -std=c99 -Wall -pedantic -Wno-long-long 

# 1. Remova "-ltirpc" do OPTC, e inclua "-I/usr/include/tirpc"
OPTC = -O2  -std=c99 -Wall -pedantic -Wno-long-long -I/usr/include/tirpc
CFLAGS = -I$I $(OPTC) $(CWP_FLAGS) -D_DEFAULT_SOURCE -D_POSIX_SOURCE

FC = gfortran
FOPTS = -g -std=legacy -no-pie
FFLAGS = $(FOPTS) -ffixed-line-length-none

C++FLAGS = -I$I $(OPTC) $(CWP_FLAGS)

# 2. Adicione a library "-ltirpc" na flag do post-linker
POSTLFLAGS = -no-pie -ltirpc
```