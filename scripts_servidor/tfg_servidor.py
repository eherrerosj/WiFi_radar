# -*- coding: utf-8 -*-
# Enrique Herreros Jiménez 2013
# Este script contiene el ejemplo del procesado y parseo de trazas de los .pcap


import sys
import getopt
import subprocess
import random
import os
import smtplib
import datetime
from datetime import datetime
import time
from scapy.all import *
from scapy.utils import rdpcap
import sqlite3
from operator import itemgetter
import logging
import json
import json as simplejson
from datetime import timedelta

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
# fichero donde queremos almacenar el log
with open('pcaptesting.log', 'w'):
    pass
handler = logging.FileHandler('pcaptesting.log')
handler.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# crear el formato de los mensajes de log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
ch.setFormatter(formatter)
# añadir el handlers al logger
logger.addHandler(handler)
logger.addHandler(ch)
# hasta que haga el deploy final queremos modo debug para loggear todos
# los tipos de mensajes log
logging.basicConfig(level=logging.INFO)

dictregistros = {}
vendors = {}
services = {}
servicios_encontrados = []
tamanos = []
mhz2ch = {2412: "1",
          2417: "2",
          2422: "3",
          2427: "4",
          2432: "5",
          2437: "6",
          2442: "7",
          2447: "8",
          2452: "9",
          2457: "10",
          2462: "11",
          2467: "12",
          2472: "13"}
mac2fon = {"00:18:84:89:3f:c2": "Fon5,4.1.A13",
           "00:18:84:89:3f:b6": "Fon2,4.1.F13",
           "00:18:84:89:3f:9a": "Fon6,4.1.F01",
           "00:18:84:89:3f:a2": "Fon7,4.1.F15",
           "00:18:84:89:3f:a6": "Fon10,4.1.A16",
           "00:18:84:89:3f:ae": "Fon11,4.1.C01",
           "00:18:84:89:3e:da": "Fon9,4.1.F03",
           "00:18:84:89:3f:8e": "Fon4,4.1.C01",
           "00:18:84:89:3f:be": "Fon3,4.1.A03",
           "00:18:84:89:3f:8a": "Fon8,4.1.F03",
           "00:18:84:89:3e:e2": "Fon1,4.1.A03",
           "001884893fc2": "Fon5,4.1.A13",
           "001884893fb6": "Fon2,4.1.F13",
           "001884893f9a": "Fon6,4.1.F01",
           "001884893fa2": "Fon7,4.1.F15",
           "001884893fa6": "Fon10,4.1.A16",
           "001884893fae": "Fon11,4.1.C01",
           "001884893eda": "Fon9,4.1.F03",
           "001884893f8e": "Fon4,4.1.C01",
           "001884893fbe": "Fon3,4.1.A03",
           "001884893f8a": "Fon8,4.1.F03",
           "001884893ee2": "Fon1,4.1.A03"}
fon2mac = {"fon5": "001884893fc2",
           "fon2": "001884893fb6",
           "fon6": "001884893f9a",
           "fon7": "001884893fa2",
           "fon10": "001884893fa6",
           "fon11": "001884893fae",
           "fon9": "001884893eda",
           "fon4": "001884893f8e",
           "fon3": "001884893fbe",
           "fon8": "001884893f8a",
           "fon1": "001884893ee2"}


dircapturas = r'/srv/Capturas'
dirvendors = r'/srv/Servidor/scripts_escorpion/vendors'
dirservices = r'/srv/Servidor/scripts_escorpion/services'
dirregistros = r'/srv/Registros'
fonera_id = "FonXX"
nombrepcap = ""

createDb = sqlite3.connect(
    # os.path.dirname(os.path.abspath(__file__)) + '/dbtest.sqlite3')
    '/srv/Servidor/web/tfgweb/db.sqlite3')
createDb.text_factory = str
queryCurs = createDb.cursor()


def main():
    global fonera_id
    try:
        cargar_vendors(dirvendors)
        cargar_services(dirservices)
        if sys.argv[1] == "procesa":
            dirpcap = os.getcwd() + '/' + sys.argv[2]
            procesapcap(dirpcap)
        elif sys.argv[1] == "borrarantiguos":
            borrarantiguos(dircapturas)
        elif sys.argv[1] == "buscapcap":
            if sys.argv[2].lower().startswith('fon'):
                dirbuscapcap = r'/srv/Capturas/' + \
                    fon2mac[sys.argv[2].lower()]
                logger.debug("La direccion a inspeccionar es %s", dirbuscapcap)
                buscapcap(dirbuscapcap)
            elif sys.argv[2].lower().startswith('/') or sys.argv[2].lower().startswith('.'):
                logger.debug("La direccion a inspeccionfar es %s", sys.argv[2])
                buscapcap(sys.argv[2])
            elif sys.argv[2].lower().startswith('001884'):
                fonera_id = mac2fon[sys.argv[2].lower()].split(',')[0]
                dirbuscapcap = r'/srv/Capturas/' + sys.argv[2].lower()
                buscapcap(dirbuscapcap)
            else:
                logger.critical(
                    "No se ha introducido un nombre de fonera (FonXX) o mac o dirección asbsoluta o relativa valida")
        else:
            logger.critical("Parametros disponibles: procesa, buscapcap")
        queryCurs.close()
    except getopt.GetoptError:
        print "Error al usar el script. Ayuda?"
        print "Parametros disponibles: procesa, buscapcap"
        queryCurs.close()
        sys.exit()


