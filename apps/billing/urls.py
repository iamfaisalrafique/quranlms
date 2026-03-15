from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('plans/', views.PlanListView.as_view(), name='plan-list'),
    path('stripe/checkout/', views.StripeCheckoutView.as_view(), name='stripe-checkout'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('paypal/create-order/', views.PayPalCreateOrderView.as_view(), name='paypal-create-order'),
    path('paypal/capture/', views.PayPalCaptureView.as_view(), name='paypal-capture'),
    path('manual/submit/', views.ManualPaymentSubmitView.as_view(), name='manual-submit'),
]
