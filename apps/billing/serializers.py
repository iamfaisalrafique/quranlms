from rest_framework import serializers
from .models import Plan, Subscription, Payment

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['verified_at', 'verified_by', 'status']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan_details = PlanSerializer(source='plan', read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'academy', 'plan', 'plan_details', 'status', 
            'started_at', 'expires_at', 'payment_method', 
            'stripe_subscription_id', 'payments'
        ]
        read_only_fields = ['status', 'started_at', 'expires_at', 'stripe_subscription_id']
