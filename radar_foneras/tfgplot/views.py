# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from tfgplot.models import *
from django.db.models import Avg
import tfgplot.models
from django.template import RequestContext, loader
import itertools


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def avg(xs):
    xs = [x for x in xs if x is not None]
    return int(round(sum(xs) / len(xs)))



def index(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.order_by('fonera_id') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]
	
	# U200clave_trazas = list(resumenpcap.objects.order_by('-inicio_tstamp')[0:2600])[::-1]  # 13 canales * 200 ultimas muestras de cada uno


	template = loader.get_template('tfgplot/index.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/index.html', context)


def index2(request):
	values_11 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.order_by('fonera_id') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]
	
	U200clave_trazas = list(resumenpcap.objects.order_by('-inicio_tstamp')[0:2400])[::-1]  # 12 canales * 200 ultimas muestras de cada uno


	template = loader.get_template('tfgplot/index2.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,
		'U200clave_trazas': U200clave_trazas,

		'avgs_11': zip(avgs_11, tavgs_11)[-100:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-100:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-100:-1]
	})
	return render(request, 'tfgplot/index2.html', context)

def home(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.order_by('fonera_id') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/boot.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,
	})
	return render(request, 'tfgplot/boot.html', context)



def thr_fon1(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon1").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon1') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon1.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon1.html', context)

def thr_fon2(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon2").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon2') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon2.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon2.html', context)

def thr_fon3(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon3").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon3') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon3.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon3.html', context)

def thr_fon4(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon4").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon4') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon4.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon4.html', context)

def thr_fon5(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon5").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon5') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon5.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon5.html', context)

def thr_fon6(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon6").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon6') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon6.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon6.html', context)

def thr_fon7(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon7").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon7') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon7.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon7.html', context)

def thr_fon8(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon8").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon8') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon8.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon8.html', context)

def thr_fon9(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon9").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon9') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon9.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon9.html', context)

def thr_fon10(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon10").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon10') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon10.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon10.html', context)

def thr_fon11(request):
	values_11 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=11).order_by('inicio_tstamp').values_list('throughput', flat=True)
	tavgs_11 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=11).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	avgs_11 = [avg(xs) for xs in grouper(values_11, 6)]

	values_6 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=6).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_6 = [avg(xs) for xs in grouper(values_6, 6)]
	tavgs_6 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=6).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]

	values_1 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=1).order_by('inicio_tstamp').values_list('throughput', flat=True)
	avgs_1 = [avg(xs) for xs in grouper(values_1, 6)]
	tavgs_1 = resumenpcap.objects.filter(fonera_id="Fon11").filter(canal=1).order_by('inicio_tstamp').values_list('inicio_tstamp', flat=True)[::6]
	
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id='Fon11') # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	clave_trazas11_10 = resumenpcap.objects.filter(canal=11).order_by('inicio_tstamp')[::5]
	clave_trazas6_10 = resumenpcap.objects.filter(canal=6).order_by('inicio_tstamp')[::5]
	clave_trazas1_10 = resumenpcap.objects.filter(canal=1).order_by('inicio_tstamp')[::5]

	template = loader.get_template('tfgplot/thr_fon11.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas,

		'clave_trazas11_10': clave_trazas11_10,
		'clave_trazas6_10': clave_trazas6_10,
		'clave_trazas1_10': clave_trazas1_10,

		'avgs_11': zip(avgs_11, tavgs_11)[-1200:-1],
		'avgs_6': zip(avgs_6, tavgs_6)[-1200:-1],
		'avgs_1': zip(avgs_1, tavgs_1)[-1200:-1]
	})
	return render(request, 'tfgplot/thr_fon11.html', context)



def tab_fon1(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon1") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/tab_fon1.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/tab_fon1.html', context)


def tab_fon2(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon2") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/tab_fon2.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/tab_fon2.html', context)


def tab_fon3(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon3") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/tab_fon3.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/tab_fon3.html', context)


def tab_fon4(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon4") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/tab_fon4.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/tab_fon4.html', context)


def tab_fon5(request):
	pass
def tab_fon6(request):
	pass
def tab_fon7(request):
	pass
def tab_fon8(request):
	pass
def tab_fon9(request):
	pass
def tab_fon10(request):
	pass
def tab_fon11(request):
	pass


def jit_fon1(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon1") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/jit_fon1.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/jit_fon1.html', context)


def jit_fon2(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon2") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/jit_fon2.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/jit_fon2.html', context)


def jit_fon3(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon3") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/jit_fon3.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/jit_fon3.html', context)


def jit_fon4(request):
	clave_ef = estado_foneras.objects.order_by('clave') # estado foneras
	clave_radar = radar.objects.filter(fonera_id="Fon4") # radar
	clave_trazas = resumenpcap.objects.order_by('inicio_tstamp') # resumen pcap, todos

	template = loader.get_template('tfgplot/jit_fon4.html')
	context = RequestContext(request, {
		'clave_ef': clave_ef,
		'clave_radar': clave_radar,
		'clave_trazas': clave_trazas
	})
	return render(request, 'tfgplot/jit_fon4.html', context)


def jit_fon5(request):
	pass
def jit_fon6(request):
	pass
def jit_fon7(request):
	pass
def jit_fon8(request):
	pass
def jit_fon9(request):
	pass
def jit_fon10(request):
	pass
def jit_fon11(request):
	pass