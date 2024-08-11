from django.contrib import admin
from .models import Pricing, Subscription, Cursos

# Registra los modelos que se crean del archivo ConsultoriaApp/models.py.

#Modelo para agregar los Cursos
admin.site.register(Cursos)
#Modelo para agregar los precios
admin.site.register(Pricing)
#Modelos para agregar o modificar las suscripciones
admin.site.register(Subscription)


