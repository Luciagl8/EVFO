# EVFO
# Introducción
Herramienta para analizar y correlacionar logs de distintos sistemas en una misma infraestructura.

1. Ordena los logs de las distintas funtes de forma temporal en formato Epoch.
2. Crea un fichero llamado "out.csv" con todos ellos.
3. Pinta 3 tipos de gráficas diferentes:
    - (tipo_log)ip.png -> <tipo_log> hace referencia a la fuente estudiada. Gráfica con las direcciones IP de los logs que aparecen 3 o más veces en el mismo segundo.
    - (tipo_log)T.png -> <tipo_log> hace referencia a la fuente estudiada. Gráfica con todos los registros de esa fuente ordenados por tiempo.
    - (X)sTotalTime.png -> Registros de los logs de las distintas fuentes agrupados en un periodo <X> de tiempo configurable para su posterior evaluación.

# Consideraciones previas
1. Es necesario tener python (versión 3) instalado y añadido al PATH.
2. La interfaz gráfica está optimizada para unas especificaciones de pantalla 4K.
3. En caso de no tener pantalla 4K y/o no poder visualizar correctamente la interfaz gráfica, se puede utilizar por línea de comandos.

# Instrucciones - Ejecución mediante Interfaz Gráfica
1. Intalar las dependencias del fichero requirements.exe (Doble click en el archivo)
2. Ejecutar el script script_executor_windows.exe (Doble click sobre el archivo)
3. Se abrirá una interfaz para elegir la gráfica que se desee que genere el programa. (La generación de las gráficas puede tardar unos segundos)
4. Para modificar el tiempo de agrupación de registros en la gráfica "All Logs" unicamente hay que introducir el valor deseado en segundos, el resto de gráficas no ofrecen opciones adicionales.
5. En el PATH donde se haya instalado el repositorio se habrán generado también las distintas gráficas.
    - access_logip.png (Direcciones IP que aparecen 3 o más veces en el mismo segundo)
    - access_logT.png (Número de logs en cada fecha)
    - error_logip.png
    - error_logT.png
    - mail_logip.png
    - mail_logT.png
    - xTotalTime.png (Gráfica con todos los logs de las 3 fuentes ordenados y agrupados según el valor introducido)
6. En la carpeta logFiles se encuentran los ficheros de logs utilizados.
7. El fichero out.csv contiene todos los logs ordenados y formateados de las distintas fuentes.

# Instrucciones - Ejecución por linea de comandos
1. Colocarse en el PATH donde se haya instalado este repositorio.
2. Introducir "python time-test.py <tiempo>". Siendo <tiempo> una variable opcional que configura el rango de tiempo para la agrupación de logs (Introducir el valor deseado en segundos, por defecto está configurado a 3600s)
3. En esa misma localización se habrán generado todas las gráficas del programa para poder estudiarlas (La generación de las gráficas puede tardar unos segundos).
    - access_logip.png (Direcciones IP que aparecen 3 o más veces en el mismo segundo)
    - access_logT.png (Número de logs en cada fecha)
    - error_logip.png
    - error_logT.png
    - mail_logip.png
    - mail_logT.png
    - xTotalTime.png (Gráfica con todos los logs de las 3 fuentes ordenados y agrupados según la variable <tiempo>)
5. En la carpeta logFiles se encuentran los ficheros de logs utilizados.
6. El fichero out.csv contiene todos los logs ordenados y formateados de las distintas fuentes.