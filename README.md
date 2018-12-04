Algoritmo de Fruchterman Reingold por Ignacio Seret
----
#### Gereralidades
El programa toma como argumento un archivo que almacena un grafo. Para entender el formato del archivo, ver la carpeta *ejemplos*. Una vez en ejecucion, permite agarrar vertices con el mouse y moverlos. El menu permite aumentar o disminuir el coeficiente de fuerza *k*. El boton *AUTO* activa el ajuste automatico del coeficiente *k* (ver funcion *updateK*).

```console
$ python draw.py --help
usage: draw.py [-h] [-v] [-K [K]] file

positional arguments:
  file          Especificar archivo de donde leer el grafo

optional arguments:
  -h, --help    show this help message and exit
  -v, -verbose  Modo verbose
  -K [K]        Especificar coeficiente de fuerza inicial
```

#### Requerimientos
Se requiere Python 2.x y las siguientes librerias: "pygame", "math", "random", "argparse", "sys" y "time".

#### Virtual environment
Si se esta en macOS y no se tiene pygame instalado, se puede usar el *virtual environment*:

```console
source TP/Bin/activate
python draw.py
```

Para salir del *virtualenv*:

```console
deactivate
```