def borrarantiguos(dircapturas):
    now = time.time()
    for root, dirs, files in os.walk(dircapturas):
        # f = os.path.join(dircapturas, f)
        for file in files:
            try:
                f = root + "/" + file
                if os.path.isfile(f):
                    if os.stat(f).st_mtime < now - 30 * 86400:
                        logger.info(
                            "%s es más antiguo de 30 dias. Se procerá a su borrado.", file)
                        # os.remove(f)
            except Exception, e:
                logger.warning("Excepcion %s", str(e))


def buscapcap(dirbuscapcap):
    global nombrepcap
    global fonera_id
    logger.debug("Buscando nuevos pcap en %s", dirbuscapcap)
    fonera_id = mac2fon[dirbuscapcap.split('/')[-1]].split(',')[0]
    try:
        lista_archivos = sorted(os.listdir(dirbuscapcap))
        for dir_entry in lista_archivos[:-1]:
            if dir_entry.endswith('.pcap'):
                dir_entry_path = os.path.join(dirbuscapcap, dir_entry)
                if os.path.isfile(dir_entry_path):
                    logger.debug("dir_entry son %s", dir_entry)
                    procesapcap(dirbuscapcap + "/" + dir_entry)
    except OSError as e:
        logger.info("La carpeta %s no existe para buscar pcaps", str(e))


