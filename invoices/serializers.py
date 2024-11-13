from rest_framework import serializers
from django.utils import timezone

from .models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'description', 'quantity', 'price', 'line_total']

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive value.")
        return value
    
class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'date', 'customer_name', 'details']

    def _validate_invoice_number(self, value):
        if not value.strip():
            raise serializers.ValidationError("Invoice number cannot be empty.")
        if Invoice.objects.filter(invoice_number=value).exists():
            raise serializers.ValidationError("Invoice number must be unique.")
        return value
    
    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate_customer_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Customer name cannot be empty.")
        return value

    def validate(self, data):
        details = data.get('details')
        if not details:
            raise serializers.ValidationError("Invoice must have at least one detail.")
        if self.context['request'].method == "POST":
            self._validate_invoice_number(data["invoice_number"])
        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        instance.details.all().delete()
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=instance, **detail_data)
        return instance