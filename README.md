# WiFi_radar
Herramienta para monitorización, análisis y visualización de tráfico WiFi. TFG/GISC/UC3M 

Características:
- Nodos de captura: foneras 2.0n flasheadas, OpenWRT, bash (configuración, captura, tx trazas al servidor, control espacio), tcpdump, sshfs, dropbear, ntpclient.
- Servidor: debian, bash, python (procesado trazas con eliminación de solapamientos, control nodos), scapy (libreria para manejo de paquetes en python), admin lte (plantilla frontend), django (backend), highcharts (gráficos front), hypertree (gráfico en forma de disco front).


Descripción general:
La plataforma diseñada persigue extraer información útil acerca del tráfico WiFi en cierto área. Tras elegir el área a estudiar, se selecciona el emplazamiento de los dispositivos de captura de manera que se optimice el área cubierta. Estos dispositivos apturarán todo el tráfico WiFi que circule a su alcance. Los  paquetes capturados en todos los puntos se centralizan en el servidor y éste extraerá aquellas variables que nos interesen para luego correrarlas y obtener información compleja que puede ser de gran interés a la hora de auditar las redes WiFi y/o a sus clientes. Para hacer más comprensible el análisis de las variables, se usan gráficos interactivos. 
