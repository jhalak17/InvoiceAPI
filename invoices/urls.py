from django.urls import path
from .views import InvoiceView

urlpatterns = [
    path('invoices', InvoiceView.as_view()),
]