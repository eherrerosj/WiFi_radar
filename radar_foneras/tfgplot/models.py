# -*- encoding: utf-8 -*-
from django.db import models
import random
import datetime


class resumenpcap(models.Model):
    clave = models.AutoField(primary_key=True)  # autoincremento
    fonera_id = models.CharField(max_length=6,default="Fon")  # FonXX
    nombrepcap = models.CharField(max_length=200,default="captura-")
    estado = models.CharField(max_length=200,default="no procesado")
    # datetime.datetime instance
    inicio_tstamp = models.DateTimeField(auto_now=False, auto_now_add=False,default=datetime.datetime.now)
    # datetime.datetime instance
    final_tstamp = models.DateTimeField(auto_now=False, auto_now_add=False,default=datetime.datetime.now)
    canal = models.SmallIntegerField(default=0)  # max es 13 min es 1
    throughput = models.DecimalField(max_digits=9, decimal_places=2,default=0)
    ultimo_pcap = models.CharField(max_length=2)
    # tipos_pkts_encontrados = models.CharField(max_length=254)
    # protocolo puede ser 802.11, tcp, udp, sctp o dccp. servicio puede ser de
    # la lista de servicios, beacon, etc.


class radar(models.Model):
    clave = models.AutoField(primary_key=True)  # autoincremento
    fonera_id = models.CharField(max_length=7)  # FonXX
    canal = models.SmallIntegerField()  # del 1 al 11
    ap_encontrado = models.CharField(max_length=254)  # ssid
    cifrado = models.CharField(max_length=2)  # Si o No
    mac = models.CharField(max_length=17)  # bssid = mac del ap
    vendor = models.CharField(max_length=250)
    clientes_encontrados = models.TextField(default="")  # mac_cliente(vendor), ...
    def lista_clientes_encontrados(self):
        return self.clientes_encontrados.split('), ')
    def aleat(self):
        return random.randint(1,10000)


class estado_foneras(models.Model):
    clave = models.AutoField(primary_key=True)  # autoincremento
    fonera_id = models.CharField(max_length=6)  # FonXX
    ip = models.CharField(max_length=15)  # IP local de la fonera
    localizacion = models.CharField(max_length=254)
    ultimo_rei = models.DateTimeField(auto_now=False, auto_now_add=False) # datetime.datetime
    ultimo_reg = models.DateTimeField(auto_now=False, auto_now_add=False)
    ruta_mnt_fonera = models.CharField(max_length=254)
    ruta_mnt_servidor = models.CharField(max_length=254)
    tmp_ocupado = models.SmallIntegerField()  # de 0 a 100
    carga_cpu = models.DecimalField(max_digits=5, decimal_places=2, default=0.0100)
    disco_ocupado = models.SmallIntegerField()  # de 0 a 100
    baja_notificada = models.CharField(max_length=2, default="no")  # Si o No