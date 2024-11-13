from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceView(APIView):
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        invoice_number = request.data.get("invoice_number")
        try:
            invoice = Invoice.objects.get(invoice_number = invoice_number)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

