# -*- coding: utf-8 -*-
# Enrique Herreros Jiménez 2013
# Este script se encargará de buscar nuestras foneras (ya autenticadas para babosa) en el departamento de telemática.
# Sabemos que el departamento e telematica cubre los rangos de IP 163.117.139.X y 163.117.140.X


import sys, getopt, subprocess, os, datetime
from time import gmtime, strftime

"""
Función main de la función que recoge los parametros pasados por consola al ejecutar el script y empieza a correr el script
"""
def main():
  for arg in sys.argv[1:]:
    try:
        #inicio139 = sys.argv[1]
        #inicio140 = sys.argv[2]
        #if arg=="0": buscador_foneras()
      print arg
      if arg!="":
        buscar(int(sys.argv[1]), int(sys.argv[2]))
      else:
        buscar(1, 1)
    except getopt.GetoptError:
      print 'Ayuda'
      print 'Si queremos iniciar la busqueda en 163.117.139.X y en 163.117.140.Y:'
      print '	python buscador_foneras.py X Y'
      print 'Si queremos iniciar la busqueda en 163.117.139.1 y en 163.117.140.1:'
      print '	python buscador_foneras.py'

def buscar(inicio139, inicio140):
  # creo una lista vacia que almacenará las foneras que encontremos autenticadas en el puerto 22
  fonera = []
  filelog = 'buscador_foneras.log'
  fecha =  strftime("%d-%b-%Y %H:%M:%S", gmtime())

  for ping in range(inicio139,255):
    address = "163.117.139." + str(ping)
    # evitamos aquellas conexiones que requieran aceptar fingerprint sin estar en la lista local de ssh rsa conocidos
    # establecemos el timeout a 2 segundos para agilizar los intentos de crear la SSH
    res = subprocess.Popen("ssh -oStrictHostKeyChecking=yes -oConnectTimeout=2 root@" + address + " exit", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    resp = res.stdout.readlines();
    if (len(resp) == 0):
      print address, " sí es un nodo nuestro. Añadido a la lista."
      fonera.append(address);
      # muestro el estado actual de la lista
      print fonera
    else:
      print address, " no es un nodo nuestro..."

  for ping in range(inicio140,255):
    address = "163.117.140." + str(ping)
    res = subprocess.Popen("ssh -oStrictHostKeyChecking=yes -oConnectTimeout=2 root@" + address + " exit", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    resp = res.stdout.readlines();
    if (len(resp) == 0):
      print address, " sí es un nodo nuestro. Añadido a la lista."
      fonera.append(address);
      print fonera
    else:
      print address, " no es un nodo nuestro..."
  print "Búsqueda terminada, los nodos que nos pertenecen son:"
  print fonera
  print "Se han encontrado " + str(len(fonera)) + " elementos" + " que se han guardado en " + filelog
  with open(filelog, 'w') as the_file:
    the_file.write(fecha + '\n' + str(fonera).strip('[]') + '\n')
  sys.exit()

if __name__ == "__main__":
  main()