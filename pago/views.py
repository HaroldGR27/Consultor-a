from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views import View

from ConsultoriaApp.models import Pricing, Subscription

import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()


# Create your views here.

class PricingView(View):
    """
    Vista basada en clase para mostrar la página de precios.

    Métodos:
    - get: Maneja las solicitudes GET para mostrar la página de precios.
    """
    def get(self, request, *args, **kwargs):
        """
        Maneja las solicitudes GET. Prepara el contexto y renderiza la plantilla de precios.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - HttpResponse: La respuesta HTTP con la plantilla renderizada.
        """
        context={
        }
        return render(request, 'ConsultoriaApp/Pago/pricing.html', context)
    
class PaymentView(View):
    """
    Vista para manejar el proceso de pago.

    Métodos:
    - get: Maneja las solicitudes GET para mostrar la página de checkout.
    """
    def get(self, request, slug,*args, **kwargs):
        """
        Maneja las solicitudes GET. Recupera los precios correspondientes al slug
        que se haya agregado y prepara el contexto para la plantilla de checkout.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - slug: El identificador único de los precios.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - HttpResponse: La respuesta HTTP con la plantilla renderizada.
        """

        pricing = get_object_or_404(Pricing, slug=slug)

        context={
            'pricing_tier':pricing,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        }

        return render(request, 'ConsultoriaApp/pago/checkout.html', context)

class CreateSubscriptionView(LoginRequiredMixin, View):
    """
    Vista para crear suscripciones de usuarios utilizando Stripe.

    Hereda:
    - LoginRequiredMixin: Asegura que el usuario esté autenticado.
    - View: Vista base de Django para manejar solicitudes HTTP.

    Métodos:
    - post: Maneja las solicitudes POST para crear una suscripción.
    """
    def post(self, request, *args, **kwargs):
        """
        Maneja las solicitudes POST para crear una suscripción.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - JsonResponse: Respuesta JSON con los detalles de la suscripción o un mensaje de error.
        """
        if request.method != 'POST':
            return HttpResponse(status=405)  # Método no permitido

        data = json.loads(request.body.decode('utf-8'))
        customer_id = request.user.stripe_customer_id

        try:
            # Vincular el método de pago al cliente
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id
            )

            # Configurar método de pago predeterminado del cliente
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Obtener el objeto Pricing
            pricing = Pricing.objects.get(stripe_price_id=data["priceId"])

            # Crear suscripción
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': data["priceId"]}],
                expand=['latest_invoice.payment_intent'],
            )

            # Guardar la suscripción en la base de datos
            Subscription.objects.create(
                user=request.user,
                pricing=pricing,
                stripe_subscription_id=subscription.id,
                status=subscription.status,
            )

            data = {}
            data.update(subscription)
            
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({
                "error": {'message': str(e)}
            }, status=400)

class ThankYouView(View):
    """
    Vista para mostrar la página de agradecimiento después de un pago exitoso.

    Hereda:
    - View: Vista base de Django para manejar solicitudes HTTP.

    Métodos:
    - get: Maneja las solicitudes GET para mostrar la página de agradecimiento.
    """
    def get(self, request, *args, **kwargs):
        """
        Maneja las solicitudes GET para mostrar la página de ThankYou.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - HttpResponse: Respuesta HTTP con el contenido renderizado de la página de agradecimiento.
        """
        context={            
        }
        return render(request, 'ConsultoriaApp/Pago/thankyou.html', context)    

class RetryInvoiceView(View):
    """
    Vista para manejar el reintento de pago en Stripe.

    Hereda:
    - View: Vista base de Django para manejar solicitudes HTTP.

    Métodos:
    - post: Maneja las solicitudes POST para reintentar el pago de una factura.
    """
    def post(self, request, *args, **kwargs):
        """
        Maneja las solicitudes POST para reintentar el pago de una factura en Stripe.

        Parámetros:
        - request: El objeto HttpRequest que contiene los datos de la solicitud.
        - *args: Argumentos adicionales.
        - **kwargs: Argumentos clave adicionales.

        Retorna:
        - JsonResponse: Respuesta JSON con los datos de la factura o un mensaje de error.
        """
        # Verificar que la solicitud es de tipo POST
        if request.method != 'POST':
            return HttpResponse(status=405)  # Método no permitido

        # Obtener los datos del cuerpo de la solicitud
        data = json.loads(request.body.decode('utf-8'))
        customer_id = request.user.stripe_customer_id

        try:
            # Vincular el método de pago al cliente
            stripe.PaymentMethod.attach(
                data['paymentMethodId'],
                customer=customer_id,
            )
            # Configurar método de pago predeterminado del cliente
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': data['paymentMethodId'],
                },
            )

            # Recuperar la factura
            invoice = stripe.Invoice.retrieve(
                data['invoiceId'],
                expand=['payment_intent'],
            )

            # Preparar datos de respuesta
            response_data = {}
            response_data.update(invoice)

            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({
                "error": {'message': str(e)}
            }, status=400)

def send_invoice(request, invoice_id):
    try:
        invoice = stripe.Invoice.send_invoice(invoice_id)
        return JsonResponse({"message":"Invoice sent successfully", "invoice":invoice})
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def webhook(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body

    signature = request.META.get("HTTP_STRIPE_SIGNATURE")
    if not signature:
        return JsonResponse({'error': 'No signature provided'}, status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret
        )
        data = event['data']
    except Exception as e:
        # Registrar el error y devolver una respuesta de error
        print(f"Error verifying webhook signature: {e}")
        return HttpResponse(status=400)

    event_type = event['type']
    data_object = data['object']

    if event_type == 'invoice.payment_succeeded':
        subscription_id = data_object.get("subscription")
        if subscription_id:
            subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id).first()
            if subscription:
                subscription.status = 'active'
                subscription.save()

    elif event_type == 'invoice.payment_failed':
        print(f"Payment failed for invoice: {data_object}")

    elif event_type == 'customer.subscription.deleted':
        subscription_id = data_object.get("id")
        if subscription_id:
            subscription = Subscription.objects.filter(stripe_subscription_id=subscription_id).first()
            if subscription:
                subscription.status = 'canceled'
                subscription.save()

    return JsonResponse({'status': 'success'}, status=200)

class ChangeSubscriptionView(View):
    def post(self, request, *args, **kwargs):
        # Verificar que la solicitud es de tipo POST
        if request.method != 'POST':
            return HttpResponse(status=405)  # Método no permitido

        # Obtener los datos del cuerpo de la solicitud
        data = json.loads(request.body.decode('utf-8'))

        subscription_id = request.user.subscription.stripe_subscription_id
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        try:
            # Modificar la suscripción
            updated_subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=False,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': data["priceId"],
                }],
                proration_behavior="always_invoice"
            )

            # Preparar datos de respuesta
            response_data = {}
            response_data.update(updated_subscription)
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({
                "error": {'message': str(e)}
            }, status=400)