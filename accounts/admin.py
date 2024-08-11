from django.contrib import admin
from django.http import HttpResponse
from .models import User
import csv
# Registra los modelos que se crean del archivo ConsultoriaApp/models.py.

#Modelo para agregar o modificar Usuarios
admin.site.register(User)