def procesapcap(dirpcap):
    global nombrepcap
    global fonera_id
    global clientes_encontrados
    global lista_clientes
    global aps_encontrados
    global throughput_dict
    global bytes_dict
    global intervals_dict

    # Reinicializar vbles
    clientes_encontrados = dict()
    lista_clientes = dict()
    aps_encontrados = dict()
    throughput_dict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6":
                       0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0}
    bytes_dict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0,
                  "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0}
    intervals_dict = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6":
                      0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0}

    logger.debug("PARAMETRO FONERA: %s", dirpcap.split('/')[-2])
    if dirpcap.split('/')[-2].startswith('0018848'):
        fonera_id = mac2fon[dirpcap.split('/')[-2]].split(',')[0]
        if dirpcap.split('/')[-1].startswith('captura-'):
            nombrepcap = dirpcap.split('/')[-1]
            logger.debug("El nombre del pcap es %s", nombrepcap)
            # borrar_tablas()
            crear_tablas()
            try:
                queryCurs.execute(
                    'SELECT fonera_id, nombrepcap, estado FROM tfgplot_resumenpcap WHERE fonera_id =? AND nombrepcap =?', (fonera_id, nombrepcap))
                datos_respuesta = queryCurs.fetchall()
            except Exception, e:
                logger.warning("Excepcion %s", str(e))
            if not datos_respuesta:
                logger.info("Procesando %s", dirpcap)
                logger.info(
                    "Este pcap ha sido capturado por la fonera %s", fonera_id)
                for k in range(1, 13):
                    while True:
                        try:
                            queryCurs.execute(
                            'INSERT INTO tfgplot_resumenpcap (fonera_id, nombrepcap, estado, canal, inicio_tstamp, final_tstamp, throughput, ultimo_pcap) VALUES (?,?,?,?,?,?,?,?)',
                            (fonera_id, nombrepcap, "procesando", k, time.strftime("%Y-%m-%d %H:%M:%S"), time.strftime("%Y-%m-%d %H:%M:%S"), 0, "no"))
                            createDb.commit()
                        except sqlite.OperationalError, e:
                            logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                            time.sleep(2)
                            continue
                        except Exception, e:
                            logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                            time.sleep(2)
                            continue
                        break

                try:
                    queryCurs.execute(
                        'SELECT fonera_id FROM tfgplot_estado_foneras WHERE fonera_id =?', (fonera_id,))
                    datos_respuesta_estado = queryCurs.fetchall()
                except Exception, e:
                    logger.warning("Excepcion %s", str(e))
                if not datos_respuesta_estado:

                    queryCurs.execute('DELETE FROM tfgplot_estado_foneras')
                    createDb.commit()
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon1", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon2", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon3", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon4", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon5", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon6", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon7", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon8", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon9", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon10", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                    queryCurs.execute(
                        'INSERT INTO tfgplot_estado_foneras (fonera_id, ip, localizacion, ultimo_reg, carga_cpu, tmp_ocupado, ruta_mnt_servidor, ruta_mnt_fonera, ultimo_rei, disco_ocupado, baja_notificada) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                        ("Fon11", "163.117.1", "4.1.", time.strftime("%Y-%m-%d %H:%M:%S"), "0.00", "0%", "ruta", "ruta", time.strftime("%Y-%m-%d %H:%M:%S"), "0%", "no"))
                createDb.commit()
                cargar_pcap(dirpcap)
                encontrar_aps()
                encontrar_clientes()
                encontrar_throughputs(dirpcap)
                actualizar_registros(dirregistros)
                try:
                    queryCurs.execute(
                        'UPDATE tfgplot_resumenpcap SET ultimo_pcap=? WHERE fonera_id =?', ("no", fonera_id))
                    queryCurs.execute(
                        'UPDATE tfgplot_resumenpcap SET estado=?, ultimo_pcap=? WHERE fonera_id =? AND nombrepcap =?',
                        ("procesado", "si", fonera_id, nombrepcap))
                    createDb.commit()
                except Exception, e:
                    logger.debug("Excepcion %s", str(e))
            else:
                logger.debug(
                    "Se ha encontrado un pcap existente para la fonera %s con el nombre %s. Estado: %s",
                    fonera_id, nombrepcap, datos_respuesta[0][2])
        else:
            logger.warning(
                "El archivo de captura debe estar en una carpeta de fonera correcta (empezar por 0018848)")
    else:
        logger.warning(
            "El archivo de captura debe tener el formato captura-AÑO-MES-DIA-HORA-MINUTO.pcap")


def encontrar_clientes():
    global clientes_encontrados
    global lista_clientes
    global aps_encontrados
    global throughput_dict
    global bytes_dict
    global intervals_dict
    logger.debug('\nBuscando clientes...')
    for p in pkts:
        # comprobar que tenemos la capa wifi para cada paquete
        if p.haslayer(Dot11):
            # tipos de tramas de management enviadas solo por el cliente (según
            # Wireshark)
            # if p.type == 0 and p.subtype in (0, 2, 4):
            # si se mandan datos (no tramas de control o management)
            if p.type == 2:
                # comprobar si estaba en la lista
                if p.addr2 not in clientes_encontrados and p.addr1 in aps_encontrados:
                    vendor = "desconocido"  # valor por defecto
                    nombre_ap = "desconocido"  # valor por defecto
                    for clave in range(17, 5, -3):  # mirar por octetos
                        if p.addr2.upper()[:clave] in vendors:
                            vendor = vendors[p.addr2.upper()[:clave]]
                            break
                    nombre_ap = aps_encontrados[p.addr1][0]
                    # print("Mac: " + p.addr2 + " Vendor: " + vendor + " \tConectado a: " + p.addr1 + "(" + nombre_ap + ")").expandtabs(18)
                    entidad_cliente = vendor, nombre_ap
                    clientes_encontrados[p.addr2] = entidad_cliente
                    if p.addr1 in lista_clientes:
                        lista_clientes[
                            p.addr1] += (", " + p.addr2 + "(" + vendor + ")")
                    else:
                        lista_clientes[p.addr1] = p.addr2 + "(" + vendor + ")"

    # print "\n   ", len(clientes_encontrados), "clientes encontrados"
    logger.info("%d clientes encontrados en total", len(clientes_encontrados))
    # print "\n Lista de clientes encontrados:\n", clientes_encontrados
    logger.debug("Se han encontrado los siguientes clientes: %s",
                 clientes_encontrados)
    # print "\n Lista de clientes encontrados ordenados por
    # AP:\n",lista_clientes

    for aps in aps_encontrados:
        if aps in lista_clientes:
            while True:
                try:
                    queryCurs.execute('UPDATE tfgplot_radar SET clientes_encontrados=? WHERE mac=?', (lista_clientes[aps], aps))
                    createDb.commit()
                except sqlite.OperationalError, e:
                    logger.info("Realizando bypass a [%s]. Actualizar clientes.", str(e))
                    time.sleep(2)
                    continue
                except Exception, e:
                    logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                    time.sleep(2)
                    continue
                break
            
        # else:
        #     queryCurs.execute(
        #         'UPDATE tfgplot_radar SET clientes_encontrados=? WHERE mac=?', ("No se ha encontrado ningun cliente conectado a este Punto de Acceso", aps))


def encontrar_aps():
    global clientes_encontrados
    global lista_clientes
    global aps_encontrados
    global throughput_dict
    global bytes_dict
    global intervals_dict
    try:
        logger.debug("Actualizando puntos de acceso que ve %s", fonera_id)
        while True:
            try:
                queryCurs.execute(
                    'DELETE FROM tfgplot_radar WHERE fonera_id =?', (fonera_id,))
                createDb.commit()
            except sqlite.OperationalError, e:
                logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                time.sleep(2)
                continue
            except Exception, e:
                logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                time.sleep(2)
                continue
            break
    except Exception, e:
        logger.warning("Excepcion %s. %s", str(e), sys.exc_traceback.tb_lineno)

    for p in pkts:
        if p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp):
            if p[Dot11].addr3 not in aps_encontrados:
                vendor = "desconocido"
                ssid = p[Dot11Elt].info
                bssid = p[Dot11].addr3
                try:
                    canal = int(ord(p[Dot11Elt:3].info))
                except:
                    canal = int(str(hex(ord(p.getlayer(RadioTap).getfieldval('notdecoded')[3]))[
                                2:4]) + str(hex(ord(p.getlayer(RadioTap).getfieldval('notdecoded')[2]))[2:4]), 16)
                # para ver si el AP usa algún tipo de cifrado
                capability = p.sprintf(
                    "{Dot11Beacon:%Dot11Beacon.cap%}{Dot11ProbeResp:%Dot11ProbeResp.cap%}")
                if re.search("privacy", capability):
                    enc = 'Si'
                else:
                    enc = 'No'
                for clave in range(17, 5, -3):
                    if bssid.upper()[:clave] in vendors:
                        vendor = vendors[bssid.upper()[:clave]]
                        break
                if canal > 13 or canal < 1:
                    canal = 0
                entity = ssid, str(canal), enc, vendor
                aps_encontrados[bssid] = entity
                # print (ssid + ': ' + bssid + "\tCanal: " + str(canal) +  " Cifrado: " + enc + " Vendor: " + vendor).expandtabs(35)
                while True:
                    try:
                        queryCurs.execute(
                            'INSERT INTO tfgplot_radar (fonera_id, canal, ap_encontrado, cifrado, mac, vendor, clientes_encontrados) VALUES (?,?,?,?,?,?,?)',
                            (fonera_id, canal, ssid, enc, bssid, vendor, "null"))
                        createDb.commit()
                    except sqlite.OperationalError, e:
                        logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                        time.sleep(2)
                        continue
                    except Exception, e:
                        logger.info("Realizando bypass a [%s]. Borrado de radar previo.", str(e))
                        time.sleep(2)
                        continue
                    break

    logger.info("%s puntos de acceso encontrados", len(aps_encontrados))
    logger.debug("Se han encontrado los siguientes puntos de acceso: %s",
                 aps_encontrados)


