from django.urls import path
from ConsultoriaApp import views


urlpatterns = [
    #Menu
    path('',views.inicio, name="Inicio"),
    path('¿Quienes-somos?',views.conocenos, name="Conocenos"),
    path('Contacto',views.contacto, name="Contacto"),

    #Login
    path('Inicio-de-sesion',views.inicios, name="index"),
    path('Registro',views.registro, name="registro"),
    path('signout/',views.cierres, name='signout'),

    #Servicios
    path('1-Tramites-Registros-y-Autorizaciones',views.tramites, name="Tramites"),
    path('2-Auditoria-Preventiva',views.auditoria, name="Auditoria"),
    path('3-Atencion-de-Auditorias',views.atencion, name="Atencion"),
    path('4-Asistencia-Legal',views.asistencia, name="Asistencia"),
    path('5-Asistencia-en-la-Operacion-Aduanera',views.asistenciaOA, name="AsistenciaOA"),
    path('6-Capacitacion',views.capacitacion, name="Capacitacion"),
    path('7-Estrategias-Comerciales',views.estrategias, name="Estrategias"),
    path('8-Servicios-Corporativas',views.serviciosC, name="ServiciosC"),
    path('9-Servicios-Digitales',views.serviciosD, name="ServiciosD"),
    path('10-Alianzas-Estrategicas',views.alianzas1, name="Alianzas1"),
    path('10.2-Alianzas-Estrategicas',views.alianzas2, name="Alianzas2"),
    path('10.3-Alianzas-Estrategicas',views.alianzas3, name="Alianzas3"),

    #Videos
    path('Tramites-Registros-y-Autorizaciones',views.tramitesvideo, name="TramiteVideo"),
    path('Auditoria-Preventiva',views.auditoriavideo, name="auditoriaVideo"),
    path('Atencion-de-Auditorias',views.atenciónvideo, name="auditoriaVideo"),
    path('Asistencia-Legal',views.asistenciavideo, name="asitenciavideo"),
    path('Asistencia-en-la-Operacion-Aduanera',views.aoavideo, name="aoavideo"),
    path('Capacitacion',views.capacitacionvideo, name="capacitacionvideo"),
    path('Estrategias-Comerciales',views.estrategiasvideo, name="estrategiasvideo"),
    path('Servicios-Corporativas',views.servicioscvideo, name="servicioscvideo"),
    path('Servicios-Digitales',views.serviciosdvideo, name="serviciosdvideo"),
    path('Alianzas-Estrategicas',views.ae1video, name="ae1video"),
    path('Alianzas-Estrategicas-2',views.ae2video, name="ae2video"),
    path('Alianzas-Estrategicas-3',views.ae3video, name="ae3video"),
]