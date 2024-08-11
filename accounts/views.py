from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CancelSubscriptionForm
from django.views.generic import FormView, View
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

import stripe
from django.contrib import messages


class CancelSubscriptionView(LoginRequiredMixin, FormView):
    form_class=CancelSubscriptionForm

    def get_success_url(self):
        return reverse("user:subscription", kwargs={"username": self.request.user.username})

    def form_valid(self, form):
        stripe.Subscription.delete(self.request.user.subscription.stripe_subscription_id)
        messages.success(self.request, "Has cancelado exitosamente tu suscripcion")
        return super().form_valid(form)


class UserSubscriptionView(View):
    """
    Vista basada en clase para mostrar las suscripciones de un usuario específico.

    Métodos:
    - get: Maneja las solicitudes GET para mostrar la página de suscripción del usuario.
    """
    def get(self, request, username,*args, **kwargs):
        """
        Maneja las solicitudes GET. Obtiene la información de suscripción de un usuario específico
        y la muestra en la plantilla correspondiente.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - username: El nombre de usuario del usuario cuyas suscripciones se desean ver.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - HttpResponse: La respuesta HTTP con la plantilla renderizada.
        """
        user = get_object_or_404(User, username=username)
        context={
            'user':user
        }
        return render(request, 'users/user_subscription.html',context)