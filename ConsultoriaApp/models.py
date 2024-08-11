from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
import stripe

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.

class Pricing(models.Model):
    """
    Modelo que representa los diferentes precios de los cursos.

    Atributos:
    - name (CharField): Nombre del plan de precios.
    - slug (SlugField): Identificador único para la URL del plan de precios.
    - stripe_price_id (CharField): Identificador del precio en Stripe.
    - price (DecimalField): Monto del precio del plan.
    - currency (CharField): Moneda en la que se expresa el precio.
    """
    name= models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    stripe_price_id = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    currency = models.CharField(max_length=50)

    def __str__(self):
        """
        Devuelve una representación en cadena del modelo.
        
        Returns:
            str: El nombre del plan de precios.
        """
        return self.name

class Subscription(models.Model):
    """
    Modelo que representa las suscripciones que tienen los usuarios.

    Atributos:
    - user (ForeignKey): Referencia al usuario que posee la suscripción.
    - pricing (ForeignKey): Referencia al plan de precios asociado a la suscripción.
    - created (DateTimeField): Fecha y hora en que se creó la suscripción.
    - stripe_subscription_id (CharField): Identificador de la suscripción en Stripe.
    - status (CharField): Estado actual de la suscripción.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name='subscriptions')
    created = models.DateTimeField(auto_now_add=True)
    stripe_subscription_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.email} - {self.pricing.name}"

    @property
    def is_active(self):
        """
        Verifica si la suscripción está activa o en periodo de prueba.

        Returns:
            bool: True si la suscripción está activa o en periodo de prueba, False en caso contrario.
        """
        return self.status in ["active", "trialing"]
  
class Cursos(models.Model):
    """
    Modelo que representa los cursos que se agregan.

    Atributos:
    - pricing_tiers (ManyToManyField): Nombre de los diferentes precios de los cursos.
    - course_name (CharField): Nombre del curso.
    - title (CharField): Título del curso.
    - sub_title (CharField): Subtítulo del curso.
    - video (FileField): Archivo de video del curso.
    - content (TextField): Descripción o contenido del curso.
    - published (DateTimeField): Fecha y hora de publicación del curso.
    - is_active (BooleanField): Indica si el curso está activo.
    """
    pricing_tiers = models.ManyToManyField(Pricing, blank=True)
    course_name = models.CharField(max_length=100, default='Nombre de Curso')
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    video = models.FileField(upload_to='ConsultoriaApp/%y', default='ConsultoriaApp/24')
    content = models.TextField(blank=True, null=True)
    published = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title    