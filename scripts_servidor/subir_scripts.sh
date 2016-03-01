#!/bin/bash

# IP="163.117.140.252" # -> Fon1  ok
# MAC="001884893ee2"
# 
# IP='163.117.139.55' #-> Fon2  ok
# MAC='001884893fb6'
# 
 # IP='163.117.140.250' #-> Fon3 ok
# MAC='001884893fbe'
# 
# IP='163.117.140.197' #-> Fon4  ok
# MAC='001884893f8e'
# 
# IP='163.117.139..56' #-> Fon5*
# MAC='001884893fc2'
# 
# IP='163.117.139..229' #-> Fon6*
# MAC='001884893f9a'
# 
# IP='163.117.139..58' #-> Fon7*
# MAC='001884893fa2'
# 
# IP='163.117.140.251' #-> Fon8  ok
# MAC='001884893f8a'
# 
# IP='163.117.140.227' #-> Fon9  ok
# MAC='001884893eda'
# 
# IP='163.117.139..246' #-> Fon10*
# MAC='001884893fa6'
# 
# IP='163.117.140.32' #-> Fon11 ok
MAC='001884893fae'

IPARRAY='163.117.140.32'
# IPARRAY='163.117.140.227,163.117.140.252,163.117.140.251,163.117.140.197,163.117.140.32,163.117.139.55,163.117.140.250'
  
echo "Copiando última version de scripts_fonera en escorpion"
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa -r /home/kike/TFG/scripts_fonera/ wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/

echo "Copiando última version de scripts_escorpion en escorpion"
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/scripts_escorpion/subir_scripts.sh wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_escorpion/subir_scripts.sh
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/scripts_escorpion/tfg_servidor.py wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_escorpion/tfg_servidor.py
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/pruebaspython/pcaptesting.py wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_escorpion
# sudo scp -o ConnectTimeout=3 -i ~kike/.ssh/id_rsa /home/kike/TFG/scripts_escorpion/vendors wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_escorpion/vendors
# sudo scp -o ConnectTimeout=3 -i ~kike/.ssh/id_rsa /home/kike/TFG/scripts_escorpion/services wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_escorpion/services
# Parar el proceso ./tfg_escorpion disable; ./tfg_escorpion stop en init.d
# Iniciar el proceso ./tfg_escorpion enable; ./tfg_escorpion start en init.d  


echo "Copiando archivos para la web"
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/web/tfgweb/tfgplot/models.py wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/tfgplot/models.py
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/web/tfgweb/tfgweb/urls.py wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/tfgweb/urls.py
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/web/tfgweb/tfgplot/index.html wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/tfgplot/index.html
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/web/tfgweb/tfgplot/index2.html wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/tfgplot/index2.html
sudo scp -o ConnectTimeout=9 -i ~kike/.ssh/id_rsa /home/kike/TFG/web/tfgweb/tfgplot/views.py wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/tfgplot/views.py
# sudo scp -o ConnectTimeout=3 -i ~kike/.ssh/id_rsa -r /home/kike/TFG/web/tfgweb/static/ wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/web/tfgweb/


for j in $(seq 1 1 1)
do
  IP=$(echo $IPARRAY | awk -v ipawk=$j -F',' '{ print $ipawk }' )

  echo "Creando carpeta de capturas de $IP en escorpion"
  ssh -i ~kike/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "mkdir -p /srv/Capturas/$MAC; mkdir -p /srv/Registros; exit;"

#  echo "Copiando banner a $IP"
#  ssh -i ~kike/.ssh/id_rsa wifi-radar@luciernaga.it.uc3m.es "ssh -i /home/jmmontes/.ssh/id_rsa root@$IP \"scp -i /root/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es:/home/jmmontes/Escritorio/Servidor/scripts_fonera/banner /etc/banner; exit;\""

  echo "Copiando el arranque a $IP"
  ssh -oConnectTimeout=5 -i ~kike/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "ssh -i .ssh/id_rsa_fon root@$IP \"scp -i /root/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_fonera/tfg_inicio /etc/init.d/tfg_inicio; chmod +x /etc/init.d/tfg_inicio; exit;\""
  ssh -oConnectTimeout=5 -i ~kike/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "ssh -i .ssh/id_rsa_fon root@$IP \"rm /etc/archivos/log_errores; cd /etc/init.d/; ./iniciotfg stop; ./iniciotfg disable; rm iniciotfg; ./tfg_inicio stop; ./tfg_inicio disable; ./tfg_inicio stop; ./tfg_inicio enable; exit;\""

  echo "Copiando tfg_ordenes.sh a $IP"
  ssh -oConnectTimeout=5 -i ~kike/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "ssh -i .ssh/id_rsa_fon root@$IP \"scp -i /root/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es:/srv/Servidor/scripts_fonera/tfg_ordenes.sh /etc/archivos/tfg_ordenes.sh; exit;\""

  echo "Reiniciando fonera $IP"
  ssh -oConnectTimeout=5 -i ~kike/.ssh/id_rsa wifi-radar@escorpion.it.uc3m.es "ssh -i .ssh/id_rsa_fon root@$IP \"reboot;\""

done  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  