import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Plan, Subscription, Payment
from .serializers import PlanSerializer, SubscriptionSerializer, PaymentSerializer
from apps.accounts.permissions import IsAcademyAdmin

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_mockkey')

class PlanListView(generics.ListAPIView):
    """List all active subscription plans."""
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]

class StripeCheckoutView(APIView):
    """POST /api/billing/stripe/checkout/ — Create a checkout session."""
    permission_classes = [permissions.IsAuthenticated, IsAcademyAdmin]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        plan = generics.get_object_or_404(Plan, id=plan_id)
        academy = request.user.owned_academies.first() # Simplification for now

        if not academy:
            return Response({"error": "No academy found for this user."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=request.user.email,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': plan.name},
                        'unit_amount': int(plan.price_monthly * 100),
                        'recurring': {'interval': 'month'},
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=settings.SITE_URL + '/dashboard?payment=success',
                cancel_url=settings.SITE_URL + '/dashboard?payment=cancel',
                metadata={
                    'academy_id': academy.id,
                    'plan_id': plan.id
                }
            )
            return Response({'checkout_url': checkout_session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe Webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        academy_id = session['metadata']['academy_id']
        plan_id = session['metadata']['plan_id']
        subscription_id = session['subscription']
        customer_id = session['customer']

        # Activate subscription
        sub = Subscription.objects.get(academy_id=academy_id)
        sub.plan_id = plan_id
        sub.status = 'active'
        sub.stripe_subscription_id = subscription_id
        sub.stripe_customer_id = customer_id
        sub.payment_method = 'stripe'
        sub.save()

    return HttpResponse(status=200)

class ManualPaymentSubmitView(APIView):
    """POST /api/billing/manual/submit/ — Submit JazzCash/EasyPaisa Ref."""
    permission_classes = [permissions.IsAuthenticated, IsAcademyAdmin]

    def post(self, request):
        amount = request.data.get('amount')
        method = request.data.get('method') # jazzcash/easypaisa
        ref_id = request.data.get('ref_id')
        
        academy = request.user.owned_academies.first()
        sub = academy.subscription

        Payment.objects.create(
            subscription=sub,
            amount=amount,
            method=method,
            status='pending',
            manual_ref=ref_id
        )
        return Response({"message": "Payment submitted for verification."}, status=status.HTTP_201_CREATED)

class PayPalCreateOrderView(APIView):
    """POST /api/billing/paypal/create-order/"""
    permission_classes = [permissions.IsAuthenticated, IsAcademyAdmin]

    def post(self, request):
        # In a real app, use PayPal SDK to create order
        plan_id = request.data.get('plan_id')
        plan = get_object_or_404(Plan, id=plan_id)
        
        return Response({
            "order_id": "MOCK_PAYPAL_ORDER_ID", 
            "status": "CREATED"
        })

class PayPalCaptureView(APIView):
    """POST /api/billing/paypal/capture/"""
    permission_classes = [permissions.IsAuthenticated, IsAcademyAdmin]

    def post(self, request):
        order_id = request.data.get('order_id')
        # In a real app, capture via PayPal API
        
        academy = request.user.owned_academies.first()
        sub = academy.subscription
        sub.status = 'active'
        sub.payment_method = 'paypal'
        sub.save()
        
        Payment.objects.create(
            subscription=sub,
            amount=0, # Should get from capture response
            method='paypal',
            status='completed',
            paypal_order_id=order_id
        )
        return Response({"status": "COMPLETED"})
