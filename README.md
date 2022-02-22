# EVFO
# Introducción
Herramienta para analizar y correlacionar "logs" de distintos sistemas en una misma infraestructura.

1. Ordena los logs de las distintas funtes de forma temporal en formato Epoch.
2. Crea un fichero llamado "ficheroAllLogs" con todos ellos.
3. Pinta gráficas con los registros de los "logs" agrupados en un periodo "X" de tiempo configurable para su posterior evaluación.

# Instrucciones
1. El script se ejecuta con "python3 time-test.py"
2. Para modificar el tiempo de agrupación de registros unicamente hay que cambiar la variable "step" del fichero "time-test.py" al valor deseado en segundos.
3. En la carpeta logFiles se encuentran los ficheros de logs utilizados
4. En la carpeta Graficas se encuentran las graficas consideradas más interesantes.