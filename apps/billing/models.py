from django.db import models
from django.conf import settings

class Plan(models.Model):
    """Subscription plans for Academies."""
    TIER_CHOICES = (
        ('starter', 'Starter'),
        ('growth', 'Growth'),
        ('enterprise', 'Enterprise'),
    )
    name = models.CharField(max_length=100)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)
    max_students = models.PositiveIntegerField()
    features = models.JSONField(default=dict, help_text="List of features enabled for this plan")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.tier})"

class Subscription(models.Model):
    """Academy's current subscription status."""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('trial', 'Trialing'),
    )
    academy = models.OneToOneField('academy.Academy', on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    payment_method = models.CharField(max_length=50, blank=True, help_text="stripe, paypal, manual")
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.academy.name} - {self.plan.name} ({self.status})"

class Payment(models.Model):
    """History of all payments made by Academies."""
    METHOD_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('jazzcash', 'JazzCash'),
        ('easypaisa', 'EasyPaisa'),
        ('bank_transfer', 'Bank Transfer'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Provider references
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    manual_ref = models.CharField(max_length=255, blank=True, null=True, help_text="JazzCash/EasyPaisa Ref ID")
    
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.subscription.academy.name} - {self.amount} {self.currency} ({self.status})"
