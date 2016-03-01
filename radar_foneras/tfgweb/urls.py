# -*- encoding: utf-8 -*-
from django.conf.urls import patterns, include, url
from tfgplot import views
from django.contrib import admin
from django.conf import settings

admin.autodiscover()
urlpatterns = patterns('',
		   url(r'^$', 'tfgplot.views.home', name='home'),
		   url(r'^admin/', include(admin.site.urls)),
		   url(r'^index/', views.index, name='index'),

		   url(r'^thr_fon1/', views.thr_fon1, name='thr_fon1'),
		   url(r'^thr_fon2/', views.thr_fon2, name='thr_fon2'),
		   url(r'^thr_fon3/', views.thr_fon3, name='thr_fon3'),
		   url(r'^thr_fon4/', views.thr_fon4, name='thr_fon4'),
		   url(r'^thr_fon5/', views.thr_fon5, name='thr_fon5'),
		   url(r'^thr_fon6/', views.thr_fon6, name='thr_fon6'),
		   url(r'^thr_fon7/', views.thr_fon7, name='thr_fon7'),
		   url(r'^thr_fon8/', views.thr_fon8, name='thr_fon8'),
		   url(r'^thr_fon9/', views.thr_fon9, name='thr_fon9'),
		   url(r'^thr_fon10/', views.thr_fon10, name='thr_fon10'),
		   url(r'^thr_fon11/', views.thr_fon11, name='thr_fon11'),

		   url(r'^tab_fon1/', views.tab_fon1, name='tab_fon1'),
		   url(r'^tab_fon2/', views.tab_fon2, name='tab_fon2'),
		   url(r'^tab_fon3/', views.tab_fon3, name='tab_fon3'),
		   url(r'^tab_fon4/', views.tab_fon4, name='tab_fon4'),
		   url(r'^tab_fon5/', views.tab_fon5, name='tab_fon5'),
		   url(r'^tab_fon6/', views.tab_fon6, name='tab_fon6'),
		   url(r'^tab_fon7/', views.tab_fon7, name='tab_fon7'),
		   url(r'^tab_fon8/', views.tab_fon8, name='tab_fon8'),
		   url(r'^tab_fon9/', views.tab_fon9, name='tab_fon9'),
		   url(r'^tab_fon10/', views.tab_fon10, name='tab_fon10'),
		   url(r'^tab_fon11/', views.tab_fon11, name='tab_fon11'),

		   url(r'^jit_fon1/', views.jit_fon1, name='jit_fon1'),
		   url(r'^jit_fon2/', views.jit_fon2, name='jit_fon2'),
		   url(r'^jit_fon3/', views.jit_fon3, name='jit_fon3'),
		   url(r'^jit_fon4/', views.jit_fon4, name='jit_fon4'),
		   url(r'^jit_fon5/', views.jit_fon5, name='jit_fon5'),
		   url(r'^jit_fon6/', views.jit_fon6, name='jit_fon6'),
		   url(r'^jit_fon7/', views.jit_fon7, name='jit_fon7'),
		   url(r'^jit_fon8/', views.jit_fon8, name='jit_fon8'),
		   url(r'^jit_fon9/', views.jit_fon9, name='jit_fon9'),
		   url(r'^jit_fon10/', views.jit_fon10, name='jit_fon10'),
		   url(r'^jit_fon11/', views.jit_fon11, name='jit_fon11'),

		   url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
) 
