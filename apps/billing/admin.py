from django.contrib import admin
from .models import Plan, Subscription, Payment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'price_monthly', 'max_students', 'is_active')
    list_filter = ('tier', 'is_active')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('academy', 'plan', 'status', 'expires_at')
    list_filter = ('status', 'plan')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'currency', 'method', 'status', 'created_at')
    list_filter = ('status', 'method', 'currency')
    search_fields = ('stripe_payment_id', 'paypal_order_id', 'manual_ref')
