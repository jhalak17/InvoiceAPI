from django.contrib import admin

from .models import InvoiceDetail

# Register your models here.
class InvoiceDetailProfile(admin.ModelAdmin):
    list_display = ['invoice__invoice_number', 'invoice__customer_name', 'description', 'quantity', 'price']

admin.site.register(InvoiceDetail, InvoiceDetailProfile)
