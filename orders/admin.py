from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'shipping_full_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__username', 'shipping_full_name', 'shipping_city']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informations de commande', {
            'fields': ('order_number', 'user', 'status', 'total_amount', 'notes')
        }),
        ('Adresse de livraison', {
            'fields': (
                'shipping_full_name', 'shipping_phone',
                'shipping_address_line1', 'shipping_address_line2',
                'shipping_city', 'shipping_postal_code', 'shipping_country'
            )
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )
