from django.urls import path

from .views import ChangeSubscriptionView, CreateSubscriptionView, PaymentView, PricingView, RetryInvoiceView, ThankYouView, send_invoice, webhook

app_name="pago"

urlpatterns = [
    path('pricing/', PricingView.as_view(), name="pricing"),
    path('checkout/<slug>/', PaymentView.as_view(), name="checkout"),
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('thank-you/',ThankYouView.as_view(),name='thank-you'),
    path('retry-invoice/', RetryInvoiceView.as_view(), name='retry-invoice'),
    path('webhook/', webhook, name='webhook'),
    path('change-subscription/', ChangeSubscriptionView.as_view(), name='change-subscription'),
    path('send-invoice/<str:invoice_id>/', send_invoice, name='send-invoice')
]