#!/bin/bash

# TFG 2013
# Enrique Herreros Jiménez
# Script con las siguiente funciones:
#        Registrar en thr.csv el canal en el que se registra el throughput medio en un intervalo de tiempo
#        Traspaso de los archivos .pcap con las cabeceras de los paquetes capturados en cada nodo al servidor
#        Temporalmente: orden desde el nodo de compresion de conjuntos de estos archivos .pcap al servidor
#        Configuración de la interfaz mon0 de monitorización
#        Configuración e inicio de la herramienta TCPDUMP
#        Registro en thr.csv el canal en el que se registra el throughput medio en un intervalo de tiempo
#        Traspaso de los archivos .pcap con las cabeceras de los paquetes capturados en cada nodo al servidor
#        Temporalmente: orden desde el nodo de compresion de conjuntos de estos archivos .pcap al servidor
#        timer funciona como un contador de operaciones más que como un reloj (pero cada tic es aprox 1 seg)

export MY_MAC2=$(ip addr show dev wlan0 | grep link | awk '{ print $2 }')
export MY_IP=$(ip addr show dev eth0.2 | grep inet | awk '{ print $2 }')
export MY_MAC=$(ip addr show dev wlan0 | grep link | awk '{ print $2 }' | tr -d :)
export TMRARRAY='8,8,8,8,8,8,8,8,8,8,8,8,8'
export THRARRAY='0,0,0,0,0,0,0,0,0,0,0,0,0'

# Configuración en segundos iniciales FIJAS
# compress_freq_interval=18120 # intervalo de tiempo para compresion de conjuntos .pcap. Entraran 100.
timer_tcpdump_interval=170 # intervalo de tiempo para copiar los .pcap al servidor
register_interval=120 # (re)registro cada 1 minutos y medio
captura_frequency=164 # cada cuanto se genera un .pcap
timer_logerrores_interval=300
last_boot=$(date +%Y-%m-%d-%H-%M)


# Inicializo variables
switch_freq=$(echo $TMRARRAY | awk -F',' '{ print $1 }' )
# compress_freq=$compress_freq_interval
timer_tcpdump=$timer_tcpdump_interval
register_time=$register_interval
timer_logerrores=$timer_logerrores_interval
sumjant=0 # sumatorio de valores del array THRARRAY de throughputs
nuevo_canal=1
tmpsat=0
canal_maximo=11
thr_max=0

