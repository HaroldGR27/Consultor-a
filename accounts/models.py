from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el modelo de usuario predeterminado de Django
    para incluir el campo de ID para el cliente de Stripe.

    Atributos:
    - stripe_customer_id (CharField): Campo para almacenar el ID del cliente de Stripe asociado
      con el usuario.
    """
    stripe_customer_id = models.CharField(max_length=50)