def encontrar_throughputs(dirpcap):
    global clientes_encontrados
    global lista_clientes
    global aps_encontrados
    global throughput_dict
    global bytes_dict
    global intervals_dict
    logger.debug('Calculando throughputs por canal...')
    totalbytes = 0
    primerait = True
    contador_reps = 0
    contador_tmp = 0
    posi = 0
    ch_estable = "X"
    global throughput_dict

    pktts = RawPcapReader(dirpcap)
    for pktraw, (sec, usec, wirelen) in pktts:
        tamanos.append(wirelen)

    for pos, pkt in enumerate(pkts):
        if pkt.haslayer(Dot11Elt):
            try:
                canal = int(ord(pkt[Dot11Elt:3].info))
            except:
                canal = int(str(hex(ord(pkt.getlayer(RadioTap).getfieldval('notdecoded')[3]))[
                            2:4]) + str(hex(ord(pkt.getlayer(RadioTap).getfieldval('notdecoded')[2]))[2:4]), 16)
                canal = mhz2ch[canal]
        else:
            try:
                canal = int(str(hex(ord(pkt.getlayer(RadioTap).getfieldval('notdecoded')[3]))[
                            2:4]) + str(hex(ord(pkt.getlayer(RadioTap).getfieldval('notdecoded')[2]))[2:4]), 16)
                canal = mhz2ch[canal]
            except:
                pass

        canal = str(canal)
        if pos == 0:
            inicio_tstamp = datetime.fromtimestamp(
                pkts[0].time).strftime('%Y-%m-%d %H:%M:%S')
            ch_tmp = canal
            ultimo_intervalo = ""
            time_estable = datetime.fromtimestamp(
                pkts[0].time).strftime('%Y-%m-%d %H:%M:%S')
        elif pos == len(pkts) - 1:
            ultimo_intervalo = datetime.strptime(datetime.fromtimestamp(pkts[pos].time).strftime(
                '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(time_estable), '%Y-%m-%d %H:%M:%S')
            time_estable = datetime.fromtimestamp(
                pkts[pos].time).strftime('%Y-%m-%d %H:%M:%S')
            final_tstamp = datetime.fromtimestamp(
                pkts[pos].time).strftime('%Y-%m-%d %H:%M:%S')
            intervals_dict[ch_estable] += ultimo_intervalo.total_seconds()
        elif ch_tmp == canal and ch_estable != canal:
            contador_tmp += 1
            if contador_tmp == 5:
                contador_reps = 5
                caux = ch_estable
                ch_tmp = canal
                ch_estable = canal
                contador_tmp = 0
        elif ch_tmp == canal and ch_estable == canal:
            contador_reps += 1
            bytes_dict[canal] += tamanos[pos]
            if contador_reps == 6:
                ch_estable = ch_tmp
                if primerait:
                    posi = pos - 6
                    time_estable = datetime.fromtimestamp(
                        pkts[pos - 6].time).strftime('%Y-%m-%d %H:%M:%S')
                # try:
                if time_estable != "" and not primerait:
                    ultimo_intervalo = datetime.strptime(datetime.fromtimestamp(
                        pkts[pos - 6].time).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(time_estable), '%Y-%m-%d %H:%M:%S')
                    time_estable = datetime.fromtimestamp(
                        pkts[pos - 6].time).strftime('%Y-%m-%d %H:%M:%S')
                    posi = pos - 6
                    intervals_dict[
                        caux] += ultimo_intervalo.total_seconds()
                primerait = False
                # except:
                    # pass
        else:
            ch_tmp = canal
            contador_tmp = 0
        # print "PAQUETE", pos
        # print "TIMESTAMP PKT ACTUAL:", datetime.fromtimestamp(pkt.time).strftime('%Y-%m-%d %H:%M:%S')
        # print "CANAL:", canal
        # print "canal estable:", ch_estable
        # print "contador temporal:", contador_tmp
        # print "contador de repeticiones estable:", contador_reps
        totalbytes += tamanos[pos]

    for k, v in bytes_dict.items():
        if k in intervals_dict:
            if intervals_dict[k] != 0:
            # kbits/seg
                throughput = round((8 * v) / (1000 * intervals_dict[k]))
                throughput_dict[k] = throughput
            else:
                throughput = 0
                throughput_dict[k] = throughput
            while True:
                try:
                    queryCurs.execute(
                        'UPDATE tfgplot_resumenpcap SET inicio_tstamp =?, final_tstamp =?, throughput =?  WHERE fonera_id =? AND nombrepcap =? AND estado =? AND canal=?',
                        (inicio_tstamp, final_tstamp, throughput, fonera_id, nombrepcap, "procesando", k))
                    createDb.commit()
                except sqlite.OperationalError, e:
                    logger.info("Realizando bypass a [%s]. throughput_dict.", str(e))
                    time.sleep(2)
                    continue
                except Exception, e:
                    logger.info("Realizando bypass a [%s]. throughput_dict.", str(e))
                    time.sleep(2)
                    continue
                break

            # queryCurs.execute(
            #         'INSERT INTO tfgplot_resumenpcap (fonera_id, nombrepcap, estado, inicio_tstamp, final_tstamp, canal, throughput) VALUES (?,?,?,?,?,?,?)',
            #         (fonera_id, nombrepcap, "procesando", inicio_tstamp, final_tstamp, k, throughput))

    # print "\nTOTAL BYTES: ", totalbytes
    # print "BYTES POR CANALES:", bytes_dict
    logger.debug(
        "%d kilobytes de información en el total de paquetes capturados", totalbytes / 1000)
    logger.debug("Diccionario de bytes/canales: %s", bytes_dict)
    logger.debug("Diccionario de intervalos/canales: %s", intervals_dict)
    logger.debug("Diccionario de throughput/canal: %s", throughput_dict)


def crear_tablas():
    logger.debug("Creando tablas en la base de datos db.sqlite3")
    queryCurs.executescript('''
BEGIN;
CREATE TABLE IF NOT EXISTS "tfgplot_resumenpcap" (
    "clave" integer NOT NULL PRIMARY KEY,
    "fonera_id" varchar(6) NOT NULL,
    "nombrepcap" varchar(200) NOT NULL,
    "estado" varchar(200) NOT NULL,
    "inicio_tstamp" datetime NOT NULL,
    "final_tstamp" datetime NOT NULL,
    "canal" smallint NOT NULL,
    "throughput" decimal NOT NULL,
    "ultimo_pcap" varchar(2) NOT NULL
)
;
CREATE TABLE IF NOT EXISTS "tfgplot_radar" (
    "clave" integer NOT NULL PRIMARY KEY,
    "fonera_id" varchar(7) NOT NULL,
    "canal" smallint NOT NULL,
    "ap_encontrado" varchar(254) NOT NULL,
    "cifrado" varchar(2) NOT NULL,
    "mac" varchar(17) NOT NULL,
    "vendor" varchar(250) NOT NULL,
    "clientes_encontrados" text NOT NULL
)
;
CREATE TABLE IF NOT EXISTS "tfgplot_estado_foneras" (
    "clave" integer NOT NULL PRIMARY KEY,
    "fonera_id" varchar(6) NOT NULL,
    "ip" varchar(15) NOT NULL,
    "localizacion" varchar(254) NOT NULL,
    "ultimo_reg" datetime NOT NULL,
    "carga_cpu" decimal NOT NULL,
    "tmp_ocupado" smallint NOT NULL,
    "ruta_mnt_servidor" varchar(254) NOT NULL,
    "ruta_mnt_fonera" varchar(254) NOT NULL,
    "ultimo_rei" datetime NOT NULL,
    "disco_ocupado" smallint NOT NULL,
    "baja_notificada" varchar(2) NOT NULL
)
;

COMMIT;
    ''')


def borrar_tablas():
    # ojo con eliminar la tabla entera cada vez
    queryCurs.executescript('''BEGIN;
        DROP TABLE IF EXISTS "tfgplot_estado_foneras"; 
        DROP TABLE IF EXISTS "tfgplot_radar"; 
        DROP TABLE IF EXISTS "tfgplot_resumenpcap";
        COMMIT;''')


def actualizar_registros(dirregistros):
    try:
        logger.debug("\n Actualizando registros de foneras")
    except Exception, e:
        logger.warning("Excepcion %s", str(e))
    fmt = '%Y-%m-%d-%H-%M'
    for dir_entry in os.listdir(dirregistros):
        dir_entry_path = os.path.join(dirregistros, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as fichero:
                dictregistros[dir_entry] = fichero.read()
    # para leer los datos de cada archivo
    for foneras in dictregistros:
        lineas = dictregistros[foneras].splitlines()
        baja_notificada = "no"
        for linea in lineas:
            try:
                fonera_id_reg, localizacion = mac2fon[str(foneras)].split(',')
                if linea.find("IP") != -1:
                    ip = linea.split(": ")[1].strip().split("/")[0]
                elif linea.find("registro") != -1:
                    ultimo_reg = datetime.strptime(
                        linea.split(": ")[1].strip(), fmt)
                    try:
                        # 1h
                        if (datetime.strptime(datetime.strftime(datetime.now(), fmt), fmt) - ultimo_reg).total_seconds() >= 3600:
                            queryCurs.execute(
                                'SELECT baja_notificada FROM tfgplot_estado_foneras WHERE fonera_id =? AND baja_notificada =?', (fonera_id_reg, "no"))
                            datos_respuesta_baja = queryCurs.fetchall()
                            if datos_respuesta_baja:
                                logger.info(
                                    "Se mandará email notificando sobre la fonera %s", fonera_id_reg)
                                # enviaremail(from_addr='fonera.tfg@gmail.com',
                                # to_addr_list=['kikexclusive@gmail.com'],
                                # cc_addr_list=['fonera.tfg@gmail.com'],
                                # subject='Fonera ' + fonera_id_reg + ' caída. Notificación automática ' + datetime.strftime(datetime.now(), fmt),
                                # mensaje='Mensaje automático generado a las ' + datetime.strftime(datetime.now(), fmt) + '\n\nLa fonera ' + fonera_id_reg + ' se registró por último vez hace más de 25 minutos.\n\nSe recomienda comprobar su conexión en el despacho ' + localizacion + '.',
                                # login='fonera.tfg',
                                # password='foneratfg')
                                baja_notificada = "si"
                                queryCurs.execute(
                                    'UPDATE tfgplot_estado_foneras SET baja_notificada=? WHERE fonera_id=?', (baja_notificada, fonera_id_reg))
                                createDb.commit()
                        else:
                            baja_notificada = "no"
                            queryCurs.execute(
                                'UPDATE tfgplot_estado_foneras SET baja_notificada=? WHERE fonera_id=?', (baja_notificada, fonera_id_reg))
                            createDb.commit()
                    except Exception, e:
                        logger.warning(
                            "Error al mandar el email de notificación de baja. Razón: %s", str(e))
                elif linea.find("reinicio") != -1:
                    ultimo_rei = datetime.strptime(
                        linea.split(": ")[1].strip(), '%Y-%m-%d-%H-%M')
                elif linea.find("disco usado") != -1:
                    disco_ocupado = linea.split(": ")[1].strip()
                elif linea.find("temporal usado") != -1:
                    tmp_ocupado = linea.split(": ")[1].strip()
                elif linea.find("procesador") != -1:
                    carga_cpu = linea.split(": ")[1].strip()
                elif linea.find("en escorpion") != -1:
                    ruta_mnt_servidor = linea.split(": ")[1].strip()
                elif linea.find("de escorpion") != -1:
                    ruta_mnt_fonera = linea.split(": ")[1].strip()
            except Exception, e:
                logger.warning(
                    "Error al procesar los archivos de registros de las foneras: %s", str(e))
        logger.debug("Procesada la info de registro de la fonera %s (%s)",
                     foneras, mac2fon[foneras])
        queryCurs.execute(
            'UPDATE tfgplot_estado_foneras SET localizacion=?, ip=?, ultimo_reg=?, ultimo_rei=?, disco_ocupado=?, tmp_ocupado=?, carga_cpu=?, ruta_mnt_fonera=?, ruta_mnt_servidor=? WHERE fonera_id=?',
            (localizacion, ip, ultimo_reg, ultimo_rei, disco_ocupado, tmp_ocupado, carga_cpu, ruta_mnt_fonera, ruta_mnt_servidor, fonera_id_reg))
        createDb.commit()

# def anadir_potencias():
#     global lista_potencia
#     lista_potencia = []
#     for pkt in pkts:
#         if pkt.haslayer(Dot11):
#             origen_pkt = pkt.getlayer(Dot11).getfieldval('addr3')
#             if origen_pkt != "00:00:00:00:00:00":
#                 potdb = int(-(256 - ord(pkt.notdecoded[-4:-3])))
#                 instante = datetime.fromtimestamp(
#                     pkt.time).strftime('%Y-%m-$d %H%M%S').split(' ')[1]
#                 entidad_potencia = instante, origen_pkt, potdb
#                 lista_potencia.append(entidad_potencia)
#     sorted(lista_potencia, key=itemgetter(1))
#     print "Lista ordenada?", lista_potencia
#     queryCurs.execute('INSERT INTO tcp (potdb) VALUES (?)', (potdb,))

# def encontrar_servicios():
    # logger.debug("Buscando servicios en uso en las redes no cifradas")
    # for pkt in pkts:
        # if pkt.haslayer(TCP):
        #     if pkt.getlayer(TCP).getfieldval('sport') not in servicios_encontrados or \
        #             pkt.getlayer(TCP).getfieldval('dport') not in servicios_encontrados:
        #         src_port = str(pkt.getlayer(TCP).getfieldval('sport'))
        #         dst_port = str(pkt.getlayer(TCP).getfieldval('dport'))
        # servicio = "desconocido"  # valor por defecto
        #         if src_port.strip() in services:
        #             if services[src_port].split(",")[1] == 'tcp' or services[src_port].split(",")[1] == 'sctp':
        # servicio tiene la forma
        # puerto,descripcion_servicio,protocolo
        #                 servicio = src_port, services[src_port].split(",")[0],\
        #                     services[src_port].split(",")[1]
        #                 if servicio not in servicios_encontrados:
        #                     servicios_encontrados.append(servicio)
        #     cnt += 1

        # if pkt.haslayer(UDP):
        #     if pkt.getlayer(UDP).getfieldval('sport') not in servicios_encontrados or \
        #       s      pkt.getlayer(UDP).getfieldval('dport') not in servicios_encontrados:
        #         src_port = str(pkt.getlayer(UDP).getfieldval('sport'))
        #         dst_port = str(pkt.getlayer(UDP).getfieldval('dport'))
        # servicio = "desconocido"  # valor por defecto
        #         if src_port.strip() in services:
        #             if services[src_port].split(",")[1] == 'udp' or services[src_port].split(",")[1] == 'dccp':
        # servicio tiene la forma
        # puerto,descripcion_servicio,protocolo
        #                 servicio = src_port, services[src_port].split(",")[0],\
        #                     services[src_port].split(",")[1]
        #                 if servicio not in servicios_encontrados:
        #                     servicios_encontrados.append(servicio)
        #     cnt += 1

        # if pkt.haslayer(ARP) or pkt.haslayer(DNS):
        #         print "\n     Paquete que usa ARP o DNS", pkts.index(pkt)
        #         print datetime.fromtimestamp(pkt.time).strftime('%Y-%m-$d %H:%M:%S').split(' ')[1]
        #     cnt2 = cnt2 + 1


    # print "\n   Servicios encontrados (conocido el puerto):"
    # for valores in servicios_encontrados:
        # print "   Puerto:", valores[0], " Servicio:", valores[1], " Protocolo:", valores[2]
    # print "\n   Total paquetes (TCP,UDP o ICMP):", str(cnt)
    # print "\n   Total paquetes (ARP,DNS):", str(cnt2)
    #     print "Inicio a las", datetime.fromtimestamp(pkts[1].time).strftime('%Y-%m-$d %H:%M:%S').split(' ')[1]
    # print "Fin a las",
    # datetime.fromtimestamp(pkts[-1].time).strftime('%Y-%m-$d
    # %H:%M:%S').split(' ')[1]

# def mostrar100aleat():
        # print "\n\n\n ################## \n   Mostrando 100 paquetes aleatorios"
        # for aleat in range(100):
        #     num = random.randrange(1, len(pkts), 1)
        #     print "\nPaquete", num, "Timestamp:", datetime.fromtimestamp(pkt.time).strftime('%Y-%m-$d %H:%M:%S').split(' ')[1]
        #     print len(pkt)
        #     print pkt.show2()


def cargar_services(filename):
    logger.debug(
        "Cargando la base de datos de relacion servicios/puerto en %s", filename)
    try:
        for l in open(filename):
            try:
                l = l.strip()
                if not l or l.startswith("#"):
                    continue
                servid, puerto, protoc, descr = l.split(",")
                puerto = puerto.strip()
                protoc = protoc.strip()
                servid = servid.strip()
                descr = descr.strip()
                services[puerto] = descr + "," + protoc
            except Exception, e:
                print "No se ha podido parsear una linea de [%s] [%r] (%s)" % (filename, l, e)
        logger.debug(
            "Se ha cargado el achivo de puertos/Servicios con %s entradas", len(services))
    except:
        logger.warning("Excepción: %s", sys.exc_info()[0])
        print "Excepción: %s" % (sys.exc_info()[0])


def cargar_vendors(filename):
    logger.debug(
        "Cargando la base de datos de fabricantes fabricante/mac en %s", filename)
    try:
        for l in open(filename):
            try:
                l = l.strip()
                if not l or l.startswith("#"):
                    continue
                macd, vendord = l.split("#")[:2]
                macd = macd.strip()
                vendord = vendord.strip()
                vendors[macd] = vendord
            except Exception, e:
                print "No se ha podido parsear una linea de [%s] [%r] (%s)" % (filename, l, e)
        logger.debug(
            "Se ha cargado el achivo de fabricantes/mac con %s entradas", len(vendors))
    except:
        logger.warning("Excepción: %s", sys.exc_info()[0])
        print "Excepción: %s" % (sys.exc_info()[0])


def cargar_pcap(dirpcap):
    global pkts
    logger.debug("Cargando el archivo de capturas pcap en %s", dirpcap)
    try:
        pkts = rdpcap(dirpcap)
    except Exception, e:
        logger.warning(
            "Se ha producido un error al cargar el fichero [%s] (%s)", dirpcap, e)
    logger.info("Se han cargado %d paquetes", len(pkts))

# Función enviaremail de la función que recoge los parametros pasados por
# consola al ejecutar el script y empieza a correr el script


def enviaremail(from_addr, to_addr_list, cc_addr_list,
                subject, mensaje,
                login, password,
                smtpserver='smtp.gmail.com:587'):
    logger.debug(
        'Enviando email a %s de %s cc a %s con asunto %s y mensaje %s', from_addr, to_addr_list, cc_addr_list, subject, mensaje)
    cabecera = 'From: %s\n' % from_addr
    cabecera += 'To: %s\n' % ','.join(to_addr_list)
    cabecera += 'Cc: %s\n' % ','.join(cc_addr_list)
    cabecera += 'Subject: %s\n\n' % subject
    mensaje = cabecera + mensaje
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problemas = server.sendmail(from_addr, to_addr_list, mensaje)
    server.quit()
    logger.debug('Respuesta del servidor: %s', problemas)


if __name__ == "__main__":
    ini_time = time.time()
    logger.debug(int(os.popen("ps -ef | grep python | grep 'tfg_servidor.py' | wc -l").read()))
    if int(os.popen("ps -ef | grep python | grep 'tfg_servidor.py' | wc -l").read()) > 3:
        logger.debug(
            "El script tfg_servidor.py ya se está ejecutando. Sólo se permite una instancia.")
        sys.exit()
    logger.info("\nComienzo de la ejecucion: %s", time.strftime("%c"))
    main()
    logger.info("Script ejecutado en %d segundos", time.time() - ini_time)
    sys.exit()


# para mandar email


# para aislar en la consola. borrar
# import sys
# import getopt
# import subprocess
# import random
# import os
# import datetime
# from datetime import datetime
# import time
# from scapy.all import *
# from scapy.utils import rdpcap
# import sqlite3
# from operator import itemgetter
# import logging
# pkts = rdpcap("./captura-2014-02-13-00-44-39.pcap")