echo "Cambio de canal inicial cada $switch_freq segundos"
echo "Cada .pcap contiene capturas de $captura_frequency segundos" >> /etc/archivos/log_errores
echo "Transmisión de los .pcap en esta fonera a escorpion cada $timer_tcpdump_interval segundos" >> /etc/archivos/log_errores
# echo "Compresión de .pcap en servidor cada $compress_freq_interval segundos" >> /etc/archivos/log_errores
echo "canal,fecha,thr,coord" > /tmp/thr.csv
# Función registrar realiza:
#    Creación de un archivo con el nombre de la mac (sin los semicolon) que contiene la fecha, la IP e info del disco
#    Transmisión del archivo a la unidad virtual montada del servidor
registrar() {
  echo 'Registrando este nodo en el servidor'
  rm  /etc/archivos/$MY_MAC
  touch /etc/archivos/$MY_MAC
  echo "Fecha último registro: $(date +%Y-%m-%d-%H-%M)" >> /etc/archivos/$MY_MAC # escribe la fecha de registro
  echo "Fecha último reinicio: $last_boot" >> /etc/archivos/$MY_MAC
  echo "IP: $MY_IP" >> /etc/archivos/$MY_MAC # escribe la IP en el fichero con nombre MAC
  echo "Espacio en disco usado: $(df | grep -e rootfs | awk -F " " ' {print $5}')" >> /etc/archivos/$MY_MAC || (echo "$(date): error al determinar el espacio en disco ocupado" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "Espacio temporal usado: $(df | grep /tmp | awk -F " " ' {print $5}')" >> /etc/archivos/$MY_MAC || (echo "$(date): error al determinar el espacio temporal ocupado" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "Carga media del procesador: $(uptime | awk -F " " ' {print $NF}')" >> /etc/archivos/$MY_MAC || (echo "$(date): error al determinar la carga media del procesador" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "Directorio en escorpion: $(df | grep -e @escorpion)" >> /etc/archivos/$MY_MAC || (echo "$(date): error al determinar la ruta de montaje en escorpion" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "Directorio de escorpion montado en: $(df | grep -e /mnt/escorpion | awk -F " " ' {print $5}')" >> /etc/archivos/$MY_MAC || (echo "$(date): error al determinar la ruta de montaje en fonera" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "*************************" >> /etc/archivos/$MY_MAC
  scp -i /root/.ssh/id_rsa /etc/archivos/$MY_MAC -o ConnectTimeout=10 wifi-radar@escorpion.it.uc3m.es:/srv/Registros || (echo "$(date): error al copiar el archivo de registro al servidor" >> /etc/archivos/log_errores && sleep 10 && reboot)
  check_tmpused
  let register_time=$timer+$register_interval
}

# Función check_tmpused realiza:
#  Control del uso de la unidad temporal de la fonera. En el futuro
check_tmpused() {
  tmpused="$(df | grep /tmp | awk -F " " ' {print $5}' | grep "%" | sed 's/%$//')"  || (echo "$(date): error al determinar el espacio temporal ocupado" >> /etc/archivos/log_errores && sleep 10 && reboot)
  echo "$(date): $tmpused% usado de espacio temporal en el disco de la fonera" > /tmp/tmp_used
  echo "La unidad temporal de esta fonera está al $tmpused% ocupada"
  if [ $tmpused -gt 94 ]; then
    echo "$(date): se ha superado el 94% de espacio ocupado en /tmp/. Reboot en 20 segundos..." >> /etc/archivos/log_errores
    sleep 20
    reboot    
  fi
}

# Función calc_thr_avg realiza:
# Calculo del throughput desde la ultima vez que se llamo a esta funcion
calc_thr_avg() {
  bytes_rcv1=$(ifconfig mon0 | grep "RX bytes" | awk -F ":" ' { print $2 }' | awk '{ print $1 }')
  timer_rcv1="$(date +%s)"
  canal_actual=$(iwlist mon0 channel | grep Current | awk -F " " '{print $5}' | tr -d ")")
  time_average_interval=$(echo $TMRARRAY | awk -v chawk=$canal_actual -F',' '{ print $chawk }' )
  thr=$(echo "scale=3; ($bytes_rcv1-$bytes_rcv)*8/(($timer_rcv1-$timer_rcv)*1000)" | bc) # en Kbps. scale es nº de decimales
  COORD=$(cat /etc/archivos/coordenadas.dat)
  
  if [ "$(echo $thr '>' $thr_max | bc -l)" -eq 1 ]; then
    canal_maximo=$canal_actual
    thr_max=$(echo "$thr" | bc)
    echo "$(date): el nuevo canal de máx tasa es $canal_maximo" >> /mnt/escorpion/tiemposrastreo
  fi

  let timediff=$timer_rcv1-$timer_rcv
  echo "$canal_actual,$(date +%Y-%m-%d-%H-%M:%S), $thr kbps, $timediff seg en canal, teorico $time_average_interval, maximo de ronda ($thr_max, $canal_maximo)" >> /mnt/escorpion/thr.csv
 
  bytes_rcv=$(ifconfig mon0 | grep "RX bytes" | awk -F ":" ' { print $2 }' | awk '{ print $1 }')
  timer_rcv="$(date +%s)"
}

# Función cambia_canal realiza:
#    Aumentar en 1 el canal a monitorizar y permanecer en ese canal el tiempo optimo
cambia_canal() {
  canal_actual=$(iwlist mon0 channel | grep Current | awk -F " " '{print $5}' | tr -d ")")
  calc_thr_avg
  THRARRAY=$(echo $THRARRAY | awk -v chawk=$canal_actual -v thrawk=$thr -F',' '{ $chawk=thrawk; print }' OFS=\,)

  if [ $canal_actual -eq 13 ]; then
    sumjant=0
    sumtant=0
    
    #Calcular el sumatorio del ultimo vector de throughputs
    for n in $(seq 1 1 13)
    do
	   sumjant=$(echo "$sumjant+$(echo $THRARRAY | awk -v thrnantawk=$n -F',' '{ print $thrnantawk }' )" | bc)
    done
    
    #Calcular el nuevo vector de tiempos de captura
    for j in $(seq 1 1 13)
    do
      thrjant=$(echo $THRARRAY | awk -v thrjantawk=$j -F',' '{ print $thrjantawk }' )
      thrj=$(echo "(13*8*$thrjant)/$sumjant" | bc)  # 13 canales a 8 segundos por canal en barrido inicial. 104seg
      echo "El tiempo calculado para el canal $j es de $thrj segundos" #>> /mnt/escorpion/tiemposrastreo
      
      #Threshold de tiempo minimo de captura
      if [ $thrj -lt 5 ]; then
        thrj=5
      fi
      
      TMRARRAY=$(echo $TMRARRAY | awk -v pos=$j -v thrjawk=$thrj -F',' '{ $pos=thrjawk; print }' OFS=\,)
    done
    echo "$(date): array de tiempos de capt es $TMRARRAY" >> /mnt/escorpion/tiemposrastreo
    
    #Calcular el sumatorio de tiempos de monitorización (puede que por el redondeo se segundos no sea exactamente 195s)
    for t in $(seq 1 1 13)
    do
	   sumtant=$(echo "$sumtant+$(echo $TMRARRAY | awk -v tmptawk=$t -F',' '{ print $tmptawk }' )" | bc)
    done
    thr_max=$(echo 0 | bc)
    let nuevo_canal=1
    echo "$(date): sumatorio de tiempos de rotación es $sumtant, volviendo a canal 1" >> /mnt/escorpion/tiemposrastreo
  else
    let nuevo_canal=$nuevo_canal+1
  fi
  if [ $nuevo_canal -eq 14 ]; then
    nuevo_canal=1
  fi
  switch_freq_interval=$(echo $TMRARRAY | awk -v chawk=$nuevo_canal -F',' '{ print $chawk }' )
  echo "$(date): siguiente canal $nuevo_canal durante $switch_freq_interval segundos" >> /mnt/escorpion/tiemposrastreo
  iwconfig mon0 channel $nuevo_canal || echo "$(date): error al cambiar al canal $nuevo_canal" >> /etc/archivos/log_errores
  let switch_freq=$timer+$switch_freq_interval && echo "El siguiente cambio de canal será en $switch_freq_interval segundos"
}

# Función config_wireless realiza
# Configuracion inicial de la interfaz wireless para OpenWRT
config_wireless() {
  wifi down || echo "$(date): error al desactivar la interfaz wifi" >> /etc/archivos/log_errores
  sleep 3
  echo "Cambiando fichero de configuracion de la interfaz wireless"
cat > wireless << END_FILENAME_WIRELESS_CONFIG.EDIT

config wifi-device  radio0
    option type     mac80211
    option channel  11
    option macaddr    $MY_MAC2
    option hwmode    11g
    #option htmode    HT20
    #list ht_capab    GF
    #list ht_capab    SHORT-GI-20
    #list ht_capab    SHORT-GI-40
    #list ht_capab    TX-STBC
    #list ht_capab    RX-STBC12
    #REMOVE THIS LINE TO ENABLE WIFI:
    #option disabled 1

config wifi-iface
    option device   radio0
    #option network  lan
    option mode     sta
    option ssid     Uni3
    option encryption none

END_FILENAME_WIRELESS_CONFIG.EDIT

  scp -p wireless /etc/config/ && echo "Cambiado fichero configuracion WIRELESS!" || echo "$(date): error al copiar el fichero de configuracion a /etc/config" >> /etc/archivos/log_errores

  wifi up || echo "$(date): error al levantar la interfaz wifi" >> /etc/archivos/log_errores
  iw phy phy0 interface add mon0 type monitor && echo "Configurada la interfaz en modo monitor" || echo "$(date): error al montar la interfaz en modo monitor" >> /etc/archivos/log_errores
  ip link set mon0 up || echo "$(date): error al levantar la interfaz wifi en modo monitor" >> /etc/archivos/log_errores
  ip link set wlan0 down || echo "$(date): error al desactivar la interfaz wifi" >> /etc/archivos/log_errores
  iw dev mon0 set channel 1 && echo "Establecido canal 1 para escucha" || echo "$(date): error al establecer el canal 1 para escucha" >> /etc/archivos/log_errores
  echo -e "Finalizada la configuración de la interfaz wireless con los siguiente parámetros:\n $(iwconfig mon0)"
}

# Función config_tcpdump realiza:
#
config_tcpdump() {
  HOME_DIR=/mnt/escorpion
  killall tcpdump || echo "$(date): no se ha matado ningun proceso tcpdump existente" >> /etc/archivos/log_errores
  killall -9 tcpdump || echo "$(date): no se ha matado ningun proceso tcpdump existente con una señal SIGKILL" >> /etc/archivos/log_errores
  tcpdump -v -i mon0 -s 100 -w /tmp/captura-%Y-%m-%d-%H-%M-%S.pcap -G $captura_frequency -W 1 &
  echo "TCPDUMP capturando! Se usará la siguiente configuracion: tcpdump -n -i mon0 -s 100 -w /tmp/captura-%Y-%m-%d-%H-%M-%S.pcap -G $captura_frequency &"
}

# Función mandar_capturas realiza el envio de capturas al servidor a traves de SSHFS
#
mandar_capturas() {
    echo "Enviando .pcap's a escorpion"
    current_dir=$pwd
    cd /tmp/
    files_to_copy=$(ls -tr *.pcap | head -$( echo "$(ls *.pcap | wc -w)" | bc))
    echo $files_to_copy > files_to_copy
    timer_inicio="$(date +%s)"
    echo "$(date): comienzo de envio de $files_to_copy" >> /mnt/escorpion/tiemposrastreo
    scp /tmp/$files_to_copy /mnt/escorpion/ && rm /tmp/$files_to_copy && timer_fin="$(date +%s)" && (tcpdump -v -i mon0 -s 100 -w /tmp/captura-%Y-%m-%d-%H-%M-%S.pcap -G $captura_frequency -W 1 &) && let timer_dif=$timer_fin-$timer_inicio && echo "$(date): fin de envío, duracion $timer_dif, volviendo a capturar" >> /mnt/escorpion/tiemposrastreo 
    cd $current_dir
    let timer_tcpdump=$timer+$timer_tcpdump_interval
}

# Función reinicia realiza:
#    
reinicia() {
  cd /etc/init.d
  ./tfg_inicio start
}

# Función comprimir realiza:
# Manda la orden de comprimir al servidor. IMPLEMENTAR EN EL SCRIPT QUE CORRE AD INFINITUM EN EL SERVIDOR.
# comprimir() {
#   echo "Comprimiendo"
#   current_dir=$pwd
#   cd /mnt/escorpion
 
#   files_to_store=$(ls -tr *.pcap | head -$( echo "$(ls *.pcap | wc -w) -1" | bc))
#   echo $files_to_store > files_to_store
#   capture_name="captura-$(date +%Y-%m-%d-%H-%M).tar.gz"
 
#   echo '#!/bin/bash
#   compress_name=$1
#   files_to_store=$(cat files_to_store)
#   tar -zcvf  $compress_name $files_to_store
#   rm $files_to_store' > compress.sh

#   ssh -i /root/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "cd /srv/Servidor/Capturas/$MY_MAC; sh compress.sh $capture_name" || echo "$(date): error al mandar orden de compresion de $capture_name al servidor" >> /etc/archivos/log_errores
#   cd /tmp
#   rm $files_to_store || echo "$(date): error al borrar los ficheros $files_to_store" >> /etc/archivos/log_errores
#   cd $current_dir
#   let compress_freq=$timer+$compress_freq_interval
# }


# Esto se ejecuta solo 1 vez al principio
echo "Montando punto /mnt/escorpion con SSHFS"
id
mkdir -p /mnt/escorpion
sshfs wifi-radar@escorpion.it.uc3m.es:/srv/Capturas/$MY_MAC/ /mnt/escorpion -o ssh_command="ssh -i /root/.ssh/id_rsa",reconnect || (echo "$(date): error al montar sshfs. Reiniciando..." >> /etc/archivos/log_errores && sleep 400 && reboot)
registrar
config_wireless
config_tcpdump
timer=0
bytes_rcv=$(ifconfig mon0 | grep "RX bytes" | awk -F ":" ' { print $2 }' | awk '{ print $1 }')
timer_rcv="$(date +%s)"
scp /etc/archivos/log_errores /mnt/escorpion/ && echo "Transmisión del log de errores correcta" || echo "$(date): error en la copia del log de errores al servidor" >> /etc/archivos/log_errores

# Bucle infininito de ejecución
echo "Iniciando bucle de ejecución de scripts"
while [ 1 ];do
    HOME_DIR=/mnt/escorpion
    
    if [ $timer -eq $register_time ]; then
      registrar
    fi
    
    if [ $timer -eq $timer_tcpdump ]; then 
      mandar_capturas
    fi

    if [ $timer -eq $switch_freq ]; then
      cambia_canal
    fi
    
    if [ $timer -eq $timer_logerrores ]; then 
      scp /etc/archivos/log_errores /mnt/escorpion/ && echo "Transmisión del log de errores correcta" || echo "$(date): error en la copia del log de errores al servidor" >> /etc/archivos/log_errores
      let timer_logerrores=$timer+timer_logerrores_interval
    fi
    
    let timer=$timer+1
    sleep 1 # stop durante 1 segundo
done

trap reinicia EXIT
cd /etc/init.d
./tfg_inicio stop





